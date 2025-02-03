from typing import TYPE_CHECKING, List

from sqlalchemy import update
from sqlalchemy.future import select

from ..db_manager import DatabaseManager
from ..models import Account

if TYPE_CHECKING:
    from . import CommonCRUD


class AccountsCRUD:
    db: DatabaseManager

    def __init__(self, db: DatabaseManager, common_crud: "CommonCRUD") -> None:
        self.db = db
        self.common = common_crud

    async def add_account(
        self,
        account_id: int,
        phone_number: str,
        api_id: int,
        api_hash: str,
        proxy: dict,
        session_string: str,
    ) -> Account:
        async with self.db.get_session() as session:
            new_user = Account(
                id=account_id,
                phone_number=phone_number,
                api_id=api_id,
                api_hash=api_hash,
                proxy=proxy,
                session_string=session_string,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        
    async def get_accounts(self) -> List[Account]:
        async with self.db.get_session() as session:
            users = await session.execute(select(Account))
            return users.scalars().all()

    async def set_account_valid(self, account_id: int, status: bool = True) -> None:
        async with self.db.get_session() as session:
            await session.execute(
                update(Account).where(Account.id == account_id).values(is_valid=status)
            )
            await session.commit()
