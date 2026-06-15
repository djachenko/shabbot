from abc import ABC, abstractmethod
from datetime import date

from shabbot.task import Task


class BaseParser(ABC):
    @abstractmethod
    def parse(self, text: str) -> Task: ...


class DumbParser(BaseParser):
    """Naive: весь текст → summary, date = today."""

    def parse(self, text: str) -> Task:
        return Task(
            summary=text.strip(),
            date=date.today(),
            raw_text=text,
        )
