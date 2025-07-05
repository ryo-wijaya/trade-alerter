from pydantic import BaseModel


class SignalRequest(BaseModel):
    webhook_secret: str
    current_price: float
    note: str = None
