from sqlalchemy import CheckConstraint, Column, Integer, Numeric, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"
    __table_args__ = (
        CheckConstraint("stock_amount >= 0", name="ck_resource_stock_amount_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resource_name = Column(String(120), unique=True, nullable=False)
    stock_amount = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    unit = Column(String(20), nullable=False)

    recipes = relationship("Recipe", back_populates="resource", cascade="all, delete-orphan")