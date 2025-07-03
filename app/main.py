from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.products import router as products_router
from routes.cart import router as cart_router
from routes.order import router as order_router

from database import client  

app = FastAPI()

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    await client.close()