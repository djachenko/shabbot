from unittest.mock import AsyncMock, MagicMock

import pytest

from shabbot.message_parser import Message, TextMessageParser, VoiceMessageParserOutput


def _make_update(text: str = "hello") -> MagicMock:
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = text
    update.message.reply_text = AsyncMock()
    update.effective_user = MagicMock()
    update.effective_user.username = "testuser"
    return update


class TestTextMessageParser:
    @pytest.mark.anyio
    async def test_returns_message_with_text(self) -> None:
        """parse_update() возвращает Message с текстом из update"""
        parser = TextMessageParser()
        update = _make_update("Buy milk")

        result = await parser.parse_update(update, MagicMock())

        assert isinstance(result, Message)
        assert result.text == "Buy milk"

    @pytest.mark.anyio
    async def test_empty_text_returns_empty_message(self) -> None:
        """parse_update() возвращает пустой Message если text is None"""
        parser = TextMessageParser()
        update = _make_update()
        update.message.text = None

        result = await parser.parse_update(update, MagicMock())

        assert result is not None
        assert result.text == ""


class TestVoiceMessageParserOutput:
    @pytest.mark.anyio
    async def test_first_pulse_sends_reply(self) -> None:
        """transcribe_pulse() отправляет reply_text при первом вызове"""
        update = _make_update()
        output = VoiceMessageParserOutput(update)

        await output.transcribe_pulse()

        update.message.reply_text.assert_awaited_once()

    @pytest.mark.anyio
    async def test_second_pulse_edits_message(self) -> None:
        """transcribe_pulse() редактирует существующее сообщение при повторном вызове"""
        update = _make_update()
        status_msg = MagicMock()
        status_msg.edit_text = AsyncMock()
        update.message.reply_text = AsyncMock(return_value=status_msg)

        output = VoiceMessageParserOutput(update)
        await output.transcribe_pulse()
        await output.transcribe_pulse()

        update.message.reply_text.assert_awaited_once()
        status_msg.edit_text.assert_awaited_once()

    @pytest.mark.anyio
    async def test_transcribe_success_sends_text(self) -> None:
        """transcribe_success() отправляет распознанный текст"""
        update = _make_update()
        output = VoiceMessageParserOutput(update)

        await output.transcribe_success("Купить молоко")

        call_text = update.message.reply_text.call_args[0][0]
        assert "Купить молоко" in call_text

    @pytest.mark.anyio
    async def test_transcribe_error_sends_error(self) -> None:
        """transcribe_error() отправляет сообщение об ошибке"""
        update = _make_update()
        output = VoiceMessageParserOutput(update)

        await output.transcribe_error()

        update.message.reply_text.assert_awaited_once()

    @pytest.mark.anyio
    async def test_timeout_error_sends_message(self) -> None:
        """timeout_error() отправляет сообщение о таймауте"""
        update = _make_update()
        output = VoiceMessageParserOutput(update)

        await output.timeout_error()

        update.message.reply_text.assert_awaited_once()
