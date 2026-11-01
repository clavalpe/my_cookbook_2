from alembic import context
from sqlalchemy import create_engine

from my_cookbook.recipes.infrastructure.postgres_settings import PostgresSettings


def run_migrations() -> None:
    engine = create_engine(PostgresSettings.from_environment().url)
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


run_migrations()
