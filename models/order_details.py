from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)
    amount = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_details")
    sandwich = relationship("Sandwich", back_populates="order_details")