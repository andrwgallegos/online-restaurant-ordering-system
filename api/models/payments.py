from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_payment_amount_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_type = Column(String(30), nullable=False)
    transaction_status = Column(String(30), nullable=False, server_default="pending")
    amount = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    card_last4 = Column(String(4), nullable=True)
    payment_reference = Column(String(100), nullable=True)
    paid_at = Column(DateTime, nullable=False, server_default=func.now())

    order = relationship("Order", back_populates="payments")