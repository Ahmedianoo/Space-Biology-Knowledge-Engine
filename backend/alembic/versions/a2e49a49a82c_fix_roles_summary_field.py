"""Fix roles_summary field

Revision ID: a2e49a49a82c
Revises: 407514f54b73
Create Date: 2025-10-04 01:15:46.581365
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a2e49a49a82c'
down_revision: str = '407514f54b73'
branch_labels: str | None = None
depends_on: str | None = None

def upgrade() -> None:
    """Upgrade schema."""
    # Use raw SQL with USING clause to safely cast text -> JSONB
    op.execute("""
        ALTER TABLE summaries
        ALTER COLUMN scientist_summary TYPE JSONB USING scientist_summary::jsonb;
    """)
    op.execute("""
        ALTER TABLE summaries
        ALTER COLUMN manager_summary TYPE JSONB USING manager_summary::jsonb;
    """)
    op.execute("""
        ALTER TABLE summaries
        ALTER COLUMN mission_architect_summary TYPE JSONB USING mission_architect_summary::jsonb;
    """)

def downgrade() -> None:
    """Downgrade schema."""
    # Cast JSONB back to TEXT
    op.execute("""
        ALTER TABLE summaries
        ALTER COLUMN mission_architect_summary TYPE TEXT USING mission_architect_summary::text;
    """)
    op.execute("""
        ALTER TABLE summaries
        ALTER COLUMN manager_summary TYPE TEXT USING manager_summary::text;
    """)
    op.execute("""
        ALTER TABLE summaries
        ALTER COLUMN scientist_summary TYPE TEXT USING scientist_summary::text;
    """)
