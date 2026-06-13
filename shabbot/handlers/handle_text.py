import logging

from telegram import Update
from telegram.ext import ContextTypes

log = logging.getLogger(__name__)


async def extract_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    assert update.message is not None
    assert update.effective_user is not None

    log.info(f"text from {update.effective_user.username}: {update.message.text!r}")

    return update.message.text
