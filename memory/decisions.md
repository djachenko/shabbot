# decisions — Архитектурные решения capturebot

### Автозапуск: launchd, не Docker (пересмотрено 2026-06-09)
Docker перебор для личного инструмента на одной машине. launchd — нативный macOS, pipx install достаточно для изоляции. Переносимость на сервер не актуальна — бот работает локально на MacBook. Docker остаётся в списке как опция если понадобится развернуть где-то ещё.

### Whisper модель: large-v3-turbo
`large` маппится на `large-v3`, которого не было локально — whisper начинал скачивать 2.88 GB в runtime. `large-v3-turbo` уже был скачан (~1.5 GB), качество сопоставимо, быстрее.

### Polling, не webhook
Нет сервера с постоянным аптаймом. Telegram хранит непрочитанные сообщения и отдаёт при следующем polling — ничего не теряется пока MacBook выключен.

### Todoist, не Google Calendar напрямую
Todoist ↔ Google Calendar уже синхронизированы. Через Todoist API — один токен. Через Google Calendar API — OAuth consent screen, credentials.json, token refresh.

### DumbParser сейчас, BaseParser interface для будущего
Текст as-is → summary, date = today. Когда появится Ollama — создаётся OllamaParser(BaseParser), в bot.py меняется одна строка.

### PSR: версия читается из git тегов, не из pyproject.toml
`version_toml` говорит PSR только **куда писать** результат. Текущую версию PSR читает из последнего git тега. Без тега поведение непредсказуемо (может выдать 1.0.0 вместо 0.1.0). Чтобы PSR знал откуда считать — нужен начальный тег `v0.0.0` на первом коммите. Порядок работы PSR: читает последний тег → считает bump по коммитам → пишет новую версию в pyproject.toml → коммит + тег → push → build → publish.

### Будущее: dotfiles-репо + централизованная Claude memory
Идея: `~/dotfiles/` с симлинками на `~/.claude/`, `.gitconfig`, `.zshrc` и т.д. Claude memory хранится в `~/dotfiles/claude/memory/<project>/`, в каждом проекте симлинк `memory → ~/dotfiles/claude/memory/<project>`. Не делать пока не закончены текущие приоритеты.

### Два визарда: install.sh и config.py — не DRY, разные контексты
install.sh спрашивает модель whisper чтобы скачать её. config.py спрашивает токены и модель при первом запуске бота без конфига. Дублирование оправдано: разные цели (bootstrap среды vs runtime fallback), разные языки (bash vs python). Альтернатива — убрать промпты из config.py и сделать его fail-fast — отклонена: пользователь может поставить shabbot без install.sh если whisper уже есть.

### Безусловный save в load_config()
`config.save()` вызывается при каждом `load_config()`, не только когда что-то было запрошено. Перезапись при каждом старте — безвредна, зато убирает `needs_save` флаг и упрощает код.

### Handler pipeline: _make_handler + _catcher
Хэндлеры возвращают текст (`str | None`), `bot.py` владеет pipeline через `_make_handler(extractor, error_msg)`. `_catcher` — декоратор внутри `_make_handler`, применяется автоматически — не нужно помнить вешать на каждый новый хэндлер. View (статус-сообщения, пульс-анимация) пока остаётся в handle_voice — полное отделение View запланировано на будущее.

### TimedOut при скачивании голоса: retry 3 раза
Первый `TimedOut` = временный сбой сети, не ошибка пользователя. Retry 3 попытки с 2s паузой — после этого user-facing error. Не глотать молча (первый баг: сообщение просто пропадало без ответа).
