import os
from pathlib import Path

from dotenv import load_dotenv


def _prompt_for_token(name: str, description: str) -> str:
    print(f"\n{description}")
    print(f"Get it from: {_get_token_source(name)}")
    value = input(f"Enter {name}: ").strip()
    if not value:
        raise ValueError(f"{name} cannot be empty")
    return value


def _get_token_source(name: str) -> str:
    sources = {
        "SHABBOT_TOKEN": "https://t.me/BotFather (create/edit your bot)",
        "TODOIST_TOKEN": "https://todoist.com/app/settings/integrations/developer",
    }
    return sources.get(name, "your service settings")


def load_config() -> dict[str, str]:
    """Load environment config from .env file or prompt user."""
    env_file = Path("shabbot.env")

    # Try loading from .env file if it exists
    if env_file.exists():
        load_dotenv(env_file)

    # Check if required tokens are available
    shabbot_token = os.environ.get("SHABBOT_TOKEN")
    todoist_token = os.environ.get("TODOIST_TOKEN")

    # Only prompt and save if .env doesn't exist
    env_file_existed = env_file.exists()

    # Prompt for missing tokens
    if not shabbot_token:
        shabbot_token = _prompt_for_token(
            "SHABBOT_TOKEN",
            "Telegram bot token is required to run shabbot.",
        )
        os.environ["SHABBOT_TOKEN"] = shabbot_token

    if not todoist_token:
        todoist_token = _prompt_for_token(
            "TODOIST_TOKEN",
            "Todoist API token is required to create tasks.",
        )
        os.environ["TODOIST_TOKEN"] = todoist_token

    # Offer to save only if .env didn't exist before
    if not env_file_existed and shabbot_token and todoist_token:
        save = input("\nSave configuration to shabbot.env? (y/n): ").strip().lower()
        if save == "y":
            with open(env_file, "w") as f:
                f.write(f"export SHABBOT_TOKEN={shabbot_token}\n")
                f.write(f"export TODOIST_TOKEN={todoist_token}\n")
            print(f"✓ Saved to {env_file}")

    return {
        "SHABBOT_TOKEN": os.environ["SHABBOT_TOKEN"],
        "TODOIST_TOKEN": os.environ["TODOIST_TOKEN"],
    }
