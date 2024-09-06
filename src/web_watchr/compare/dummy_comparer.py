from . import AbstractComparer, Status


class DummyComparer(AbstractComparer):
    def __call__(self, text: str) -> Status:
        return Status.CHANGED
