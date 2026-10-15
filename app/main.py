import os
from contextlib import asynccontextmanager
from decimal import Decimal
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.database import Base, engine, SessionLocal
from app.models.product import Product
from app.models.inventory import Inventory
from app.routers import auth, products, inventory, orders, payments

def seed_initial_products():
    """Seeds default products and stock if the table is empty."""
    db = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            sample_products = [
                {"title": "Wireless Noise-Canceling Headphones", "description": "Over-ear comfort with active ANC.", "price": Decimal("149.99"), "sku": "HP-ANC-1", "stock": 25},
                {"title": "Ergonomic Mechanical Keyboard", "description": "Tactile brown switches with USB-C cable.", "price": Decimal("89.50"), "sku": "KB-MEC-4", "stock": 40},
                {"title": "4K Ultra-HD Monitor 27-inch", "description": "IPS panel with HDR400 and tilt stand.", "price": Decimal("319.00"), "sku": "MON-4K-27", "stock": 15},
                {"title": "Ergonomic Desk Chair", "description": "Lumbar support with breathable mesh back.", "price": Decimal("210.00"), "sku": "CHR-ERG-9", "stock": 12},
                {"title": "Wireless Gaming Mouse", "description": "High precision sensor with rechargeable battery.", "price": Decimal("49.99"), "sku": "MOU-WL-01", "stock": 50}
            ]
            for item in sample_products:
                prod = Product(
                    title=item["title"],
                    description=item["description"],
                    price=item["price"],
                    sku=item["sku"]
                )
                db.add(prod)
                db.flush()
                
                inv = Inventory(product_id=prod.id, quantity=item["stock"])
                db.add(inv)

            db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and seed data
    Base.metadata.create_all(bind=engine)
    seed_initial_products()
    yield

app = FastAPI(title="Apex Store", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def serve_ui():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}