from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

import pytest
from pydantic.networks import AnyHttpUrl
from website_monitoring_bot.compare.fs_comparer import FSComparer, FSComparerConfig
from website_monitoring_bot.poll import Poll


@pytest.fixture()
def test_url() -> str:
    return "http://example.com/"


@pytest.fixture()
def test_element():
    return "test_element"


@pytest.fixture
def poll_config(
    test_url: str,
    test_element: str,
) -> Poll:
    return Poll(
        url=test_url,
        element=test_element,
    )


@pytest.fixture
def test_page_path() -> Path:
    return Path(__file__).parent / "data/test.html"


@pytest.fixture
def test_page(test_page_path: Path) -> str:
    with open(test_page_path, "r") as f:
        return f.read()


@pytest.fixture
def test_cache_dir() -> Path:
    return Path(TemporaryDirectory().name)


@pytest.fixture
def test_fs_comparer_config(test_cache_dir: Path) -> FSComparerConfig:
    return FSComparerConfig(cache_dir=test_cache_dir)


@pytest.fixture
def mock_poller() -> Callable[[], str]:
    return lambda: "test"


@pytest.fixture
def test_fs_comparer(
    test_fs_comparer_config: FSComparerConfig,
    mock_poller: Callable[[], str],
) -> FSComparer:
    return FSComparer(
        config=test_fs_comparer_config,
        poller=mock_poller,
    )
