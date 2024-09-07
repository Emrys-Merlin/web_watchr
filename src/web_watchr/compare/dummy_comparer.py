from . import AbstractComparer, Status


class DummyComparer(AbstractComparer):
    """A comparer that always returns [`Status.CHANGED`][web_watchr.compare.Status]."""

    def __call__(self, text: str) -> Status:
        """Always return [`Status.CHANGED`][web_watchr.compare.Status]."""
        return Status.CHANGED
