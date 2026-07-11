from abc import abstractmethod, ABC
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


class TaskParser(ABC):
    @abstractmethod
    def parse(self, text: str) -> Task:
        ...


class SimpleTaskParser(TaskParser):
    """Naive: весь текст → summary, date = today."""

    def parse(self, text: str) -> Task:
        return Task(
            summary=text.strip(),
            date=date.today(),
            raw_text=text,
        )
