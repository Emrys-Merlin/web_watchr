from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractAlerter(BaseModel, ABC):
    """Send an alert."""

    @abstractmethod
    def __call__(self, text: str) -> None:
        """Send an alert.

        A new alerter must implement this method. The method should send the alert with the given text.

        Args:
            text: The text of the alert.
        """
        ...
