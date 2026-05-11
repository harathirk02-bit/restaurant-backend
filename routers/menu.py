from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.menu_item import MenuItem
from schemas.menu_item import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse
)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)

# DATABASE CONNECTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TOKEN SECURITY
security = HTTPBearer()

# VERIFY TOKEN
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )
    return token

# GET ALL MENU ITEMS
@router.get("/", response_model=list[MenuItemResponse])
def get_menu_items(db: Session = Depends(get_db)):
    items = db.query(MenuItem).all()
    return items

# ADD MENU ITEM
@router.post("/", response_model=MenuItemResponse)
def create_menu_item(
    item: MenuItemCreate,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    new_item = MenuItem(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# UPDATE MENU ITEM
@router.put("/{item_id}", response_model=MenuItemResponse)
def update_menu_item(
    item_id: int,
    updated_item: MenuItemUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )
    for key, value in updated_item.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

# DELETE MENU ITEM
@router.delete("/{item_id}")
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )
    db.delete(item)
    db.commit()
    return {"message": "Menu item deleted successfully"}
