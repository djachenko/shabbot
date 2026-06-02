# feat-initial-setup — Бот запущен, proof of concept работает

<!-- Telegram-бот capturebot установлен через pipx, текстовые и голосовые сообщения создают задачи в Todoist. -->

### 2026-06-03 — Первый запуск capturebot, отладка, проверка голоса

Создана вся структура проекта (capturebot/bot.py, parser/base.py, todoist/client.py, pyproject.toml) и установлена через `pipx install -e .`. Токены хранятся в `shabbot.env` с `export` — без этого дочерние процессы не видят переменные. Бот запускается командой `pkill -f capturebot; source shabbot.env && capturebot` (точка с запятой перед source обязательна — pkill возвращает 1 если процесс не найден, и `&&` обрывает цепь). Голосовые сообщения транскрибируются через whisper, модель `large-v3-turbo` (~1.5 GB, уже была скачана); `large` маппится на `large-v3` которого не было и он начинал скачиваться. Добавлен pulse-индикатор в Telegram пока whisper думает. Задачи без времени не появляются в Google Calendar по умолчанию — нужно включить "Sync all-day tasks" в Todoist → Settings → Integrations → Google Calendar.

#### Что осталось
- Автозапуск (решено делать через Docker, не launchd)
- LLM-парсер для извлечения даты/локации из текста (Ollama, когда появится Mac Mini)
- Метки/проекты Todoist — накопить задачи, потом разметить
