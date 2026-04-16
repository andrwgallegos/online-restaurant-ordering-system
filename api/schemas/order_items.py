from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderItemBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    unit_price: float
    line_total: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    line_total: Optional[float] = None


class OrderItem(OrderItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)