import enum
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PaymentStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    transaction_id = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    order = relationship("Order", back_populates="payment")