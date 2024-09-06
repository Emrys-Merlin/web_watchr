from abc import ABC, abstractmethod
from enum import StrEnum, auto

from pydantic import BaseModel


class Status(StrEnum):
    CHANGED = auto()
    NO_CHANGES = auto()


class AbstractComparer(BaseModel, ABC):
    @abstractmethod
    def __call__(self, text: str) -> Status: ...
