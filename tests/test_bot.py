import asyncio
from unittest.mock import AsyncMock, MagicMock

from shabbot.bot import Bot


def _make_bot() -> Bot:
    return Bot(config=MagicMock(), processor=MagicMock())


class TestReject:
    def test_replies_with_ban_emoji(self) -> None:
        message = AsyncMock()
        update = MagicMock()
        update.effective_message = message

        asyncio.run(_make_bot()._reject(update, MagicMock()))

        message.reply_text.assert_called_once_with("🚫")

    def test_no_reply_without_message(self) -> None:
        update = MagicMock()
        update.effective_message = None

        asyncio.run(_make_bot()._reject(update, MagicMock()))
