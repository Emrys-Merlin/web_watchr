from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from loguru import logger
from pydantic import BaseModel


class FSComparerConfig(BaseModel):
    cache_dir: Path = Path(
        "$HOME/.local/share/website_monitoring_bot/cache"
    ).expanduser()
    send_on_missing: bool = False


@dataclass
class FSComparer:
    config: FSComparerConfig
    poller: Callable[[], str]
    # sender: Any

    def __post_init__(self):
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _cache_path(*, cache_dir: Path, poller: Callable[[], str]) -> Path:
        return cache_dir / f"{hash(poller)}.txt"

    @property
    def cache_path(self) -> Path:
        return self._cache_path(cache_dir=self.config.cache_dir, poller=self.poller)

    def _load_cache(self) -> str:
        with open(self.cache_path, "r") as f:
            return f.read()

    def compare(self, *, new_state: str) -> bool:
        try:  # load cache
            old_state = self._load_cache()
        except FileNotFoundError:
            return not self.config.send_on_missing

        return old_state == new_state

    def save(self, *, new_state: str):
        with open(self.cache_path, "w") as f:
            f.write(new_state)

    def run(self):
        new_state = self.poller()
        if not self.compare(new_state=new_state):
            self.save(new_state=new_state)
            # self.sender.send(new_state=new_state)
            logger.info(f"New data found: {new_state}")
        else:
            logger.info("No new data found")
