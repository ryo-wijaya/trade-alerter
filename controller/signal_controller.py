from fastapi import APIRouter, HTTPException, Depends
import logging

from telegram.telegram_client import TelegramClient
from util.errors import AlerterError, AuthenticationError
from util.helpers import construct_alert_message, validate_webhook_secret
from util.enums import AlertType
from util.models import SignalRequest

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


signal_router = APIRouter(prefix="/webhook", tags=["Signals"])


def get_telegram_client():
    return TelegramClient(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)


@signal_router.post("/buy-signal/{ticker}/")
async def send_buy_signal(
    ticker: str,
    request: SignalRequest,
    telegram_client: TelegramClient = Depends(get_telegram_client),
):
    """
    Endpoint to send a buy signal via Telegram.
    """
    try:
        validate_webhook_secret(request.webhook_secret)
        message = construct_alert_message(
            signal_type=AlertType.BUY,
            symbol=ticker,
            current_price=request.current_price,
            note=request.note,
        )
        telegram_client.send_message(message)
        return {"status": "success", "message": "Buy signal sent successfully"}
    except AuthenticationError as e:
        logging.error(f"Invalid webhook secret.")
        raise HTTPException(status_code=401, detail=str(e))
    except AlerterError as e:
        logging.error(f"Error sending buy signal: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@signal_router.post("/sell-signal/{ticker}/")
async def send_sell_signal(
    ticker: str,
    request: SignalRequest,
    telegram_client: TelegramClient = Depends(get_telegram_client),
):
    """
    Endpoint to send a sell signal via Telegram.
    """
    try:
        validate_webhook_secret(request.webhook_secret)
        message = construct_alert_message(
            signal_type=AlertType.SELL,
            symbol=ticker,
            current_price=request.current_price,
            note=request.note,
        )
        telegram_client.send_message(message)
        return {"status": "success", "message": "Sell signal sent successfully"}
    except AuthenticationError as e:
        logging.error(f"Invalid webhook secret.")
        raise HTTPException(status_code=401, detail=str(e))
    except AlerterError as e:
        logging.error(f"Error sending sell signal: {e}")
        raise HTTPException(status_code=500, detail=str(e))
