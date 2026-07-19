import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from telegram import Update, Message as TeleMessage
from telegram.error import TimedOut
from telegram.ext import ContextTypes

from shabbot.loggable import Loggable
from shabbot.transcribe import Transcriber, TranscriptionError


class MessageParseError(Exception):
    pass


@dataclass(frozen=True)
class Message:
    text: str


class MessageParser(ABC):
    @abstractmethod
    async def parse_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Message:
        pass


class TextMessageParser(MessageParser, Loggable):
    async def parse_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Message:
        assert update.message is not None
        assert update.effective_user is not None

        self.logger.info(
            "text from %s: %r", update.effective_user.username, update.message.text
        )

        return Message(update.message.text or "")


class VoiceMessageParserOutput:
    def __init__(self, update: Update) -> None:
        self._update = update
        self._status: TeleMessage | None = None
        self._pulse_count = 0

    async def transcribe_pulse(self) -> None:
        await self._send("🎙 Транскрибирую" + "." * self._pulse_count)

        self._pulse_count += 1
        self._pulse_count %= 5

    async def transcribe_success(self, text: str) -> None:
        await self._send(f"📝 Распознал: «{text}»")

    async def delete(self) -> None:
        if self._status is not None:
            await self._status.delete()

    async def _send(self, message: str) -> None:
        assert self._update.message is not None
        if self._status is None:
            self._status = await self._update.message.reply_text(message)
        else:
            await self._status.edit_text(message)


class VoiceMessageParser(MessageParser, Loggable):
    def __init__(self, transcriber: Transcriber) -> None:
        self._transcriber = transcriber

    async def parse_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Message:
        assert update.message is not None
        assert update.effective_user is not None
        assert update.message.voice is not None

        self.logger.info("voice from %s", update.effective_user.username)

        output = VoiceMessageParserOutput(update)

        async def pulse() -> None:
            while True:
                await output.transcribe_pulse()
                await asyncio.sleep(3)

        pulse_task = asyncio.create_task(pulse())

        try:
            text = await self._download_and_transcribe(update, context)
        except TimedOut as e:
            await output.delete()

            raise MessageParseError("download timed out") from e
        except TranscriptionError:
            await output.delete()

            raise
        finally:
            pulse_task.cancel()
            await asyncio.gather(pulse_task, return_exceptions=True)

        self.logger.info("transcribed: %r", text)
        await output.transcribe_success(text)

        return Message(text)

    async def _download_and_transcribe(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> str:
        assert update.message is not None
        assert update.message.voice is not None

        file = await context.bot.get_file(update.message.voice.file_id)

        with TemporaryDirectory() as tmp_dir:
            ogg_path = Path(tmp_dir) / "voice.ogg"

            for attempt in range(3):
                try:
                    await file.download_to_drive(ogg_path)
                    break
                except TimedOut:
                    if attempt == 2:
                        raise

                    self.logger.warning("download timed out, retrying (%d/3)", attempt + 1)
                    await asyncio.sleep(2 ** attempt)

            return await self._transcriber.transcribe(ogg_path)
