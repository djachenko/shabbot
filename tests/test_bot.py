import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from telegram import Update

from shabbot.bot import Bot
from shabbot.message_parser import MessageParseError
from shabbot.todoist import TodoistError
from shabbot.transcribe import TranscriptionError


def _make_bot() -> Bot:
    return Bot(config=MagicMock(), processor=MagicMock())


def _make_context(error: BaseException) -> MagicMock:
    context = MagicMock()
    context.bot.send_message = AsyncMock()
    context.error = error
    return context


def _make_update(text: str | None = None, caption: str | None = None, topic_id: int | None = None) -> MagicMock:
    update = MagicMock()
    update.__class__ = Update
    update.effective_chat = MagicMock()
    update.effective_chat.id = 42
    update.effective_message = AsyncMock()
    update.effective_message.text = text
    update.effective_message.caption = caption
    update.effective_message.is_topic_message = topic_id is not None
    update.effective_message.message_thread_id = topic_id
    update.effective_message.chat.id = 42
    update.effective_message.chat.type = "supergroup"
    return update


# -------------------------------------------------------------------
# _reject
# -------------------------------------------------------------------

class TestReject:
    def test_reply_explains_how_to_allow_chat(self) -> None:
        update = _make_update()

        asyncio.run(_make_bot()._reject(update, MagicMock()))

        update.effective_message.reply_text.assert_called_once_with(
            "🚫 Чат не в allowlist.\n"
            "chat_id: 42\n"
            "тип: supergroup\n"
            "Добавь chat_id в ALLOWED_CHAT_IDS и перезапусти бота."
        )

    def test_reply_includes_thread_id_from_topic(self) -> None:
        update = _make_update(topic_id=7)

        asyncio.run(_make_bot()._reject(update, MagicMock()))

        reply = update.effective_message.reply_text.call_args.args[0]
        assert "thread_id: 7" in reply

    def test_reply_thread_outside_topic_is_not_shown(self) -> None:
        update = _make_update()
        update.effective_message.message_thread_id = 5

        asyncio.run(_make_bot()._reject(update, MagicMock()))

        reply = update.effective_message.reply_text.call_args.args[0]
        assert "thread_id" not in reply

    def test_logs_rejected_chat(self, caplog: pytest.LogCaptureFixture) -> None:
        update = _make_update(topic_id=7)

        asyncio.run(_make_bot()._reject(update, MagicMock()))

        assert "rejected chat_id=42 thread_id=7 type=supergroup" in caplog.text

    def test_no_reply_without_message(self) -> None:
        update = MagicMock()
        update.effective_message = None

        asyncio.run(_make_bot()._reject(update, MagicMock()))


# -------------------------------------------------------------------
# _error_handler — ранний выход (нет кому отвечать)
# -------------------------------------------------------------------

class TestErrorHandlerEarlyReturn:
    @pytest.mark.anyio
    async def test_non_update_object_skips_reply(self) -> None:
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler("not an update", context)

        context.bot.send_message.assert_not_awaited()

    @pytest.mark.anyio
    async def test_no_effective_chat_skips_reply(self) -> None:
        update = _make_update()
        update.effective_chat = None
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_not_awaited()


# -------------------------------------------------------------------
# _error_handler — известные ошибки → конкретные сообщения
# -------------------------------------------------------------------

class TestErrorHandlerKnownErrors:
    @pytest.mark.anyio
    async def test_transcription_error(self) -> None:
        update = _make_update()
        context = _make_context(TranscriptionError("whisper timed out"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не удалось распознать голос", message_thread_id=None)

    @pytest.mark.anyio
    async def test_message_parse_error(self) -> None:
        update = _make_update()
        context = _make_context(MessageParseError("download timed out"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не удалось загрузить голосовое сообщение", message_thread_id=None)

    @pytest.mark.anyio
    async def test_todoist_error(self) -> None:
        update = _make_update()
        context = _make_context(TodoistError("api error"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось добавить задачу", message_thread_id=None)

    @pytest.mark.anyio
    async def test_replies_to_same_topic(self) -> None:
        update = _make_update(topic_id=7)
        context = _make_context(TodoistError("api error"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось добавить задачу", message_thread_id=7)

    @pytest.mark.anyio
    async def test_reply_thread_outside_topic_goes_to_chat(self) -> None:
        update = _make_update()
        update.effective_message.message_thread_id = 5
        context = _make_context(TodoistError("api error"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось добавить задачу", message_thread_id=None)


# -------------------------------------------------------------------
# _error_handler — неизвестная ошибка → fallback с контекстом
# -------------------------------------------------------------------

class TestErrorHandlerGenericError:
    @pytest.mark.anyio
    async def test_includes_text_in_message(self) -> None:
        update = _make_update(text="купить молоко")
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось. Текст был: купить молоко.", message_thread_id=None)

    @pytest.mark.anyio
    async def test_falls_back_to_caption_when_no_text(self) -> None:
        update = _make_update(text=None, caption="голосовая подпись")
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось. Текст был: голосовая подпись.", message_thread_id=None)

    @pytest.mark.anyio
    async def test_text_takes_priority_over_caption(self) -> None:
        update = _make_update(text="основной текст", caption="подпись")
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось. Текст был: основной текст.", message_thread_id=None)

    @pytest.mark.anyio
    async def test_generic_message_when_no_text_and_no_caption(self) -> None:
        update = _make_update(text=None, caption=None)
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось.", message_thread_id=None)

    @pytest.mark.anyio
    async def test_generic_message_when_no_effective_message(self) -> None:
        update = _make_update()
        update.effective_message = None
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось.", message_thread_id=None)


# -------------------------------------------------------------------
# Независимость сообщений
# Одно сообщение отрабатывает нормально — другое нет.
# Каждый вызов изолирован, ошибка в одном не влияет на другой.
# -------------------------------------------------------------------

class TestMessageIsolation:
    @pytest.mark.anyio
    async def test_different_errors_produce_independent_replies(self) -> None:
        bot = _make_bot()

        update1 = _make_update()
        context1 = _make_context(TranscriptionError("timed out"))

        update2 = _make_update(text="купить молоко")
        context2 = _make_context(RuntimeError("unexpected"))

        await bot._error_handler(update1, context1)
        await bot._error_handler(update2, context2)

        context1.bot.send_message.assert_awaited_once_with(42, "❌ не удалось распознать голос", message_thread_id=None)
        context2.bot.send_message.assert_awaited_once_with(42, "❌ не получилось. Текст был: купить молоко.", message_thread_id=None)

    @pytest.mark.anyio
    async def test_failed_message_does_not_affect_next(self) -> None:
        bot = _make_bot()

        update1 = _make_update()
        update1.effective_chat = None  # это сообщение молча проигнорируется
        context1 = _make_context(RuntimeError("first"))

        update2 = _make_update()
        context2 = _make_context(TodoistError("api error"))

        await bot._error_handler(update1, context1)
        await bot._error_handler(update2, context2)

        context1.bot.send_message.assert_not_awaited()
        context2.bot.send_message.assert_awaited_once_with(42, "❌ не получилось добавить задачу", message_thread_id=None)


# -------------------------------------------------------------------
# run() — регистрация хендлеров
# -------------------------------------------------------------------

class TestHandlerRegistration:
    def _run_bot(self, bot: Bot) -> MagicMock:
        mock_app = MagicMock()
        mock_app.run_polling = MagicMock()
        mock_builder = MagicMock()
        mock_builder.token.return_value = mock_builder
        mock_builder.concurrent_updates.return_value = mock_builder
        mock_builder.build.return_value = mock_app

        with patch("shabbot.bot.ApplicationBuilder", return_value=mock_builder):
            bot.run()

        return mock_app

    def test_three_message_handlers_registered(self) -> None:
        app = self._run_bot(_make_bot())

        assert app.add_handler.call_count == 3

    def test_error_handler_is_bot_method(self) -> None:
        bot = _make_bot()
        app = self._run_bot(bot)

        app.add_error_handler.assert_called_once_with(bot._error_handler)

    def test_registered_callbacks_include_processor_and_reject(self) -> None:
        bot = _make_bot()
        app = self._run_bot(bot)

        callbacks = {call.args[0].callback for call in app.add_handler.call_args_list}

        assert bot._processor.handle_text in callbacks
        assert bot._processor.handle_voice in callbacks
        assert bot._reject in callbacks

    def test_run_polling_called(self) -> None:
        app = self._run_bot(_make_bot())

        app.run_polling.assert_called_once()
