from typing import List
from pathlib import Path

import aiosqlite


class DB:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.connection = None

    async def connect(self):
        """Автоматическое подключение к базе данных."""
        if not self.connection or not self.connection.is_alive():
            self.connection = await aiosqlite.connect(self.db_path)
            self.connection.row_factory = aiosqlite.Row

    async def close(self):
        """Закрытие соединения с базой данных."""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def create_tables(self):
        """Создание таблиц в базе данных."""
        async with self.connection.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY,
                    phone_number TEXT NOT NULL,
                    api_id TEXT NOT NULL,
                    api_hash TEXT NOT NULL,
                    proxy TEXT,
                    session_string TEXT NOT NULL,
                    is_valid BOOLEAN NOT NULL DEFAULT TRUE
                )
            """)
            await self.connection.commit()

    async def get_valid_accounts(self) -> List[aiosqlite.Row]:
        """Выполнение SQL-запроса."""
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM accounts WHERE is_valid"
            )
            return await cursor.fetchall()
