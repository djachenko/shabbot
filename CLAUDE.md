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
- `WHISPER_MODEL` — модель (default: `large`)
- `WHISPER_BIN` — путь к whisper (default: `~/.local/bin/whisper`)

---

## Текущее состояние

- Базовая функциональность работает
- 1 незакоммиченный файл (`bot.py`) — активная доработка
- Ещё не зарелизен

---

## Что нужно сделать

1. **Зарелизить**: оформить как нормальный релиз (версия, changelog)
2. **Docker**: упаковать в контейнер чтобы запускать на сервере без зависимостей от локальной среды
3. Возможно: LLM-парсер для естественного языка в дату (`parser/base.py` — уже есть заготовка `DumbParser`)

---

## Git

Semantic commits: `feat:`, `fix:`, `refactor:`, `chore:`  
Ветки: `feat/llm-parser`, `fix/whisper-timeout`, `refactor/todoist-client`
