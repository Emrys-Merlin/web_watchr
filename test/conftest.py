from pathlib import Path

import pytest
from pydantic.networks import AnyHttpUrl

from website_monitoring_bot.poll import Poll


@pytest.fixture()
def test_url() -> AnyHttpUrl:
    return AnyHttpUrl("http://example.com")


@pytest.fixture()
def test_element():
    return "test_element"


@pytest.fixture
def poll_config(
    test_url: AnyHttpUrl,
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
