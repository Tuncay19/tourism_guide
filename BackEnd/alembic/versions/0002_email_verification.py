"""email tesdiqleme sahələri elave edilir

Revision ID: 0002_email_verification
Revises: 0001_init
Create Date: 2026-09-27

"""
from alembic import op
import sqlalchemy as sa

revision = "0002_email_verification"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("verification_code", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column("verification_code_expires_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "verification_code_expires_at")
    op.drop_column("users", "verification_code")
