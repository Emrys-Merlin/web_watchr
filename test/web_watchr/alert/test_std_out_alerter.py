import builtins
from unittest.mock import Mock

from web_watchr.alert.print_alerter import PrintAlerter


def test_std_out_alerter():
    message = "Test"
    alerter = PrintAlerter()

    # Inspired by https://stackoverflow.com/a/62360735/9685500
    mock = Mock()
    print_original = print
    builtins.print = mock

    try:
        alerter(message)

        mock.assert_called_once_with(message)
    finally:
        builtins.print = print_original  # ensure print is "unmocked"
