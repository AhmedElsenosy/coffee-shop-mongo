from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: str
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: Optional[str] = Field(default=None, alias="_id")
    order_id: str

    class Config:
        populate_by_name = True

class OrderBase(BaseModel):
    total_price: float
    status: str = "Pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    created_at: datetime
    items: List[OrderItem]

    class Config:
        populate_by_name = True