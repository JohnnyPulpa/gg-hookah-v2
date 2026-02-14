"""add_discounts_used_order_fk

Revision ID: ffe00b36291f
Revises: 4ee508eaed82
Create Date: 2026-02-06
"""
from typing import Sequence, Union
from alembic import op

revision: str = 'ffe00b36291f'
down_revision: Union[str, None] = '4ee508eaed82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        'fk_discounts_used_order_id',
        'discounts', 'orders',
        ['used_order_id'], ['id'],
    )


def downgrade() -> None:
    op.drop_constraint('fk_discounts_used_order_id', 'discounts', type_='foreignkey')
