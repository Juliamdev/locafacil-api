"""remove valor_referencia de casas

Revision ID: 0c0d8fa4c65d
Revises: 1ff3ff34b393
Create Date: 2026-09-25 20:29:30.605218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c0d8fa4c65d'
down_revision = '1ff3ff34b393'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # O valor do aluguel já vive em Contrato.valor_aluguel — esse campo em
    # Casa era duplicado e não fazia sentido manter.
    op.drop_column('casas', 'valor_referencia')


def downgrade() -> None:
    op.add_column('casas', sa.Column('valor_referencia', sa.Numeric(10, 2), nullable=False, server_default='0'))
