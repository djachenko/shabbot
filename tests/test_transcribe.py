import asyncio
from pathlib import Path
from typing import Callable
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from shabbot.transcribe import Transcriber, TranscriptionError


def _mock_proc(returncode: int = 0, stderr: bytes = b"") -> MagicMock:
    proc = MagicMock()
    proc.pid = 12345
    proc.returncode = returncode
    proc.communicate = AsyncMock(return_value=(b"", stderr))
    proc.kill = MagicMock()
    proc.wait = AsyncMock()

    return proc


@pytest.fixture
def transcriber() -> Transcriber:
    return Transcriber(whisper_bin="whisper", whisper_model="tiny")


class TestTranscriber:
    @pytest.mark.anyio
    async def test_returns_txt_content(self, transcriber: Transcriber, tmp_path: Path, create_files: Callable) -> None:
        """transcribe() возвращает содержимое .txt файла"""
        create_files(tmp_path, {"voice.ogg": None, "voice.txt": "Привет мир"})
        ogg = tmp_path / "voice.ogg"

        with patch("asyncio.create_subprocess_exec", AsyncMock(return_value=_mock_proc())):
            result = await transcriber.transcribe(ogg)

        assert result == "Привет мир"

    @pytest.mark.anyio
    async def test_strips_whitespace(self, transcriber: Transcriber, tmp_path: Path, create_files: Callable) -> None:
        """transcribe() убирает пробелы и переносы строк вокруг текста"""
        create_files(tmp_path, {"voice.ogg": None, "voice.txt": "  hello  \n"})
        ogg = tmp_path / "voice.ogg"

        with patch("asyncio.create_subprocess_exec", AsyncMock(return_value=_mock_proc())):
            result = await transcriber.transcribe(ogg)

        assert result == "hello"

    @pytest.mark.anyio
    async def test_calls_whisper_with_correct_args(self, transcriber: Transcriber, tmp_path: Path, create_files: Callable) -> None:
        """transcribe() передаёт правильные аргументы и модель в whisper"""
        create_files(tmp_path, {"voice.ogg": None, "voice.txt": "text"})
        ogg = tmp_path / "voice.ogg"

        mock_exec = AsyncMock(return_value=_mock_proc())
        with patch("asyncio.create_subprocess_exec", mock_exec):
            await transcriber.transcribe(ogg)

        args = mock_exec.call_args[0]
        assert args[0] == "whisper"
        assert str(ogg) in args
        assert "--model" in args
        assert "tiny" in args
        assert "--language" in args
        assert "ru" in args


class TestTranscriberFailures:
    @pytest.mark.anyio
    async def test_timeout_raises(self, transcriber: Transcriber, tmp_path: Path, create_files: Callable) -> None:
        """transcribe() бросает TranscriptionError с сообщением о таймауте"""
        create_files(tmp_path, {"voice.ogg": None})
        ogg = tmp_path / "voice.ogg"

        proc = MagicMock()
        proc.pid = 12345
        proc.communicate = MagicMock()  # не AsyncMock — coroutine не создаётся до wait_for
        proc.kill = MagicMock()
        proc.wait = AsyncMock()

        with patch("asyncio.create_subprocess_exec", AsyncMock(return_value=proc)):
            with patch("asyncio.wait_for", AsyncMock(side_effect=asyncio.TimeoutError)):
                with pytest.raises(TranscriptionError, match=TranscriptionError.TIMEOUT):
                    await transcriber.transcribe(ogg)

    @pytest.mark.anyio
    async def test_nonzero_exit_raises(self, transcriber: Transcriber, tmp_path: Path, create_files: Callable) -> None:
        """transcribe() бросает TranscriptionError с сообщением о ненулевом коде"""
        create_files(tmp_path, {"voice.ogg": None})
        ogg = tmp_path / "voice.ogg"

        with patch("asyncio.create_subprocess_exec", AsyncMock(return_value=_mock_proc(returncode=1, stderr=b"error"))):
            with pytest.raises(TranscriptionError, match=TranscriptionError.NONZERO_EXIT):
                await transcriber.transcribe(ogg)

    @pytest.mark.anyio
    async def test_missing_txt_raises(self, transcriber: Transcriber, tmp_path: Path, create_files: Callable) -> None:
        """transcribe() бросает TranscriptionError если whisper не создал .txt"""
        create_files(tmp_path, {"voice.ogg": None})
        ogg = tmp_path / "voice.ogg"

        with patch("asyncio.create_subprocess_exec", AsyncMock(return_value=_mock_proc())):
            with pytest.raises(TranscriptionError, match=TranscriptionError.MISSING_TXT):
                await transcriber.transcribe(ogg)
