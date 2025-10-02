"""add metadata fields to publications

Revision ID: 989bbe42f7fd
Revises: 11d5859d5c0c
Create Date: 2025-10-02 00:33:28.194480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '989bbe42f7fd'
down_revision: Union[str, Sequence[str], None] = '11d5859d5c0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add metadata fields to publications."""
    op.add_column('publications', sa.Column('journal', sa.String(), nullable=True))
    op.add_column('publications', sa.Column('date', sa.String(), nullable=True))
    op.add_column('publications', sa.Column('authors', postgresql.JSONB(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    """Downgrade schema: remove metadata fields from publications."""
    op.drop_column('publications', 'authors')
    op.drop_column('publications', 'date')
    op.drop_column('publications', 'journal')
