# credits: https://github.com/deependujha

import os
import telebot
from typing import override
from deepflow_engine.publisher.base import BasePublisher


def get_telegram_bot_token() -> str:
    return os.getenv("TELEGRAM_BOT_TOKEN")


class TelegramPublisher(BasePublisher):
    def __init__(self) -> None:
        _token = get_telegram_bot_token()
        if not _token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")
        self._bot = telebot.TeleBot(_token)
        self._chat_id = "-1003780272239"  # oddly_realm group

    @override
    def _publish(self, filename: str, msg: str) -> None:
        video = open(filename, "rb")
        self._bot.send_video(chat_id=self._chat_id, video=video, caption=msg)
        video.close()
