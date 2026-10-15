import uuid
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.order import Order, OrderItem, OrderStatus
from app.models.payment import Payment, PaymentStatus
from app.schemas.order import OrderCreate

def process_checkout(db: Session, user_id: int, order_data: OrderCreate) -> Order:
    if not order_data.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    try:
        total_amount = Decimal("0.00")
        order_items_to_create = []

        for item in order_data.items:
            # Row-level lock on inventory to prevent race conditions
            inv = db.query(Inventory).filter(Inventory.product_id == item.product_id).with_for_update().first()
            if not inv or inv.quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient inventory for product ID {item.product_id}"
                )

            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

            # Deduct stock
            inv.quantity -= item.quantity
            item_total = product.price * item.quantity
            total_amount += item_total

            order_items_to_create.append(
                OrderItem(product_id=product.id, quantity=item.quantity, price=product.price)
            )

        # 1. Create Order
        order = Order(user_id=user_id, total_amount=total_amount, status=OrderStatus.CONFIRMED)
        db.add(order)
        db.flush()  # Generates order.id

        # 2. Attach items
        for order_item in order_items_to_create:
            order_item.order_id = order.id
            db.add(order_item)

        # 3. Simulate and attach Payment record
        payment = Payment(
            order_id=order.id,
            amount=total_amount,
            status=PaymentStatus.SUCCESS,
            transaction_id=f"tx_{uuid.uuid4().hex[:12]}"
        )
        db.add(payment)

        # Commit entire unit of work
        db.commit()
        db.refresh(order)
        return order

    except Exception:
        db.rollback()
        raise