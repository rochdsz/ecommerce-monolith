from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

from app.core.database import get_db
from app.models.payment import Payment, PaymentStatus

router = APIRouter()

class PaymentOut(BaseModel):
    id: int
    order_id: int
    amount: Decimal
    status: PaymentStatus
    transaction_id: str
    created_at: datetime
    class Config:
        from_attributes = True

@router.get("/{order_id}", response_model=PaymentOut)
def get_payment_by_order(order_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.order_id == order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")
    return payment