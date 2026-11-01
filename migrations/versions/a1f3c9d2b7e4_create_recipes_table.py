from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a1f3c9d2b7e4"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("recipe_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.UniqueConstraint("recipe_id"),
    )


def downgrade() -> None:
    op.drop_table("recipes")
