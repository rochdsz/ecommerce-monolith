from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    inventory = relationship("Inventory", back_populates="product", uselist=False)
    order_items = relationship("OrderItem", back_populates="product")