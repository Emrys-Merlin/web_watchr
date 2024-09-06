from unittest.mock import MagicMock

import pytest
from web_watchr.compare.abstract_comparer import Status
from web_watchr.watchr import Watchr


def test_unset_poller(
    mocked_watchr: Watchr,
):
    with pytest.raises(ValueError):
        mocked_watchr()


def test_watchr(
    mocked_watchr: Watchr,
    mock_variable_poller: MagicMock,
    mock_status_list: list[Status],
):
    mocked_watchr.set_poller(mock_variable_poller)
    n = len(mock_status_list)
    n_sent = len([status for status in mock_status_list if status == Status.CHANGED])

    for _ in range(n):
        mocked_watchr()

    assert mock_variable_poller.call_count == n
    assert mocked_watchr.comparer.call_count == n
    assert mocked_watchr.alerter.call_count == n_sent
