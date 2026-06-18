# shabbot — Project Guide

## Что это

Telegram-бот для захвата задач с минимальным трением. Отправляешь текст или голос — задача появляется в Todoist, синхронизируется в Google Calendar.

Личный инструмент продуктивности, не связан с фотопайплайном.

---

## Как работает

- **Текст** → задача в Todoist с due date = сегодня
- **Голос** → транскрипция через Whisper → задача в Todoist

---

## Стек

- Python 3.11+, `python-telegram-bot`, `todoist-api-python`
- Whisper (openai-whisper) — запускается как внешний процесс через subprocess
- Переменные окружения через `shabbot.env` (не в репо)

---

## Запуск

```bash
source shabbot.env && shabbot
```

Переменные:
- `SHABBOT_TOKEN` — Telegram bot token
- `TODOIST_TOKEN` — Todoist API token
- `WHISPER_MODEL` — модель (default: `large-v3-turbo`)
- `WHISPER_BIN` — путь к whisper (default: `whisper`)

---

## Текущее состояние

- Релиз v0.3.0, src layout (`src/shabbot/`)
- CI + PSR автоматически выпускают версии при мерже в master

---

## Что нужно сделать

1. **Docker**: упаковать в контейнер чтобы запускать на сервере без зависимостей от локальной среды
2. Возможно: LLM-парсер для естественного языка в дату (`src/shabbot/parser/base.py` — заготовка `BaseParser` + `DumbParser` есть)

---

## Git

Semantic commits: `feat:`, `fix:`, `refactor:`, `chore:`  
Ветки: `feat/llm-parser`, `fix/whisper-timeout`, `refactor/todoist-client`
