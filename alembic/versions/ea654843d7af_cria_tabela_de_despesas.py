"""cria tabela de despesas

Revision ID: ea654843d7af
Revises: 0c0d8fa4c65d
Create Date: 2026-09-26 17:31:35.459699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea654843d7af'
down_revision = '0c0d8fa4c65d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'despesas',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('casa_id', sa.UUID(), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('valor', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('data', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['casa_id'], ['casas.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('despesas')
