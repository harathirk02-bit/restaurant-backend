from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String(50), default="Main Course")
    available = Column(Boolean, default=True)