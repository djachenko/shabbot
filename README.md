# shabbot

Telegram bot for capturing tasks with minimal friction. Send text or voice — task appears in Todoist, syncs to Google Calendar.

## How it works

- **Text message** → task in Todoist with due date = today
- **Voice message** → transcribed via Whisper → task in Todoist

## Run with Docker (recommended for servers)

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) with Compose plugin.

```bash
git clone https://github.com/djachenko/shabbot.git
cd shabbot
bash scripts/docker.sh
```

The script picks a Whisper model, prompts for tokens, writes `docker.env`, and starts the bot.

Or manually:

```bash
cp docker.env.example docker.env  # fill in tokens
docker compose up -d
```

On first start the container downloads the Whisper model (~1.5 GB) before the bot comes online — this takes a few minutes. Subsequent starts are instant: the model is cached in a named Docker volume and survives container restarts and rebuilds.

```bash
docker compose logs -f   # view logs
docker compose down      # stop
docker compose restart   # restart
```

## Local setup

**Requirements:** Python 3.11+, [openai-whisper](https://github.com/openai/whisper) via pipx, Telegram bot token, Todoist API token.

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
