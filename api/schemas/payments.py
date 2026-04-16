from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    order_id: int
    payment_type: str
    transaction_status: str = "pending"
    amount: float
    card_last4: Optional[str] = None
    payment_reference: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    payment_type: Optional[str] = None
    transaction_status: Optional[str] = None
    amount: Optional[float] = None
    card_last4: Optional[str] = None
    payment_reference: Optional[str] = None


class Payment(PaymentBase):
    id: int
    paid_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)