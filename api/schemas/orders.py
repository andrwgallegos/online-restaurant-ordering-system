from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    customer_id: int
    promotion_id: Optional[int] = None
    fulfillment_type: str
    subtotal: float = 0.0
    discount_amount: float = 0.0
    total_price: float = 0.0
    delivery_address: str
    special_instructions: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    fulfillment_type: Optional[str] = None
    order_status: Optional[str] = None
    subtotal: Optional[float] = None
    discount_amount: Optional[float] = None
    total_price: Optional[float] = None
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None


class Order(OrderBase):
    id: int
    tracking_number: str
    order_status: str
    order_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)