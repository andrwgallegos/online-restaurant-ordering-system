from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="ck_order_subtotal_non_negative"),
        CheckConstraint("discount_amount >= 0", name="ck_order_discount_non_negative"),
        CheckConstraint("total_price >= 0", name="ck_order_total_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)
    order_date = Column(DateTime, nullable=False, server_default=func.now())
    tracking_number = Column(String(50), unique=True, nullable=False, index=True)
    order_status = Column(String(30), nullable=False, server_default="pending")
    fulfillment_type = Column(String(20), nullable=False, server_default="takeout")
    subtotal = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    discount_amount = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    total_price = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    delivery_address = Column(String(255), nullable=False)
    special_instructions = Column(String(300), nullable=True)

    customer = relationship("Customer", back_populates="orders")
    promotion = relationship("Promotion", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="order")