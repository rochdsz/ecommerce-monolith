from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.inventory import Inventory

router = APIRouter()

class InventoryOut(BaseModel):
    product_id: int
    quantity: int
    updated_at: datetime
    class Config:
        from_attributes = True

class InventoryUpdate(BaseModel):
    quantity: int

@router.get("/{product_id}", response_model=InventoryOut)
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found for this product")
    return inv

@router.put("/{product_id}", response_model=InventoryOut)
def update_stock(product_id: int, payload: InventoryUpdate, db: Session = Depends(get_db)):
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    inv.quantity = payload.quantity
    db.commit()
    db.refresh(inv)
    return inv