from datetime import date

import pytest

from shabbot.task_parser import SimpleTaskParser as DumbParser


class TestSimpleTaskParser:
    def test_summary(self) -> None:
        """parse() ставит summary равным тексту"""
        task = DumbParser().parse("Buy milk")
        assert task.summary == "Buy milk"

    def test_date_today(self) -> None:
        """parse() ставит date равным сегодняшней дате"""
        task = DumbParser().parse("anything")
        assert task.date == date.today()

    def test_raw_text_preserved(self) -> None:
        """parse() сохраняет исходный текст в raw_text"""
        text = "  Buy milk  "
        task = DumbParser().parse(text)
        assert task.raw_text == text

    def test_strips_whitespace_from_summary(self) -> None:
        """parse() обрезает пробелы в summary"""
        task = DumbParser().parse("  Buy milk  ")
        assert task.summary == "Buy milk"

    @pytest.mark.parametrize("text", ["", "   "])
    def test_empty_or_whitespace_input(self, text: str) -> None:
        """parse() не падает на пустой строке или строке из пробелов"""
        task = DumbParser().parse(text)
        assert task.summary == ""

    def test_optional_fields_default_none(self) -> None:
        """parse() оставляет description и location пустыми"""
        task = DumbParser().parse("Buy milk")
        assert task.description is None
        assert task.location is None
