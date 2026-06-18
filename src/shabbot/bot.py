import asyncio
import logging
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from telegram import Update
from telegram.error import TimedOut
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from shabbot.config import load_config
from shabbot.parser.base import DumbParser
from shabbot.todoist.client import create_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

WHISPER_BIN = "whisper"

parser = DumbParser()


async def transcribe_voice(update: Update, context: ContextTypes.DEFAULT_TYPE, whisper_model: str) -> str | None:
    assert update.message is not None
    voice = update.message.voice
    assert voice is not None
    file = await context.bot.get_file(voice.file_id)

    with TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)

        ogg_path = tmp / "voice.ogg"
        for attempt in range(3):
            try:
                await file.download_to_drive(ogg_path)
                break
            except TimedOut:
                if attempt == 2:
                    raise
                log.warning("download timed out, retrying (%d/3)", attempt + 1)
                await asyncio.sleep(2)

        result = subprocess.run(
            [WHISPER_BIN, ogg_path, "--model", whisper_model, "--language", "ru", "--output_format", "txt", "--output_dir", tmp],
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
    assert update.message is not None
    assert update.effective_user is not None
    log.info("text from %s: %r", update.effective_user.username, update.message.text)
    await _process(update, update.message.text or "")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    assert update.effective_user is not None
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
        text = await transcribe_voice(update, context, context.bot_data["whisper_model"])
    except TimedOut:
        pulse_task.cancel()
        log.error("timed out downloading voice file")
        await status.edit_text("❌ Таймаут при загрузке файла, попробуй ещё раз")
        return
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
    assert update.message is not None
    task = parser.parse(text)

    log.info("creating todoist task: %r", task.summary)
    result = create_task(task)
    log.info("created task id=%s", result.id)

    await update.message.reply_text(f"✅ Добавил: «{task.summary}»\nhttps://todoist.com/app/task/{result.id}")


def main() -> None:
    import argparse

    argparse.ArgumentParser(description="Telegram bot for capturing tasks to Todoist.").parse_known_args()

    config = load_config()

    app = ApplicationBuilder().token(config.shabbot_token).build()
    app.bot_data["whisper_model"] = config.whisper_model
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.run_polling(drop_pending_updates=False, allowed_updates=Update.ALL_TYPES)
