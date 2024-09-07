from typing import Callable

from loguru import logger
from playwright.sync_api import Playwright, sync_playwright
from pydantic import BaseModel, Field, PrivateAttr

from web_watchr.alert import AbstractAlerter, PrintAlerter
from web_watchr.compare import AbstractComparer, FSComparer, Status


class Watchr(BaseModel):
    """Central class that orchestrates the polling, comparing, and alerting process.

    Attributes:
        alerter: The instance is called with the scraped text and is responsible to send out the alert.
        comparer: The instance is called with the scraped text and is responsible to compare the text with
            the previous state to check if there are any changes and an alert is necessary.
    """

    comparer: AbstractComparer = Field(default_factory=FSComparer)
    alerter: AbstractAlerter = Field(default_factory=PrintAlerter)

    _poller: Callable[[Playwright], str] | None = PrivateAttr(default=None)

    @property
    def poller(self) -> Callable[[Playwright], str]:
        """The poller function that scrapes the text from the website."""
        if self._poller is None:
            message = "Please set a poller function using the `set_poller` decorator."
            logger.error(message)
            raise ValueError(message)
        return self._poller

    def set_poller(
        self,
        f: Callable[[Playwright], str],
    ) -> Callable[[Playwright], str]:
        """Decorator to set the poller function.

        The wrapper returns the function unchanged, but stores it in the `_poller` attribute.

        Args:
            f: A function that takes a `Playwright` instance and returns the scraped text.

        Returns:
            The function that was passed in.
        """
        self._poller = f
        return f

    def __call__(
        self,
    ) -> None:
        """Main method that orchestrates the polling, comparing, and alerting process.

        When called the poller function is called to scrape the text from the website. The text is then
        compared to the previous state. If there are changes, an alert is sent out.
        """
        with sync_playwright() as playwright:
            result = self.poller(playwright)
            logger.debug(result)

        if self.comparer(result) == Status.NO_CHANGES:
            logger.info("No changes detected.")
            return

        logger.info("Changes detected! Sending alert.")
        self.alerter(result)
