import asyncio
import logging
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from telegram import Update
from telegram.error import TimedOut
from telegram.ext import ContextTypes

log = logging.getLogger(__name__)

WHISPER_BIN = "whisper"


async def extract_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    assert update.message is not None
    assert update.effective_user is not None

    log.info(f"voice from {update.effective_user.username}")

    status = await update.message.reply_text("🎙 Транскрибирую")

    async def pulse() -> None:
        dots = 1
        while True:
            await asyncio.sleep(3)
            await status.edit_text("🎙 Транскрибирую" + "." * dots)
            dots = dots % 5 + 1

    pulse_task = asyncio.create_task(pulse())

    try:
        text = await _transcribe(update, context)
    except TimedOut:
        log.error("timed out downloading voice file")
        await status.delete()
        return None
    finally:
        pulse_task.cancel()

    if not text:
        log.error("whisper returned empty result")
        await status.delete()
        return None

    log.info(f"transcribed: {text!r}")
    await status.edit_text(f"📝 Распознал: «{text}»")

    return text


async def _transcribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    assert update.message is not None

    voice = update.message.voice
    assert voice is not None

    file = await context.bot.get_file(voice.file_id)
    whisper_model = context.bot_data["whisper_model"]

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
                log.warning(f"download timed out, retrying ({attempt + 1}/3)")
                await asyncio.sleep(2)

        result = subprocess.run(
            [WHISPER_BIN, ogg_path, "--model", whisper_model, "--language", "ru", "--output_format", "txt", "--output_dir", tmp],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            log.error(f"whisper error: {result.stderr}")
            return None

        txt_path = tmp / "voice.txt"

        if not txt_path.exists():
            return None

        return txt_path.read_text().strip()
