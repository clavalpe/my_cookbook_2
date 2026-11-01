from pathlib import Path

REPOSITORY_ROOT: Path = Path(__file__).parents[5]
ALEMBIC_INI: Path = REPOSITORY_ROOT / "alembic.ini"
MIGRATIONS_FOLDER: Path = REPOSITORY_ROOT / "migrations"
