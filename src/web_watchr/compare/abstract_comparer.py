from abc import ABC, abstractmethod
from enum import Enum, auto

from pydantic import BaseModel


class Status(Enum):
    CHANGED = auto()
    NO_CHANGES = auto()


class AbstractComparer(BaseModel, ABC):
    @abstractmethod
    def __call__(self, text: str) -> Status: ...
