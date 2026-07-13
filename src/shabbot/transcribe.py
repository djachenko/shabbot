import asyncio
from pathlib import Path

from shabbot.loggable import Loggable

WHISPER_TIMEOUT = 300


class TranscriptionError(Exception):
    pass


class Transcriber(Loggable):
    def __init__(self, whisper_bin: str, whisper_model: str) -> None:
        self._whisper_bin = whisper_bin
        self._whisper_model = whisper_model

    async def transcribe(self, ogg_path: Path) -> str:
        proc = await asyncio.create_subprocess_exec(
            self._whisper_bin,
            str(ogg_path),
            "--model", self._whisper_model,
            "--language", "ru",
            "--output_format", "txt",
            "--output_dir", str(ogg_path.parent),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        self.logger.info("whisper pid=%d started", proc.pid)
        start_time = asyncio.get_event_loop().time()

        try:
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=WHISPER_TIMEOUT)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            self.logger.error("whisper timed out after %ds", WHISPER_TIMEOUT)
            raise TranscriptionError("whisper timed out")

        end_time = asyncio.get_event_loop().time()
        self.logger.info("whisper done in %.1fs", end_time - start_time)

        if proc.returncode != 0:
            self.logger.error("whisper error: %s", stderr.decode())
            raise TranscriptionError("whisper non-zero exit")

        txt_path = ogg_path.with_suffix(".txt")

        if not txt_path.exists():
            raise TranscriptionError("txt output not found")

        return txt_path.read_text(encoding="utf-8").strip()
