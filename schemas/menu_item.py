from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    available: bool

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True