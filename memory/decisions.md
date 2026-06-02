# decisions — Архитектурные решения capturebot

### Автозапуск: Docker, не launchd
launchd — лишняя сложность для одного процесса без сервера. Docker даёт изоляцию и переносимость, проще перенести на сервер если понадобится.

### Whisper модель: large-v3-turbo
`large` маппится на `large-v3`, которого не было локально — whisper начинал скачивать 2.88 GB в runtime. `large-v3-turbo` уже был скачан (~1.5 GB), качество сопоставимо, быстрее.

### Polling, не webhook
Нет сервера с постоянным аптаймом. Telegram хранит непрочитанные сообщения и отдаёт при следующем polling — ничего не теряется пока MacBook выключен.

### Todoist, не Google Calendar напрямую
Todoist ↔ Google Calendar уже синхронизированы. Через Todoist API — один токен. Через Google Calendar API — OAuth consent screen, credentials.json, token refresh.

### DumbParser сейчас, BaseParser interface для будущего
Текст as-is → summary, date = today. Когда появится Ollama — создаётся OllamaParser(BaseParser), в bot.py меняется одна строка.
