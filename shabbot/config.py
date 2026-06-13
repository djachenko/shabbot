import getpass
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

CONFIG_DIR = Path.home() / ".config" / "shabbot"
CONFIG_FILE = CONFIG_DIR / "env"

DEFAULT_WHISPER_MODEL = "large-v3-turbo"


@dataclass(frozen=True)
class Config:
    shabbot_token: str
    todoist_token: str
    whisper_model: str

    def save(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        with open(CONFIG_FILE, "w") as f:
            f.write(f"SHABBOT_TOKEN={self.shabbot_token}\n")
            f.write(f"TODOIST_TOKEN={self.todoist_token}\n")
            f.write(f"WHISPER_MODEL={self.whisper_model}\n")

        CONFIG_FILE.chmod(0o600)


def _prompt_secret(name: str, hint: str) -> str:
    print(f"\n{name}: {hint}")

    value = getpass.getpass(f"{name}: ").strip()

    if not value:
        raise ValueError(f"{name} cannot be empty")

    return value


def _prompt_model() -> str:
    value = input(f"\nWhisper model [{DEFAULT_WHISPER_MODEL}]: ").strip()

    return value or DEFAULT_WHISPER_MODEL


def load_config() -> Config:
    if CONFIG_FILE.exists():
        load_dotenv(CONFIG_FILE)

    shabbot_token = os.environ.get("SHABBOT_TOKEN") or _prompt_secret(
        "SHABBOT_TOKEN",
        "https://t.me/BotFather",
    )

    todoist_token = os.environ.get("TODOIST_TOKEN") or _prompt_secret(
        "TODOIST_TOKEN",
        "https://todoist.com/app/settings/integrations/developer",
    )

    whisper_model = os.environ.get("WHISPER_MODEL") or _prompt_model()

    config = Config(
        shabbot_token=shabbot_token,
        todoist_token=todoist_token,
        whisper_model=whisper_model,
    )

    config.save()

    return config
