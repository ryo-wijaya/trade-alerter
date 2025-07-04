from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from controller.signal_controller import signal_router
from telegram.telegram_client import TelegramClient

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signal_router)


@app.get("/")
async def health_check():
    try:
        return {"status": "Backend server is healthy and running :)"}
    except Exception as e:
        logging.error(f"Failed to perform health check: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform health check")
