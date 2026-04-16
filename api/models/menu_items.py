from sqlalchemy import Boolean, CheckConstraint, Column, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_menu_item_price_non_negative"),
        CheckConstraint("calories >= 0", name="ck_menu_item_calories_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    ingredients_summary = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    calories = Column(Integer, nullable=False, server_default="0")
    food_category = Column(String(50), nullable=False)
    is_available = Column(Boolean, nullable=False, server_default="1")

    recipes = relationship("Recipe", back_populates="menu_item", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="menu_item")
    reviews = relationship("Review", back_populates="menu_item")