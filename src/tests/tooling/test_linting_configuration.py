import json
import subprocess
from pathlib import Path

import pytest

SOURCE_ROOT = Path(__file__).resolve().parents[2]


class TestRuffConfiguration:
    @pytest.mark.parametrize(
        "relative_import",
        [
            "from . import recipe",
            "from .recipe import build as recipe",
            "from ..domain import recipe",
            "from ..domain.recipe import build as recipe",
        ],
    )
    def test_rejects_relative_imports_in_a_source_file(
        self, relative_import: str
    ) -> None:
        source = f"{relative_import}\n\nvalue = recipe\n"

        codes = self.violation_codes(source)

        assert codes == ["TID252"]

    def test_accepts_absolute_imports_in_a_source_file(self) -> None:
        source = "from my_cookbook.recipes.domain import recipe\n\nvalue = recipe\n"

        codes = self.violation_codes(source)

        assert codes == []

    @staticmethod
    def violation_codes(source: str) -> list[str]:
        filename = SOURCE_ROOT / "my_cookbook" / "recipes" / "domain" / "module.py"
        result = subprocess.run(
            [
                "ruff",
                "check",
                "--output-format",
                "json",
                "--stdin-filename",
                str(filename),
                "-",
            ],
            input=source,
            capture_output=True,
            text=True,
            check=False,
        )
        return [violation["code"] for violation in json.loads(result.stdout)]


class TestMypyConfiguration:
    def test_reports_a_function_without_annotations_because_mypy_runs_strict(
        self,
    ) -> None:
        source = "def identity(value):\n    return value\n"

        result = subprocess.run(
            ["mypy", "--no-incremental", "--output", "json", "-c", source],
            capture_output=True,
            text=True,
            cwd=SOURCE_ROOT,
            check=False,
        )

        codes = [
            json.loads(line)["code"]
            for line in result.stdout.splitlines()
            if line.startswith("{")
        ]
        assert codes == ["no-untyped-def"]
