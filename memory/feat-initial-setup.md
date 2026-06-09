# feat-initial-setup — Бот shabbot готов к использованию, незакоммиченные правки в bot.py

<!-- Telegram-бот shabbot установлен через pipx, текстовые и голосовые сообщения создают задачи в Todoist. -->

### 2026-06-09 — Переименование, retry на таймаут, язык whisper, git history

Проект переименован capturebot → shabbot. В `bot.py` добавлены: retry при `TimedOut` во время загрузки голосового файла (3 попытки, 2s задержка, потом user-facing error), флаг `--language ru` для whisper (по умолчанию определял украинский), pathlib вместо строк для путей, восстановлен `~filters.COMMAND` фильтр. В `client.py` рефактор: `description or None` заменён на `parts: list[str]`. Создан git-репо с semantic commits, README, CLAUDE.md с конвенциями. **Остаток: `shabbot/bot.py` ещё не закоммичен** (retry + language + pathlib).

### 2026-06-03 — Первый запуск capturebot, отладка, проверка голоса

Создана вся структура проекта (capturebot/bot.py, parser/base.py, todoist/client.py, pyproject.toml) и установлена через `pipx install -e .`. Токены хранятся в `shabbot.env` с `export` — без этого дочерние процессы не видят переменные. Бот запускается командой `pkill -f capturebot; source shabbot.env && capturebot` (точка с запятой перед source обязательна — pkill возвращает 1 если процесс не найден, и `&&` обрывает цепь). Голосовые сообщения транскрибируются через whisper, модель `large-v3-turbo` (~1.5 GB, уже была скачана); `large` маппится на `large-v3` которого не было и он начинал скачиваться. Добавлен pulse-индикатор в Telegram пока whisper думает. Задачи без времени не появляются в Google Calendar по умолчанию — нужно включить "Sync all-day tasks" в Todoist → Settings → Integrations → Google Calendar.

#### Что осталось
- Автозапуск (решено делать через Docker, не launchd)
- LLM-парсер для извлечения даты/локации из текста (Ollama, когда появится Mac Mini)
- Метки/проекты Todoist — накопить задачи, потом разметить
