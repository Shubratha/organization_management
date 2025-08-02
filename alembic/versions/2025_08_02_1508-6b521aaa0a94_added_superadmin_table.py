"""Added superadmin table

Revision ID: 6b521aaa0a94
Revises: 455ec55f6bb8
Create Date: 2025-08-02 15:08:01.458174

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from app.core.security import get_password_hash

# revision identifiers, used by Alembic.
revision: str = "6b521aaa0a94"
down_revision: Union[str, Sequence[str], None] = "455ec55f6bb8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create super_admins table
    op.create_table(
        "super_admins",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # Add default super admin for dev purpose
    default_password = "admin123"  # You should change this in production
    hashed_password = get_password_hash(default_password)

    op.execute(
        """
        INSERT INTO super_admins (email, password, is_active)
        VALUES ('admin@example.com', '{}', true)
        """.format(
            hashed_password
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("super_admins")
