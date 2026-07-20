import asyncio
from unittest.mock import AsyncMock, MagicMock

from shabbot.bot import reject


class TestReject:
    def test_replies_with_ban_emoji(self) -> None:
        message = AsyncMock()
        update = MagicMock()
        update.effective_message = message

        asyncio.run(reject(update, MagicMock()))

        message.reply_text.assert_called_once_with("🚫")

    def test_no_reply_without_message(self) -> None:
        update = MagicMock()
        update.effective_message = None

        asyncio.run(reject(update, MagicMock()))
