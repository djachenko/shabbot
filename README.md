# shabbot

Telegram bot for capturing tasks with minimal friction. Send text or voice — task appears in Todoist, syncs to Google Calendar.

## How it works

- **Text message** → task in Todoist with due date = today
- **Voice message** → transcribed via Whisper → task in Todoist

## Requirements

- Python 3.11+
- [openai-whisper](https://github.com/openai/whisper) installed via pipx
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- Todoist API token from [Settings → Integrations → Developer](https://todoist.com/app/settings/integrations/developer)

## Run with Docker (recommended for servers)

```bash
cp docker.env.example docker.env
# fill in SHABBOT_TOKEN and TODOIST_TOKEN in docker.env
docker compose up -d
```

Whisper model weights (~1.5 GB) are cached in a named volume and survive container restarts.

To pre-download the model before the first voice message:

```bash
docker compose run --rm shabbot python -c "import whisper; whisper.load_model('large-v3-turbo')"
```

## Local setup

```bash
bash scripts/install.sh
```

The script installs Whisper, lets you pick a model, prompts for tokens, and saves config to `~/.config/shabbot/env`.

To install manually:

```bash
pipx install openai-whisper
pipx install -e .
shabbot  # prompts for tokens on first run
```

## Run locally

```bash
shabbot
```

Config is read from `~/.config/shabbot/env`. Optional overrides:

```
WHISPER_MODEL=large-v3-turbo
```

## Google Calendar sync

Tasks sync to Google Calendar via the native Todoist ↔ Google Calendar integration. To make all-day tasks (no time set) appear in the calendar, enable **Sync all-day tasks** in Todoist → Settings → Integrations → Google Calendar.
