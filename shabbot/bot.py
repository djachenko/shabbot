import logging
from collections.abc import Coroutine
from functools import wraps
from typing import Any, Callable

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from shabbot.config import load_config
import shabbot.handlers.handle_text as handle_text
import shabbot.handlers.handle_voice as handle_voice
from shabbot.parser.base import DumbParser
from shabbot.todoist.client import create_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

parser = DumbParser()

Handler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]]
Extractor = Callable[[Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, str | None]]


def _catcher(func: Handler) -> Handler:
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assert update.message is not None

        try:
            await func(update, context)
        except Exception:
            log.exception(f"unhandled error in {func.__name__}")

            await update.message.reply_text("❌ Не удалось создать задачу")

    return wrapper


async def _process(update: Update, text: str) -> None:
    assert update.message is not None
    task = parser.parse(text)

    log.info(f"creating todoist task: {task.summary!r}")
    result = create_task(task)
    log.info(f"created task id={result.id}")

    await update.message.reply_text(f"✅ Добавил: «{task.summary}»\nhttps://todoist.com/app/task/{result.id}")


def _make_handler(extractor: Extractor, error: str) -> Handler:
    @_catcher
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = await extractor(update, context)

        if text:
            await _process(update, text)
        else:
            await update.message.reply_text(error)  # type: ignore[union-attr]

    return handler


_on_text = _make_handler(handle_text.extract_text, "❌ Пустое сообщение")
_on_voice = _make_handler(handle_voice.extract_text, "❌ Не удалось распознать голос")


def main() -> None:
    import argparse

    argparse.ArgumentParser(description="Telegram bot for capturing tasks to Todoist.").parse_known_args()

    config = load_config()

    app = ApplicationBuilder().token(config.shabbot_token).build()
    app.bot_data["whisper_model"] = config.whisper_model
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _on_text))
    app.add_handler(MessageHandler(filters.VOICE, _on_voice))
    app.run_polling()
