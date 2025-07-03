from fastapi import APIRouter, HTTPException, Depends
from models.product import Product, ProductCreate, PyObjectId
from database import products_collection
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from .dependencies import get_current_user, get_current_admin_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=Product)
async def create_product(
    product: ProductCreate,
    admin_user: dict = Depends(get_current_admin_user)
):
    product_data = product.model_dump()
    product_data["created_at"] = product_data["updated_at"] = datetime.now()
    result = await products_collection.insert_one(product_data)
    created_product = await products_collection.find_one({"_id": result.inserted_id})
    if created_product:
        created_product["id"] = str(created_product["_id"])
        del created_product["_id"]
        return Product(**created_product)
    raise HTTPException(status_code=500, detail="Product creation failed")

@router.get("/", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    query = {"category": category} if category else {}
    products = []
    async for product in products_collection.find(query):
        product["id"] = str(product["_id"])
        del product["_id"]
        products.append(Product(**product))
    return products

@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: str,
    user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["id"] = str(product["_id"])
    del product["_id"]
    return Product(**product)

@router.put("/{product_id}")
async def update_product(
    product_id: str,
    product: ProductCreate,
    admin_user: dict = Depends(get_current_admin_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    update_data = product.dict()
    update_data["updated_at"] = datetime.now()
    result = await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    admin_user: dict = Depends(get_current_admin_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    result = await products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}