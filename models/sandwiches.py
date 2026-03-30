from sqlalchemy import Column, DECIMAL, Integer, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=False)
    price = Column(DECIMAL(6, 2), nullable=False, server_default="0.00")

    recipes = relationship("Recipe", back_populates="sandwich")
    order_details = relationship("OrderDetail", back_populates="sandwich")