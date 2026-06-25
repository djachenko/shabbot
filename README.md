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

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) with Compose plugin.

```bash
# 1. Clone the repo
git clone https://github.com/djachenko/shabbot.git
cd shabbot

# 2. Create env file and fill in your tokens
cp docker.env.example docker.env

# 3. Build and start
docker compose up -d
```

**docker.env:**
```
SHABBOT_TOKEN=<token from @BotFather>
TODOIST_TOKEN=<token from Todoist → Settings → Integrations → Developer>
WHISPER_MODEL=large-v3-turbo
```

On first start the container downloads the Whisper model (~1.5 GB) before the bot comes online — this takes a few minutes. Subsequent starts are instant: the model is cached in a named Docker volume and survives container restarts and rebuilds.

```bash
# View logs
docker compose logs -f

# Stop
docker compose down

# Restart
docker compose restart
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
