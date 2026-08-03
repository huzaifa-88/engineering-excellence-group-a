"""add task timestamps

Revision ID: 8c2f41d9b731
Revises: d6d0667d3a3d
Create Date: 2026-07-29 14:12:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8c2f41d9b731"
down_revision: str | Sequence[str] | None = "d6d0667d3a3d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "task",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.add_column(
        "task",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("task", "updated_at")
    op.drop_column("task", "created_at")
