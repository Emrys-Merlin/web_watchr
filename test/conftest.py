from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator
from unittest.mock import MagicMock

import pytest
from web_watchr.alert.abstract_alerter import AbstractAlerter
from web_watchr.compare.abstract_comparer import AbstractComparer, Status
from web_watchr.compare.fs_comparer import FSComparer
from web_watchr.watchr import Watchr


@pytest.fixture()
def cache_dir() -> Iterator[Path]:
    with TemporaryDirectory() as temp_dir:
        yield Path(temp_dir) / "cache"


@pytest.fixture()
def fs_comparer(
    cache_dir: Path,
) -> FSComparer:
    return FSComparer(cache_dir=cache_dir)


@pytest.fixture()
def mock_variable_poller() -> MagicMock:
    poller = MagicMock()
    poller.side_effect = ["a", "b", "c"]
    return poller


@pytest.fixture()
def mock_status_list() -> list[Status]:
    return [Status.CHANGED, Status.NO_CHANGES, Status.CHANGED]


@pytest.fixture()
def mock_comparer(
    mock_status_list: list[Status],
) -> MagicMock:
    mock = MagicMock(spec=AbstractComparer)
    mock.side_effect = mock_status_list
    return mock


@pytest.fixture()
def mock_alerter() -> MagicMock:
    return MagicMock(spec=AbstractAlerter)


@pytest.fixture()
def mocked_watchr(
    mock_comparer: MagicMock,
    mock_alerter: MagicMock,
) -> Watchr:
    return Watchr(
        comparer=mock_comparer,
        alerter=mock_alerter,
    )
