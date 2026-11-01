import os
import re
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.exc import OperationalError

from my_cookbook.recipes.tests.infrastructure.alembic_locations import (
    ALEMBIC_INI,
    MIGRATIONS_FOLDER,
    REPOSITORY_ROOT,
)

CREDENTIALS_IN_URL: re.Pattern[str] = re.compile(r"://[^/\s]*:[^/\s]*@")


class TestMigrationConnection:
    @pytest.fixture(autouse=True)
    def restored_schema(self) -> Iterator[None]:
        yield
        command.upgrade(Config(str(ALEMBIC_INI)), "head")

    @pytest.mark.parametrize(
        ("variable", "wrong_value"),
        [
            ("PG_USER", "unknown_user"),
            ("PG_PASSWORD", "wrong_password"),
            ("PG_HOST", "unreachable.invalid"),
            ("PG_DB", "unknown_database"),
        ],
    )
    def test_takes_each_part_of_the_connection_from_the_environment(
        self, monkeypatch: pytest.MonkeyPatch, variable: str, wrong_value: str
    ) -> None:
        monkeypatch.setenv(variable, wrong_value)

        with pytest.raises(OperationalError):
            command.upgrade(Config(str(ALEMBIC_INI)), "head")

    def test_keeps_literal_credentials_out_of_the_alembic_configuration(self) -> None:
        files_with_credentials = [
            path.relative_to(REPOSITORY_ROOT)
            for path in self.configuration_files()
            if self.contains_credentials(path.read_text())
        ]

        assert files_with_credentials == []

    @staticmethod
    def configuration_files() -> list[Path]:
        return [
            ALEMBIC_INI,
            *(
                path
                for path in MIGRATIONS_FOLDER.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            ),
        ]

    @staticmethod
    def contains_credentials(content: str) -> bool:
        return (
            os.environ["PG_PASSWORD"] in content
            or "sqlalchemy.url" in content
            or CREDENTIALS_IN_URL.search(content) is not None
        )
