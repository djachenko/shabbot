from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def create_files() -> Callable:
    def _create(root: Path, structure: dict) -> None:
        for key, value in structure.items():
            path = root / key

            if value is None:
                path.touch()
            elif isinstance(value, str):
                path.write_text(value, encoding="utf-8")
            elif isinstance(value, dict):
                path.mkdir(parents=True, exist_ok=True)
                _create(path, value)

    return _create
