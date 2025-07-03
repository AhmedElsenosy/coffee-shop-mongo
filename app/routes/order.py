from fastapi import APIRouter, Depends, HTTPException
from models.order import Order, OrderItem
from database import orders_collection, order_items_collection, cart_collection, products_collection
from bson import ObjectId
from datetime import datetime
from typing import List
from .dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/from-cart", response_model=Order)
async def create_order_from_cart(user: dict = Depends(get_current_user)):
    cart_items = []
    async for item in cart_collection.find({"user_id": user["id"]}):
        cart_items.append(item)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0
    order_items = []
    for item in cart_items:
        product = await products_collection.find_one({"_id": ObjectId(item["product_id"])})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item['product_id']} not found")
        price = product.get("price", 0)
        total_price += price * item["quantity"]
        order_items.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": price
        })

    order_doc = {
        "user_id": user["id"],
        "total_price": total_price,
        "status": "Pending",
        "created_at": datetime.utcnow()
    }
    order_result = await orders_collection.insert_one(order_doc)
    order_id = str(order_result.inserted_id)

    items_to_insert = []
    for item in order_items:
        item_doc = {
            "order_id": order_id,
            **item
        }
        items_to_insert.append(item_doc)
    await order_items_collection.insert_many(items_to_insert)

    await cart_collection.delete_many({"user_id": user["id"]})

    db_items = []
    async for db_item in order_items_collection.find({"order_id": order_id}):
        db_item["id"] = str(db_item["_id"])
        del db_item["_id"]
        db_items.append(OrderItem(**db_item))

    return Order(
        id=order_id,
        user_id=user["id"],
        total_price=total_price,
        status="Pending",
        created_at=order_doc["created_at"],
        items=db_items
    )