import pytest

from my_cookbook.recipes.infrastructure.postgres_settings import PostgresSettings


class TestPostgresSettings:
    def test_builds_the_connection_url_from_the_pg_environment_variables(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PG_USER", "cook")
        monkeypatch.setenv("PG_PASSWORD", "s3cret")
        monkeypatch.setenv("PG_HOST", "database.internal")
        monkeypatch.setenv("PG_DB", "cookbook")

        url = PostgresSettings.from_environment().url

        assert (
            url.render_as_string(hide_password=False)
            == "postgresql+psycopg://cook:s3cret@database.internal/cookbook"
        )

    def test_escapes_the_credentials_that_contain_reserved_characters(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PG_USER", "cook")
        monkeypatch.setenv("PG_PASSWORD", "p@ss/word")
        monkeypatch.setenv("PG_HOST", "database.internal")
        monkeypatch.setenv("PG_DB", "cookbook")

        url = PostgresSettings.from_environment().url

        assert url.password == "p@ss/word"
        assert (
            url.render_as_string(hide_password=False)
            == "postgresql+psycopg://cook:p%40ss%2Fword@database.internal/cookbook"
        )
