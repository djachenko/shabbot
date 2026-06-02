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

## Setup

```bash
pipx install -e .
```

Create a `shabbot.env` file:

```bash
export SHABBOT_TOKEN=your_telegram_bot_token
export TODOIST_TOKEN=your_todoist_api_token
export WHISPER_MODEL=large-v3-turbo  # optional, default: large
export WHISPER_BIN=~/.local/bin/whisper  # optional
```

## Run

```bash
source shabbot.env && shabbot
```

## Google Calendar sync

Tasks sync to Google Calendar via the native Todoist ↔ Google Calendar integration. To make all-day tasks (no time set) appear in the calendar, enable **Sync all-day tasks** in Todoist → Settings → Integrations → Google Calendar.
