from fastapi import FastAPI

from database import Base, engine

from routers.menu import router as menu_router
from routers.auth import router as auth_router
from routers.orders import router as orders_router

# IMPORT MODELS
from models.user import User
from models.menu_item import MenuItem
from models.order import Order

# CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Menu Manager API"
)

# INCLUDE ROUTERS
app.include_router(menu_router)
app.include_router(auth_router)
app.include_router(orders_router)

@app.get("/")
def home():
    return {
        "message": "Restaurant API Running"
    }