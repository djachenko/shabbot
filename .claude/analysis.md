# shabbot — Технический анализ и рекомендации

> Дата: 2026-06-05. Полное чтение исходников.

---

## Архитектура

```
Telegram Update
    ↓
bot.py (handlers)
    ├── text → DumbParser → create_task() → Todoist
    └── voice → download OGG → Whisper (subprocess) → DumbParser → create_task()
```

**Task dataclass** (`task.py`):
```python
@dataclass
class Task:
    summary: str
    date: date
    description: str | None
    location: str | None
    reminder_minutes: int | None
    raw_text: str
```

**DumbParser** — заглушка: весь текст как summary, дата = сегодня. `BaseParser` абстрактный класс существует, но только один наследник.

---

## Проблемы

### 1. Parser — это placeholder
`DumbParser` не парсит вообще ничего. Фраза "встреча в среду в 3" → summary="встреча в среду в 3", date=сегодня. Google Calendar синхронизация бесполезна без дат.

**Следующий шаг:** LLM-парсер. Архитектура (`BaseParser`) уже готова для подключения.

Вариант реализации:
```python
class LLMParser(BaseParser):
    def parse(self, text: str) -> Task:
        # Claude API: structured output с date/summary/location
        ...
```

### 2. Whisper — хрупкий subprocess
```python
result = subprocess.run([WHISPER_BIN, ogg_path, "--model", WHISPER_MODEL, ...])
```
- Нет обработки отсутствия бинарника
- Нет обработки timeout кроме Telegram download
- Модель `large` — тяжёлая, медленно работает без GPU

**Варианты улучшения:**
- Проверять наличие `WHISPER_BIN` при старте
- Добавить timeout для subprocess
- Рассмотреть OpenAI Whisper API вместо локального (проще в Docker)

### 3. Нет обработки ошибок Todoist API
`create_task()` не оборачивается в try/except. При сетевой ошибке бот молчит и не отвечает пользователю.

### 4. Нет тестов
Parser, todoist client, task dataclass — всё легко тестируемо, но тестов нет.

---

## Релиз + Docker (план)

### 1. Зарелизить
```bash
# pyproject.toml уже готов
# Добавить [tool.bumpversion]
# Добавить GitHub Release
```

### 2. Dockerfile
```dockerfile
FROM python:3.11-slim

# Whisper зависимости
RUN apt-get install -y ffmpeg

# Whisper
RUN pip install openai-whisper

# shabbot
COPY . /app
RUN pip install /app

CMD ["shabbot"]
```

### 3. docker-compose.yml
```yaml
services:
  shabbot:
    build: .
    env_file: shabbot.env
    restart: unless-stopped
```

**Проблема с Whisper в Docker:** модель `large` = 3GB, нужен volume для кэша:
```yaml
    volumes:
      - whisper-cache:/root/.cache/whisper
```

Альтернатива: использовать OpenAI Whisper API — нет локального бинарника, нет GPU, проще Docker-образ.

---

## LLM-парсер (идея)

```python
class LLMParser(BaseParser):
    """Парсит естественный язык через Claude API с structured output."""
    
    def parse(self, text: str) -> Task:
        # Prompt: "Извлеки задачу: дату, время, суть, место"
        # Response: JSON с полями Task
        # Fallback: date=today если дата не найдена
```

Это закроет главный gap — Google Calendar синхронизация станет полезной.

---

## Итог по приоритетам

1. **Сейчас:** дорелизить (pyproject.toml, версия, CHANGELOG)
2. **Потом:** Docker (Dockerfile + compose)
3. **После:** LLM-парсер (значительно увеличит полезность)
4. **Всегда:** error handling в Todoist client
