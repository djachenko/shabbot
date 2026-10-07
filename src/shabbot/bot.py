import logging

from telegram import Message, Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from shabbot.config import Config, load_config
from shabbot.message_parser import MessageParseError, TextMessageParser, VoiceMessageParser
from shabbot.processor import Processor
from shabbot.task_parser import SimpleTaskParser
from shabbot.todoist import TodoistClient, TodoistError
from shabbot.transcribe import Transcriber, TranscriptionError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)


def _topic_id(message: Message | None) -> int | None:
    if message is None or not message.is_topic_message:
        return None

    return message.message_thread_id


class Bot:
    def __init__(self, config: Config, processor: Processor) -> None:
        self._config = config
        self._processor = processor
        self._logger = logging.getLogger(__name__)

    async def _error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        self._logger.error("unhandled exception", exc_info=context.error)

        if not isinstance(update, Update) or update.effective_chat is None:
            return

        if isinstance(context.error, TranscriptionError):
            msg = "❌ не удалось распознать голос"
        elif isinstance(context.error, MessageParseError):
            msg = "❌ не удалось загрузить голосовое сообщение"
        elif isinstance(context.error, TodoistError):
            msg = "❌ не получилось добавить задачу"
        else:
            if update.effective_message:
                text = update.effective_message.text or update.effective_message.caption or ""
            else:
                text = ""

            suffix = f" Текст был: {text}." if text else ""
            msg = f"❌ не получилось.{suffix}"

        await context.bot.send_message(
            update.effective_chat.id,
            msg,
            message_thread_id=_topic_id(update.effective_message),
        )

    async def _reject(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message

        if message is None:
            return

        chat = message.chat
        topic_id = _topic_id(message)

        self._logger.warning("rejected chat_id=%s thread_id=%s type=%s", chat.id, topic_id, chat.type)

        lines = ["🚫 Чат не в allowlist.", f"chat_id: {chat.id}"]

        if topic_id is not None:
            lines.append(f"thread_id: {topic_id}")

        lines.append(f"тип: {chat.type}")
        lines.append("Добавь chat_id в ALLOWED_CHAT_IDS и перезапусти бота.")

        await message.reply_text("\n".join(lines))

    def run(self) -> None:
        allowed = filters.Chat(chat_id=self._config.allowed_chat_ids)

        app = ApplicationBuilder() \
            .token(self._config.shabbot_token) \
            .concurrent_updates(True) \
            .build()

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & allowed, self._processor.handle_text))
        app.add_handler(MessageHandler(filters.VOICE & allowed, self._processor.handle_voice))
        app.add_handler(MessageHandler(filters.ALL & ~allowed, self._reject))
        app.add_error_handler(self._error_handler)

        app.run_polling(drop_pending_updates=False, allowed_updates=Update.ALL_TYPES)


def main() -> None:
    config = load_config()

    transcriber = Transcriber(
        whisper_bin=config.whisper_bin,
        whisper_model=config.whisper_model,
    )

    processor = Processor(
        text_parser=TextMessageParser(),
        voice_parser=VoiceMessageParser(transcriber=transcriber),
        task_parser=SimpleTaskParser(),
        todoist=TodoistClient(config.todoist_token),
    )

    Bot(config, processor).run()


if __name__ == '__main__':
    main()
