from datetime import date

from shabbot.parser.base import DumbParser


def test_dumb_parser_summary() -> None:
    parser = DumbParser()
    task = parser.parse("Buy milk")
    assert task.summary == "Buy milk"


def test_dumb_parser_date_today() -> None:
    parser = DumbParser()
    task = parser.parse("anything")
    assert task.date == date.today()
