import os
from dataclasses import dataclass

from sqlalchemy.engine import URL


@dataclass(frozen=True)
class PostgresSettings:
    user: str
    password: str
    host: str
    database: str

    @classmethod
    def from_environment(cls) -> PostgresSettings:
        return cls(
            user=os.environ["PG_USER"],
            password=os.environ["PG_PASSWORD"],
            host=os.environ["PG_HOST"],
            database=os.environ["PG_DB"],
        )

    @property
    def url(self) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
        )
