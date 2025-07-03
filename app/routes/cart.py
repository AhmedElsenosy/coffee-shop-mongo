from fastapi import APIRouter, Depends, HTTPException
from models.cart import CartItem, CartItemCreate
from database import cart_collection, products_collection
from bson import ObjectId
from typing import List
from .dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=CartItem)
async def add_to_cart(
    item: CartItemCreate,
    user: dict = Depends(get_current_user)
):
    product = await products_collection.find_one({"_id": ObjectId(item.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    cart_item = {
        "user_id": user["id"],
        "product_id": item.product_id,
        "quantity": item.quantity
    }
    result = await cart_collection.insert_one(cart_item)
    cart_item["_id"] = str(result.inserted_id)  
    return CartItem(**cart_item)

@router.get("/", response_model=List[CartItem])
async def get_cart(user: dict = Depends(get_current_user)):
    items = []
    async for item in cart_collection.find({"user_id": user["id"]}):
        item["id"] = str(item["_id"])
        del item["_id"]
        items.append(CartItem(**item))
    return items

@router.delete("/{cart_item_id}")
async def remove_from_cart(cart_item_id: str, user: dict = Depends(get_current_user)):
    result = await cart_collection.delete_one({
        "_id": ObjectId(cart_item_id),
        "user_id": user["id"]
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}