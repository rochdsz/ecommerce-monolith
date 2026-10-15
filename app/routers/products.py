from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.models.inventory import Inventory
from app.schemas.product import ProductCreate, ProductOut

router = APIRouter()

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.sku == product_in.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")

    product = Product(
        title=product_in.title,
        description=product_in.description,
        price=product_in.price,
        sku=product_in.sku
    )
    db.add(product)
    db.flush()

    inv = Inventory(product_id=product.id, quantity=product_in.initial_stock)
    db.add(inv)

    db.commit()
    db.refresh(product)
    return product

@router.get("", response_model=List[ProductOut])
def list_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product