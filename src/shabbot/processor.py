from telegram import Update
from telegram.ext import ContextTypes

from shabbot.loggable import Loggable
from shabbot.message_parser import MessageParser
from shabbot.task_parser import TaskParser
from shabbot.todoist import TodoistClient


class Processor(Loggable):
    def __init__(
        self,
        text_parser: MessageParser,
        voice_parser: MessageParser,
        task_parser: TaskParser,
        todoist: TodoistClient,
    ) -> None:
        self._text_parser = text_parser
        self._voice_parser = voice_parser
        self._task_parser = task_parser
        self._todoist = todoist

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._process(update, context, self._text_parser)

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._process(update, context, self._voice_parser)

    async def _process(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_parser: MessageParser) -> None:
        assert update.message is not None
        assert update.effective_user is not None

        message = await message_parser.parse_update(update, context)
        task = self._task_parser.parse(message.text)

        self.logger.info("creating todoist task: %r", task.summary)
        result = await self._todoist.create_task(task)
        self.logger.info("created task id=%s", result.id)

        await update.message.reply_text(f"✅ Добавил: «{task.summary}»\nhttps://todoist.com/app/task/{result.id}")
