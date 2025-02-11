"""Добавил таблицы с ингнирированием лидов и их сообщений

Revision ID: 6cc967e05dd1
Revises: 90301f6074b6
Create Date: 2025-02-11 10:28:48.510973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cc967e05dd1'
down_revision: Union[str, None] = '90301f6074b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ignore_lead',
    sa.Column('id', sa.BIGINT(), nullable=False, comment='Айди аккаунта Teleagram'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ignore_lead_id'), 'ignore_lead', ['id'], unique=False)
    op.create_table('ignore_lead_messages',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False, comment='Идентификатор записи внутри нашей системы'),
    sa.Column('message', sa.TEXT(), nullable=False, comment='Игнорируемое сообщение'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ignore_lead_messages_message'), 'ignore_lead_messages', ['message'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ignore_lead_messages_message'), table_name='ignore_lead_messages')
    op.drop_table('ignore_lead_messages')
    op.drop_index(op.f('ix_ignore_lead_id'), table_name='ignore_lead')
    op.drop_table('ignore_lead')
    # ### end Alembic commands ###
