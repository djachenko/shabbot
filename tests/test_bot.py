import asyncio
from unittest.mock import AsyncMock, MagicMock

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


def _make_update(text: str | None = None) -> MagicMock:
    update = MagicMock()
    update.__class__ = Update
    update.effective_chat = MagicMock()
    update.effective_chat.id = 42
    update.effective_message = MagicMock()
    update.effective_message.text = text
    update.effective_message.caption = None
    return update


class TestReject:
    def test_replies_with_ban_emoji(self) -> None:
        message = AsyncMock()
        update = MagicMock()
        update.effective_message = message

        asyncio.run(_make_bot()._reject(update, MagicMock()))

        message.reply_text.assert_called_once_with("🚫")

    def test_no_reply_without_message(self) -> None:
        update = MagicMock()
        update.effective_message = None

        asyncio.run(_make_bot()._reject(update, MagicMock()))


class TestErrorHandler:
    @pytest.mark.anyio
    async def test_transcription_error(self) -> None:
        update = _make_update()
        context = _make_context(TranscriptionError("whisper timed out"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не удалось распознать голос")

    @pytest.mark.anyio
    async def test_message_parse_error(self) -> None:
        update = _make_update()
        context = _make_context(MessageParseError("download timed out"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не удалось загрузить голосовое сообщение")

    @pytest.mark.anyio
    async def test_todoist_error(self) -> None:
        update = _make_update()
        context = _make_context(TodoistError("api error"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось добавить задачу")

    @pytest.mark.anyio
    async def test_generic_error_with_text(self) -> None:
        update = _make_update(text="купить молоко")
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось. Текст был: купить молоко.")

    @pytest.mark.anyio
    async def test_generic_error_without_text(self) -> None:
        update = _make_update(text=None)
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_awaited_once_with(42, "❌ не получилось.")

    @pytest.mark.anyio
    async def test_no_chat_skips_reply(self) -> None:
        update = _make_update()
        update.effective_chat = None
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler(update, context)

        context.bot.send_message.assert_not_awaited()

    @pytest.mark.anyio
    async def test_non_update_object_skips_reply(self) -> None:
        context = _make_context(RuntimeError("unexpected"))

        await _make_bot()._error_handler("not an update", context)

        context.bot.send_message.assert_not_awaited()
