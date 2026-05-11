from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.order import Order

from schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# DATABASE CONNECTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET ALL ORDERS
@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db)
):
    return db.query(Order).all()

# PLACE ORDER
@router.post(
    "/",
    response_model=OrderResponse
)
def place_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    new_order = Order(**order.model_dump())

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

# GET MY ORDERS
@router.get(
    "/me",
    response_model=list[OrderResponse]
)
def get_my_orders(
    user_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Order).filter(
        Order.user_id == user_id
    ).all()

# UPDATE ORDER STATUS
@router.put(
    "/{order_id}",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    updated_order: OrderUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = updated_order.status

    db.commit()
    db.refresh(order)

    return order