from datetime import datetime
import pytz

from util.errors import AuthenticationError

from config import TIMEZONE, WEBHOOK_SECRET


def get_current_timestamp():
    """
    Get the current timestamp in the desired timezone in the format of "hh:mm AM/PM dd/mm/yy"
    """
    sgt = pytz.timezone(TIMEZONE)
    current_time = datetime.now(sgt)
    return current_time.strftime("%I:%M %p %d/%m/%y")


def construct_alert_message(signal_type, symbol, current_price, note=None):
    """
    Construct an alert message for buy or sell signals.
    """
    message = (
        f"🚨 {signal_type.value} Signal Alert 🚨\n"
        "======================\n"
        f"Symbol: {symbol}\n"
        f"Price: {current_price}\n"
    )
    if note:
        message += f"Note: {note}\n"

    return message


def validate_webhook_secret(provided_secret: str):
    """
    Validates the webhook secret provided in the request body.
    """
    if provided_secret != WEBHOOK_SECRET:
        raise AuthenticationError("Invalid webhook secret")
