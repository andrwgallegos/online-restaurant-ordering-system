from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    customer_id: int
    order_id: int
    menu_item_id: Optional[int] = None
    rating: int
    review_text: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    customer_id: Optional[int] = None
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)