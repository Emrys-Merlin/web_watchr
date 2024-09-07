from . import AbstractAlerter


class PrintAlerter(AbstractAlerter):
    """Print the alert to the standard output."""

    def __call__(self, text: str) -> None:
        """Print the alert to the standard output.

        Args:
            text: The text of the alert.
        """
        print(text)
