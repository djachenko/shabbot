from unittest.mock import AsyncMock, MagicMock

import pytest

from shabbot.message_parser import Message
from shabbot.processor import Processor
from shabbot.task_parser import Task
from datetime import date


def _make_update(text: str = "Buy milk") -> MagicMock:
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    update.effective_user = MagicMock()
    update.effective_user.username = "testuser"
    return update


def _make_processor(
    message: Message | None = Message("Buy milk"),
    task: Task | None = None,
) -> tuple[Processor, MagicMock, MagicMock, MagicMock]:
    text_parser = MagicMock()
    text_parser.parse_update = AsyncMock(return_value=message)

    voice_parser = MagicMock()
    voice_parser.parse_update = AsyncMock(return_value=message)

    if task is None:
        task = Task(summary="Buy milk", date=date.today())

    task_parser = MagicMock()
    task_parser.parse = MagicMock(return_value=task)

    todoist = MagicMock()
    result = MagicMock()
    result.id = "task-123"
    todoist.create_task = AsyncMock(return_value=result)

    processor = Processor(
        text_parser=text_parser,
        voice_parser=voice_parser,
        task_parser=task_parser,
        todoist=todoist,
    )

    return processor, text_parser, task_parser, todoist


class TestProcessorHandlers:
    @pytest.mark.anyio
    async def test_handle_text_uses_text_parser(self) -> None:
        """handle_text() передаёт update в text_parser"""
        processor, text_parser, _, _ = _make_processor()
        update = _make_update()
        context = MagicMock()

        await processor.handle_text(update, context)

        text_parser.parse_update.assert_awaited_once_with(update, context)

    @pytest.mark.anyio
    async def test_handle_voice_uses_voice_parser(self) -> None:
        """handle_voice() передаёт update в voice_parser"""
        processor, _, _, _ = _make_processor()
        voice_parser = processor._voice_parser
        update = _make_update()
        context = MagicMock()

        await processor.handle_voice(update, context)

        voice_parser.parse_update.assert_awaited_once_with(update, context)


class TestProcessorProcess:
    @pytest.mark.anyio
    async def test_creates_todoist_task(self) -> None:
        """_process() создаёт задачу в Todoist при успешном парсинге"""
        processor, _, task_parser, todoist = _make_processor()
        update = _make_update()

        await processor.handle_text(update, MagicMock())

        task_parser.parse.assert_called_once_with("Buy milk")
        todoist.create_task.assert_awaited_once()

    @pytest.mark.anyio
    async def test_replies_with_task_link(self) -> None:
        """_process() отправляет reply с summary и ссылкой на задачу"""
        processor, _, _, _ = _make_processor()
        update = _make_update()

        await processor.handle_text(update, MagicMock())

        reply_text = update.message.reply_text.call_args[0][0]
        assert "Buy milk" in reply_text
        assert "task-123" in reply_text

    @pytest.mark.anyio
    async def test_propagates_parser_exception(self) -> None:
        """_process() пробрасывает исключение из parser не перехватывая"""
        from shabbot.message_parser import MessageParseError

        processor, text_parser, _, todoist = _make_processor()
        text_parser.parse_update = AsyncMock(side_effect=MessageParseError("download timed out"))
        update = _make_update()

        with pytest.raises(MessageParseError):
            await processor.handle_text(update, MagicMock())

        todoist.create_task.assert_not_awaited()
