from loguru import logger

from .watchr import Watchr

__all__ = ["Watchr"]
__version__ = "0.2.1"

logger.disable("website_monitoring_bot")
