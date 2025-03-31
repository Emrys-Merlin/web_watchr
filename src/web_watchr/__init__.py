from loguru import logger

from .watchr import Watchr

__all__ = ["Watchr"]
__version__ = "0.6.0"

logger.disable("website_monitoring_bot")
