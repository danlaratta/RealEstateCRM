"""listing and lead

Revision ID: 0908e84c8a41
Revises: 615049e9a77f
Create Date: 2025-03-12 18:41:58.643981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0908e84c8a41'
down_revision: Union[str, None] = '615049e9a77f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listings', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.create_unique_constraint(None, 'listings', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'listings', type_='unique')
    op.drop_column('listings', 'id')
    # ### end Alembic commands ###
