from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    item_id = Column(
        Integer,
        ForeignKey("menu_items.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    status = Column(
        String,
        default="Pending"
    )