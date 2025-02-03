from typing import Any

from sqlalchemy import (
    BIGINT,
    JSON,
    TEXT,
    Boolean,
    String
)
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from .db_manager import Base


class BaseModel(Base):
    __abstract__ = True

    def to_dict(self) -> dict[str, Any]:
        """Метод для преобразования объекта в словарь."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Account(BaseModel):
    __tablename__: str = "accounts"
    __tableargs__ = {"comment": "Таблица с телеграм аккаунтами для спама рекламой."}

    id: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Айди аккаунта Teleagram",
    )
    phone_number: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
        comment="номер телефона, привязанный к аккаунту.",
    )
    api_id: Mapped[int] = mapped_column(
        BIGINT, nullable=False, comment="параметр для аутентификации"
    )
    api_hash: Mapped[str] = mapped_column(
        String, nullable=False, comment="параметр для аутентификации"
    )

    _proxy: Mapped[dict] = mapped_column(
        JSON,
        nullable=True,
        default=None,
        comment='прокси для аккаунта в формате JSON. Пример: {"scheme": "socks5", "hostname": "...", "port": 1234}',
    )

    session_string: Mapped[str] = mapped_column(
        TEXT, nullable=False, comment="Сессия в формате строки"
    )

    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true",
        comment="валидная ли сессия или нет",
    )

    @property
    def proxy(self) -> dict:
        return self._proxy

    @proxy.setter
    def proxy(self, value: Optional[dict]) -> None:
        if value is None:
            self._proxy = None
            return
        
        required_keys = [
            ("scheme", str),
            ("hostname", str),
            ("port", int),
            ("username", str),
            ("password", str),
        ]

        for key in required_keys:
            if key[0] not in value or not isinstance(value[key[0]], key[1]):
                raise ValueError(
                    "Missing required keys or incorrect types in proxy settings."
                )

        self._proxy = value

    def __str__(self):
        return f"[{self.id}] {self.phone_number}"
