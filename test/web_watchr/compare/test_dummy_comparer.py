import string
from random import choices, randint

from web_watchr.compare import DummyComparer, Status


def test_always_status_changed():
    comparer = DummyComparer()
    alphabet = string.ascii_letters + string.digits
    text_length = randint(0, 10)
    text = "".join(choices(alphabet, k=text_length))

    assert comparer(text=text) == Status.CHANGED
