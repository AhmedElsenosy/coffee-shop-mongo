from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class CartItemBase(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}