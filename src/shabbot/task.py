from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    summary: str
    date: date
    description: str | None = None
    location: str | None = None
    reminder_minutes: int = 30
    raw_text: str | None = None
