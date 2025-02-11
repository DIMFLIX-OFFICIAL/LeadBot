from .accounts import AccountsCRUD
from ..db_manager import DatabaseManager
from .spam_filter import SpamFilterCRUD


class CommonCRUD:
    __slots__ = (
        "db_manager",
        "accounts",
        "spam"
    )

    accounts: AccountsCRUD

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager
        self.accounts = AccountsCRUD(self.db_manager, self)
        self.spam = SpamFilterCRUD(self.db_manager, self)
