import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from shabbot.config import Config, DEFAULT_WHISPER_MODEL, load_config


@pytest.fixture
def env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHABBOT_TOKEN", "tg-token")
    monkeypatch.setenv("TODOIST_TOKEN", "td-token")
    monkeypatch.setenv("ALLOWED_CHAT_ID", "123456")
    monkeypatch.setenv("WHISPER_MODEL", "tiny")
    monkeypatch.setenv("WHISPER_BIN", "/usr/bin/whisper")


class TestLoadConfig:
    def test_reads_all_env_vars(self, env_vars: None, tmp_path: Path) -> None:
        with patch("shabbot.config.CONFIG_DIR", tmp_path), \
             patch("shabbot.config.CONFIG_FILE", tmp_path / "env"):
            config = load_config()

        assert config.shabbot_token == "tg-token"
        assert config.todoist_token == "td-token"
        assert config.allowed_chat_id == 123456
        assert config.whisper_model == "tiny"
        assert config.whisper_bin == "/usr/bin/whisper"

    def test_default_whisper_bin(self, env_vars: None, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.delenv("WHISPER_BIN", raising=False)

        with patch("shabbot.config.CONFIG_DIR", tmp_path), \
             patch("shabbot.config.CONFIG_FILE", tmp_path / "env"):
            config = load_config()

        assert config.whisper_bin == "whisper"


class TestConfigSave:
    def test_writes_env_file(self, tmp_path: Path) -> None:
        config = Config(
            shabbot_token="tg-token",
            todoist_token="td-token",
            allowed_chat_id=123456,
            whisper_model="tiny",
        )

        with patch("shabbot.config.CONFIG_DIR", tmp_path), \
             patch("shabbot.config.CONFIG_FILE", tmp_path / "env"):
            config.save()

        content = (tmp_path / "env").read_text()
        assert "SHABBOT_TOKEN=tg-token" in content
        assert "TODOIST_TOKEN=td-token" in content
        assert "ALLOWED_CHAT_ID=123456" in content
        assert "WHISPER_MODEL=tiny" in content

    @pytest.mark.skipif(sys.platform == "win32", reason="chmod 600 is Unix-only")
    def test_file_permissions(self, tmp_path: Path) -> None:
        config = Config(
            shabbot_token="x",
            todoist_token="x",
            allowed_chat_id=1,
            whisper_model="tiny",
        )

        env_file = tmp_path / "env"
        with patch("shabbot.config.CONFIG_DIR", tmp_path), \
             patch("shabbot.config.CONFIG_FILE", env_file):
            config.save()

        mode = oct(env_file.stat().st_mode & 0o777)
        assert mode == oct(0o600)


class TestDefaultWhisperModel:
    def test_default_model_value(self) -> None:
        assert DEFAULT_WHISPER_MODEL == "large-v3-turbo"
