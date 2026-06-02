import asyncio
import logging
import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from shabbot.parser.base import DumbParser
from shabbot.todoist.client import create_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

WHISPER_BIN = Path(os.environ.get("WHISPER_BIN", "~/.local/bin/whisper")).expanduser()
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "large")

parser = DumbParser()


async def transcribe_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)

    with TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)

        ogg_path = tmp / "voice.ogg"
        await file.download_to_drive(ogg_path)

        result = subprocess.run(
            [WHISPER_BIN, ogg_path, "--model", WHISPER_MODEL, "--output_format", "txt", "--output_dir", tmp],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            log.error("whisper error: %s", result.stderr)

            return None

        txt_path = tmp / "voice.txt"

        if not txt_path.exists():
            return None

        return txt_path.read_text().strip()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.info("text from %s: %r", update.effective_user.username, update.message.text)
    await _process(update, update.message.text)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.info("voice from %s", update.effective_user.username)
    status = await update.message.reply_text("🎙 Транскрибирую")

    async def pulse() -> None:
        dots = 1

        while True:
            await asyncio.sleep(3)
            await status.edit_text("🎙 Транскрибирую" + "." * dots)

            dots = dots % 5 + 1

    pulse_task = asyncio.create_task(pulse())

    try:
        text = await transcribe_voice(update, context)
    finally:
        pulse_task.cancel()

    if not text:
        log.error("whisper returned empty result")
        await status.edit_text("❌ Не удалось распознать голос")

        return

    log.info("transcribed: %r", text)
    await status.edit_text(f"📝 Распознал: «{text}»")

    await _process(update, text)


async def _process(update: Update, text: str) -> None:
    task = parser.parse(text)

    log.info("creating todoist task: %r", task.summary)
    result = create_task(task)
    log.info("created task id=%s", result.id)

    await update.message.reply_text(f"✅ Добавил: «{task.summary}»\nhttps://todoist.com/app/task/{result.id}")


def main() -> None:
    app = ApplicationBuilder().token(os.environ["SHABBOT_TOKEN"]).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.run_polling()
