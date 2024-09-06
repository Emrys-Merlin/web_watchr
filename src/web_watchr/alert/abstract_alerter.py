from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractAlerter(BaseModel, ABC):
    @abstractmethod
    def __call__(self, text: str) -> None: ...
