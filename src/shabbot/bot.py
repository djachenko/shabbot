import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from shabbot.config import load_config
from shabbot.message_parser import TextMessageParser, VoiceMessageParser
from shabbot.processor import Processor
from shabbot.task_parser import SimpleTaskParser
from shabbot.todoist import TodoistClient
from shabbot.transcribe import Transcriber

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

    allowed = filters.Chat(chat_id=config.allowed_chat_id)

    async def _reject(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_message:
            await update.effective_message.reply_text("🚫")

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & allowed, processor.handle_text))
    app.add_handler(MessageHandler(filters.VOICE & allowed, processor.handle_voice))
    app.add_handler(MessageHandler(filters.ALL & ~allowed, _reject))
    app.run_polling(drop_pending_updates=False, allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
