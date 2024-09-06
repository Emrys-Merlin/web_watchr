from pathlib import Path

from loguru import logger

from web_watchr.compare.abstract_comparer import Status

from . import AbstractComparer


class FSComparer(AbstractComparer):
    cache_dir: Path = Path("~/.local/share/website_monitoring_bot/cache").expanduser()
    send_on_missing: bool = False
    identifier: str = "fs_comparer"

    _cache_path: Path | None = None

    @property
    def cache_path(self) -> Path:
        if self._cache_path is None:
            self._cache_path = self.cache_dir / f"{self.identifier}.txt"
            if not self.cache_dir.exists():
                logger.debug(f"Creating cache directory: {self.cache_dir}")
                self.cache_dir.mkdir(parents=True)

        return self._cache_path

    def __call__(self, text: str) -> Status:
        if not self.cache_path.exists():
            logger.debug(f"Cache file not found: {self.cache_path}. Saving new state.")
            self._save(new_state=text)
            return Status.CHANGED if self.send_on_missing else Status.NO_CHANGES

        if not self._equal_to_cache(new_state=text):
            self._save(new_state=text)
            return Status.CHANGED

        return Status.NO_CHANGES

    def _load(self) -> str:
        with open(self.cache_path, "r") as f:
            return f.read()

    def _equal_to_cache(self, *, new_state: str) -> bool:
        old_state = self._load()
        return old_state == new_state

    def _save(self, *, new_state: str):
        with open(self.cache_path, "w") as f:
            f.write(new_state)
