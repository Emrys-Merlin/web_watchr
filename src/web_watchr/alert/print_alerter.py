from . import AbstractAlerter


class PrintAlerter(AbstractAlerter):
    def __call__(self, text: str):
        print(text)
