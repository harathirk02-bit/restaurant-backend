from pydantic import BaseModel

class OrderBase(BaseModel):
    item_id: int
    user_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: str

class OrderResponse(OrderBase):
    id: int
    status: str

    class Config:
        from_attributes = True