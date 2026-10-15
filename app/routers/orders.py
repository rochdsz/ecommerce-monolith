from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import process_checkout

router = APIRouter()

@router.post("", response_model=OrderOut, status_code=201)
def create_order(
    order_in: OrderCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return process_checkout(db=db, user_id=current_user_id, order_data=order_in)

@router.get("", response_model=List[OrderOut])
def get_user_orders(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return db.query(Order).filter(Order.user_id == current_user_id).all()