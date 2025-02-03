import sys
from .config import cfg
from .database.db_manager import DatabaseManager
from .database.cruds import CommonCRUD

from loguru import logger


##==> Database
#################################################
db_manager = DatabaseManager(cfg.db.url)
db = CommonCRUD(db_manager)


##==> Logging
#################################################
logger.remove()

format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{module}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# Создаем директорию для логов, если она не существует
logs_dir = cfg.logs.folder
logs_dir.mkdir(exist_ok=True)

logger.add(
    sink=logs_dir / "app_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # Ротация каждый день в полночь
    retention=cfg.logs.retention,
    compression="zip",
    level=cfg.logs.level,
    format=format,
)

logger.add(sys.stderr, level=cfg.logs.level, format=format)
