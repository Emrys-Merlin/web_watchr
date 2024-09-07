from abc import ABC, abstractmethod
from enum import Enum, auto

from pydantic import BaseModel


class Status(Enum):
    """Enum representing the status of a comparison.

    Convenience enum because I got confused with booleans.

    Attributes:
        CHANGED: The text has changed.
        NO_CHANGES: The text has not changed.
    """

    CHANGED = auto()
    NO_CHANGES = auto()


class AbstractComparer(BaseModel, ABC):
    """Decide if a text has changed."""

    @abstractmethod
    def __call__(self, text: str) -> Status:
        """Decide if a text has changed.

        A new comparer must implement this method. The method should compare the text with the previous
        state and return the status of the comparison.
        """
        ...
