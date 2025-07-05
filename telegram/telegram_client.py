import requests
import logging
from util.helpers import get_current_timestamp
from util.errors import AlerterError


class TelegramClient:
    def __init__(self, bot_token, chat_id):
        """
        Initialize the TelegramClient with the bot token and chat ID.
        """
        if not bot_token or not chat_id:
            raise AlerterError("Bot token and chat ID must be provided.")
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, message):
        """
        Send a message to the Telegram chat via a configured Telegram bot.
        """
        if not message:
            raise AlerterError("Message content cannot be empty.")

        payload = {"chat_id": self.chat_id, "text": message}

        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            if response.status_code == 200:
                logging.info(
                    f"Message: '{message}' sent successfully to Telegram at {get_current_timestamp()}"
                )
                return True
            else:
                error_message = (
                    f"Failed to send message to Telegram. Status Code: {response.status_code}, "
                    f"Response: {response.text}"
                )
                raise AlerterError(error_message)
        except requests.exceptions.Timeout:
            raise AlerterError("Request to Telegram API timed out.")
        except requests.exceptions.RequestException as e:
            raise AlerterError(f"An error occurred while sending the message: {e}")
        except Exception as e:
            raise AlerterError(f"An unexpected error occurred: {e}")
