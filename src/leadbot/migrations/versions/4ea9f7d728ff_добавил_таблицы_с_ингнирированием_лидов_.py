"""Добавил таблицы с ингнирированием лидов и их сообщений

Revision ID: 4ea9f7d728ff
Revises: 
Create Date: 2025-02-11 11:27:48.200830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ea9f7d728ff'
down_revision: Union[str, None] = "90301f6074b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ignore_lead_messages',
    sa.Column('message', sa.TEXT(), nullable=False, comment='Игнорируемое сообщение'),
    sa.PrimaryKeyConstraint('message')
    )
    op.create_index(op.f('ix_ignore_lead_messages_message'), 'ignore_lead_messages', ['message'], unique=False)
    op.create_table('ignore_leads',
    sa.Column('id', sa.BIGINT(), nullable=False, comment='Айди аккаунта Teleagram'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ignore_leads_id'), 'ignore_leads', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ignore_leads_id'), table_name='ignore_leads')
    op.drop_table('ignore_leads')
    op.drop_index(op.f('ix_ignore_lead_messages_message'), table_name='ignore_lead_messages')
    op.drop_table('ignore_lead_messages')
    # ### end Alembic commands ###
