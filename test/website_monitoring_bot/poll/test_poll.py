from unittest.mock import Mock, patch

from pydantic.networks import AnyHttpUrl
from requests import Response

from website_monitoring_bot.poll import Poll


@patch("website_monitoring_bot.poll.poll.get")
def test_poll(
    mocked_get: Mock,
    poll_config: Poll,
    test_page: str,
    test_url: AnyHttpUrl,
):
    """Poll extracts the correct website element."""
    mocked_response = Mock(spec=Response)
    mocked_response.text = test_page
    mocked_get.return_value = mocked_response
    expected = "Test"

    res = poll_config.poll()

    mocked_get.assert_called_once_with(url=test_url)
    assert res == expected


def test_website_does_not_exist(poll_config: Poll):
    """Returns an empty string if website does not exist"""
    url = "https://does-not.work"
    poll_config.url = url

    res = poll_config.poll()

    assert res == ""


def test_element_does_not_exist(poll_config: Poll):
    """Returns an empty string if element does not exist"""
    element = "non_existent"
    poll_config.element = element

    res = poll_config.poll()

    assert res == ""
