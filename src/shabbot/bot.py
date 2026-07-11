import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

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

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processor.handle_text))
    app.add_handler(MessageHandler(filters.VOICE, processor.handle_voice))
    app.run_polling(drop_pending_updates=False, allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
