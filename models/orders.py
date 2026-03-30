from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    customer_address = Column(String(255), nullable=False)
    order_type = Column(String(20), nullable=False, default="takeout")
    status = Column(String(30), nullable=False, default="pending")
    tracking_number = Column(String(50), unique=True, nullable=False)
    description = Column(String(300), nullable=True)
    order_date = Column(DateTime, nullable=False, server_default=func.now())

    order_details = relationship(
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan"
    )