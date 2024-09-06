from unittest.mock import Mock, patch

from web_watchr.alert.telegram_alerter import TelegramAlerter


@patch("web_watchr.alert.telegram_alerter.Bot")
@patch("web_watchr.alert.telegram_alerter.run")
def test_telegram_alerter(
    mock_run: Mock,
    mock_telegram_bot: Mock,
):
    token = "invalid"
    chat_id = "different_but_invalid"
    message = "test message"
    alerter = TelegramAlerter(token=token, chat_id=chat_id)

    alerter(message)

    mock_telegram_bot.assert_called_once_with(token=token)
    mock_telegram_bot.return_value.send_message.assert_called_once_with(
        chat_id=chat_id,
        text=message,
    )
    mock_run.assert_called_once_with(
        mock_telegram_bot.return_value.send_message.return_value
    )
