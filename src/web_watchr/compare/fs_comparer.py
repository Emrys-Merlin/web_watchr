from pathlib import Path

from loguru import logger

from web_watchr.compare.abstract_comparer import Status

from . import AbstractComparer


class FSComparer(AbstractComparer):
    """A comparer that compares the text with the content of a file.

    Attributes:
        cache_dir: The directory where the cache file is stored. Defaults to `~/.local/share/web_watchr/cache`.
        send_on_missing: Whether to send a notification if the cache file is missing.
        identifier: The identifier used for the cache file.
    """

    cache_dir: Path = Path("~/.local/share/web_watchr/cache").expanduser()
    send_on_missing: bool = False
    identifier: str = "fs_comparer"

    _cache_path: Path | None = None

    @property
    def cache_path(self) -> Path:
        """The path to the cache file.

        Creates the cache directory if it does not exist.
        """
        if self._cache_path is None:
            self._cache_path = self.cache_dir / f"{self.identifier}.txt"
            if not self.cache_dir.exists():
                logger.debug(f"Creating cache directory: {self.cache_dir}")
                self.cache_dir.mkdir(parents=True)

        return self._cache_path

    def __call__(self, text: str) -> Status:
        """Compare the text with the content of the cache file.

        Args:
            text: The text to compare with the cache file.

        Returns:
            [`Status.CHANGED`][web_watchr.compare.Status] if the text is different from the cache file.
            [`Status.NO_CHANGES`][web_watchr.compare.Status] if the text is the same as the cache file.
            If the cache file is missing, it returns [`Status.CHANGED`][web_watchr.compare.Status] if `send_on_missing` is `True`.
        """
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
