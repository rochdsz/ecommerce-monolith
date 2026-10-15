from pydantic import BaseModel
from decimal import Decimal
from typing import List
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: OrderStatus
    class Config:
        from_attributes = True