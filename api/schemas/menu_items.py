from typing import Optional

from pydantic import BaseModel, ConfigDict


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients_summary: Optional[str] = None
    price: float
    calories: int
    food_category: str
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ingredients_summary: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    food_category: Optional[str] = None
    is_available: Optional[bool] = None


class MenuItem(MenuItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)