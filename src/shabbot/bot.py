import asyncio
import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from telegram import Update
from telegram.error import TimedOut
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from shabbot.config import Config, load_config
from shabbot.parser.base import DumbParser
from shabbot.todoist.client import create_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

WHISPER_TIMEOUT = 300

parser = DumbParser()


async def transcribe_voice(update: Update, context: ContextTypes.DEFAULT_TYPE, config: Config) -> str | None:
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

        proc = await asyncio.create_subprocess_exec(
            config.whisper_bin,
            str(ogg_path),
            "--model", config.whisper_model,
            "--language", "ru",
            "--output_format", "txt",
            "--output_dir", str(tmp),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=WHISPER_TIMEOUT)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            log.error("whisper timed out after %ds", WHISPER_TIMEOUT)
            return None

        if proc.returncode != 0:
            log.error("whisper error: %s", stderr.decode())
            return None

        txt_path = tmp / "voice.txt"

        if not txt_path.exists():
            return None

        return txt_path.read_text(encoding="utf-8").strip()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    assert update.effective_user is not None
    log.info("text from %s: %r", update.effective_user.username, update.message.text)
    await _process(update, update.message.text or "", context.bot_data["config"])


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    assert update.effective_user is not None
    log.info("voice from %s", update.effective_user.username)
    status = await update.message.reply_text("🎙 Транскрибирую")
    config: Config = context.bot_data["config"]

    async def pulse() -> None:
        dots = 1
        while True:
            await asyncio.sleep(3)
            await status.edit_text("🎙 Транскрибирую" + "." * dots)
            dots = dots % 5 + 1

    pulse_task = asyncio.create_task(pulse())

    try:
        text = await transcribe_voice(update, context, config)
    except TimedOut:
        log.error("timed out downloading voice file")
        await status.edit_text("❌ Таймаут при загрузке файла, попробуй ещё раз")
        return
    finally:
        pulse_task.cancel()
        await asyncio.gather(pulse_task, return_exceptions=True)

    if text is None:
        await status.edit_text("❌ Не удалось распознать голос")
        return

    log.info("transcribed: %r", text)
    await status.edit_text(f"📝 Распознал: «{text}»")

    await _process(update, text, config)


async def _process(update: Update, text: str, config: Config) -> None:
    assert update.message is not None
    task = parser.parse(text)

    log.info("creating todoist task: %r", task.summary)
    result = await create_task(task, config.todoist_token)
    log.info("created task id=%s", result.id)

    await update.message.reply_text(f"✅ Добавил: «{task.summary}»\nhttps://todoist.com/app/task/{result.id}")


def main() -> None:
    config = load_config()

    app = ApplicationBuilder().token(config.shabbot_token).concurrent_updates(True).build()
    app.bot_data["config"] = config
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.run_polling(drop_pending_updates=False, allowed_updates=Update.ALL_TYPES)
