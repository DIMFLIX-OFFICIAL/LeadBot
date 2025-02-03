from .accounts import AccountsCRUD
from ..db_manager import DatabaseManager


class CommonCRUD:
    __slots__ = (
        "db_manager",
        "accounts",
    )

    accounts: AccountsCRUD

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager
        self.accounts = AccountsCRUD(self.db_manager, self)
