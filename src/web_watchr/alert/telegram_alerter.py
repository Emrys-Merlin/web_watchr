from asyncio import run

from loguru import logger
from telegram import Bot

from . import AbstractAlerter


class TelegramAlerter(AbstractAlerter):
    """Sends a message to a telegram chat.

    For this alerter to work, you need to
    [create a telegram bot and get its token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).
    Furthermore, the bot needs to be added to the chat you want to send messages to and you
    need to retrieve the chat ID of the chat (e.g., like [this](https://stackoverflow.com/a/32572159/9685500)).

    Attributes:
        token: The token of the telegram bot.
        chat_id: The chat ID to send the message to.
    """

    token: str
    chat_id: str

    _bot: Bot | None = None

    @property
    def bot(self) -> Bot:
        """Telegram bot instance"""
        if self._bot is None:
            self._bot = Bot(token=self.token)
        return self._bot

    def __call__(self, text: str) -> None:
        """Send a message to a telegram chat.

        Args:
            text: The text of the message.
        """
        logger.debug(f"Sending message '{text}' to telegram.")
        run(self.bot.send_message(chat_id=self.chat_id, text=text))
