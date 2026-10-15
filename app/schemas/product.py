from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: Decimal
    sku: str
    initial_stock: int = 0

class ProductOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: Decimal
    sku: str
    class Config:
        from_attributes = True