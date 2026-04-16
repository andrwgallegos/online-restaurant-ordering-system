from sqlalchemy import Boolean, CheckConstraint, Column, Date, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"
    __table_args__ = (
        CheckConstraint("discount_value >= 0", name="ck_promotion_discount_value_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(40), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(String(20), nullable=False, server_default="percentage")
    discount_value = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    expiration_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="1")

    orders = relationship("Order", back_populates="promotion")