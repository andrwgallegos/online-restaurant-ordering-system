from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str
    order_type: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    order_type: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    status: str
    tracking_number: str
    order_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)