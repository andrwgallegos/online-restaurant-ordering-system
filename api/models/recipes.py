from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"
    __table_args__ = (
        UniqueConstraint("menu_item_id", "resource_id", name="uq_recipe_menu_item_resource"),
        CheckConstraint("amount_required >= 0", name="ck_recipe_amount_required_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    amount_required = Column(Numeric(10, 2), nullable=False, server_default="0.00")

    menu_item = relationship("MenuItem", back_populates="recipes")
    resource = relationship("Resource", back_populates="recipes")