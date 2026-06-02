# shabbot

Telegram-бот для захвата задач голосом и текстом → Todoist → Google Calendar.

## Git

Commits и ветки — Conventional Commits:
`feat:`, `fix:`, `refactor:`, `chore:`, `style:`, `test:`, `docs:`

Ветки называть так же: `feat/llm-parser`, `fix/whisper-timeout`, `refactor/todoist-client`.

## Stack

- Python 3.11+, pipx
- python-telegram-bot, todoist-api-python, openai-whisper
- Переменные окружения через `shabbot.env` (не в репо)

## Запуск

```bash
source shabbot.env && shabbot
```
