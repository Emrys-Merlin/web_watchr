from typing import Callable

from loguru import logger
from playwright.sync_api import Playwright, sync_playwright
from pydantic import BaseModel, Field, PrivateAttr

from web_watchr.alert import AbstractAlerter, PrintAlerter
from web_watchr.compare import AbstractComparer, FSComparer, Status


class Watchr(BaseModel):
    comparer: AbstractComparer = Field(default_factory=FSComparer)
    alerter: AbstractAlerter = Field(default_factory=PrintAlerter)

    _poller: Callable[[Playwright], str] | None = PrivateAttr(default=None)

    @property
    def poller(self) -> Callable[[Playwright], str]:
        if self._poller is None:
            message = "Please set a poller function using the `set_poller` decorator."
            logger.error(message)
            raise ValueError(message)
        return self._poller

    def set_poller(
        self,
        f: Callable[[Playwright], str],
    ) -> Callable[[Playwright], str]:
        self._poller = f
        return f

    def __call__(
        self,
    ) -> None:
        with sync_playwright() as playwright:
            result = self.poller(playwright)
            logger.debug(result)

        if self.comparer(result) == Status.NO_CHANGES:
            logger.info("No changes detected.")
            return

        logger.info("Changes detected! Sending alert.")
        self.alerter(result)
