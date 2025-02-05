from pathlib import Path
from typing import List

import yaml
from pydantic import field_validator
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    token: str
    manager_chat_id: int
    log_chat_id: int
    folder_name: str
    trigger_words: List[str]
    blacklist_chats: List[int]
    delay_for_update_accounts_chats: int


class Database(BaseSettings):
    url: str


class LogsConfig(BaseSettings):
    level: str
    retention: str
    folder: Path

    @field_validator("folder", mode="before")
    def validate_folder(cls, v) -> Path:
        path = Path(v).resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path


class Config(BaseSettings):
    bot: BotConfig
    db: Database
    logs: LogsConfig

    @classmethod
    def from_yaml(cls, config_file: Path) -> "Config":
        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return cls(**config)


project_src: Path = Path(__file__).resolve().parent.parent
project_root: Path = project_src.parent
path_to_yaml = project_root / ".env.yaml"
path_to_db = project_root / "data.db"
cfg = Config.from_yaml(path_to_yaml)
