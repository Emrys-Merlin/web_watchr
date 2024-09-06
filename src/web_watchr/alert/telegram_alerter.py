from asyncio import run

from loguru import logger
from telegram import Bot

from . import AbstractAlerter


class TelegramAlerter(AbstractAlerter):
    token: str
    chat_id: str

    _bot: Bot | None = None

    @property
    def bot(self) -> Bot:
        if self._bot is None:
            self._bot = Bot(token=self.token)
        return self._bot

    def __call__(self, text: str):
        logger.debug(f"Sending message '{text}' to telegram.")
        run(self.bot.send_message(chat_id=self.chat_id, text=text))
