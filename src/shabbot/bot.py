import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from shabbot.config import load_config
from shabbot.message_parser import MessageParseError, TextMessageParser, VoiceMessageParser
from shabbot.processor import Processor
from shabbot.task_parser import SimpleTaskParser
from shabbot.todoist import TodoistClient, TodoistError
from shabbot.transcribe import Transcriber, TranscriptionError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> None:
    config = load_config()

    transcriber = Transcriber(
        whisper_bin=config.whisper_bin,
        whisper_model=config.whisper_model
    )

    processor = Processor(
        text_parser=TextMessageParser(),
        voice_parser=VoiceMessageParser(transcriber=transcriber),
        task_parser=SimpleTaskParser(),
        todoist=TodoistClient(config.todoist_token),
    )

    app = ApplicationBuilder() \
        .token(config.shabbot_token) \
        .concurrent_updates(True) \
        .build()

    logger = logging.getLogger(__name__)

    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.error("unhandled exception", exc_info=context.error)

        if not isinstance(update, Update) or update.effective_chat is None:
            return

        if isinstance(context.error, TranscriptionError):
            msg = "❌ не удалось распознать голос"
        elif isinstance(context.error, MessageParseError):
            msg = "❌ не удалось загрузить голосовое сообщение"
        elif isinstance(context.error, TodoistError):
            msg = "❌ не получилось добавить задачу"
        else:
            text = ""
            if update.effective_message:
                text = update.effective_message.text or update.effective_message.caption or ""
            suffix = ""
            if text:
                suffix = f". Текст был: {text}"
            msg = f"❌ не получилось{suffix}"

        await context.bot.send_message(update.effective_chat.id, msg)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processor.handle_text))
    app.add_handler(MessageHandler(filters.VOICE, processor.handle_voice))
    app.add_error_handler(error_handler)
    app.run_polling(drop_pending_updates=False, allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
