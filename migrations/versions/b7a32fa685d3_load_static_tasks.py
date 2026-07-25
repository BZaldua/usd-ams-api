"""load static tasks

Revision ID: b7a32fa685d3
Revises: a0c0b44b91a4
Create Date: 2026-07-19 11:24:22.371979

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import column, table

# revision identifiers, used by Alembic.
revision = "b7a32fa685d3"
down_revision = "a0c0b44b91a4"
branch_labels = None
depends_on = None


def upgrade():
    tasks_tbl = table("tasks", column("id", sa.Integer), column("name", sa.String))

    op.bulk_insert(
        tasks_tbl,
        [
            {"id": 1, "name": "modeling"},
            {"id": 2, "name": "texturig"},
            {"id": 3, "name": "rigging"},
            {"id": 4, "name": "layout"},
            {"id": 5, "name": "animation"},
            {"id": 6, "name": "vfx"},
            {"id": 7, "name": "lighting"},
            {"id": 8, "name": "compositing"},
            {"id": 9, "name": "rendering"},
        ],
    )


def downgrade():
    op.execute("DELETE FROM tasks WHERE id BETWEEN 1 AND 9")
