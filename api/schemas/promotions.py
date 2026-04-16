from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PromotionBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str
    discount_value: float
    expiration_date: date
    is_active: bool = True


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    expiration_date: Optional[date] = None
    is_active: Optional[bool] = None


class Promotion(PromotionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)