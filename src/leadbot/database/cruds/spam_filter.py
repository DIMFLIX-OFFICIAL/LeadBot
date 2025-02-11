from typing import TYPE_CHECKING, List

from sqlalchemy import exists
from sqlalchemy.future import select

from ..db_manager import DatabaseManager
from ..models import IgnoreLead, IgnoreLeadMessage

if TYPE_CHECKING:
    from . import CommonCRUD


class SpamFilterCRUD:
    db: DatabaseManager

    def __init__(self, db: DatabaseManager, common_crud: "CommonCRUD") -> None:
        self.db = db
        self.common = common_crud

    async def add_account_to_ignore(self, account_id: int) -> IgnoreLead:
        async with self.db.get_session() as session:
            exists_query = await session.execute(
                select(exists().where(IgnoreLead.id == account_id))
            )
            if not exists_query.scalar():
                new_ignored_lead = IgnoreLead(id=account_id)
                session.add(new_ignored_lead)
                await session.commit()
                await session.refresh(new_ignored_lead)
                return new_ignored_lead
        
    async def add_message_to_ignore(self, message_text: str) -> IgnoreLeadMessage:
        async with self.db.get_session() as session:
            exists_query = await session.execute(
                select(exists().where(IgnoreLeadMessage.message == message_text))
            )
            if not exists_query.scalar():
                new_ignored_lead_message = IgnoreLeadMessage(message=message_text)
                session.add(new_ignored_lead_message)
                await session.commit()
                await session.refresh(new_ignored_lead_message)
                return new_ignored_lead_message
        
    async def add_full_ignore(self, account_id: int, message_text: str):
        await self.add_account_to_ignore(account_id)
        await self.add_message_to_ignore(message_text)

    async def get_ignoring_accounts(self) -> List[IgnoreLead]:
        async with self.db.get_session() as session:
            ignoring_accounts = await session.execute(select(IgnoreLead))
            return ignoring_accounts.scalars().all()

    async def get_ignoring_messages(self) -> List[IgnoreLeadMessage]:
        async with self.db.get_session() as session:
            ignoring_messages = await session.execute(select(IgnoreLeadMessage))
            return ignoring_messages.scalars().all()
        