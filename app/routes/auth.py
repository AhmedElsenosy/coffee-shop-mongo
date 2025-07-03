from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import UserCreate, UserLogin, UserInDB
from database import users_collection
from utils.security import hash_password, verify_password, create_access_token
from datetime import datetime , timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/signup", response_model=UserInDB)
async def signup(user: UserCreate):
    
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "is_admin": False,  
        "created_at": datetime.now()
    }
    
    result = await users_collection.insert_one(user_data)
    return {**user_data, "id": str(result.inserted_id)}

@router.post("/login")
async def login(user: UserLogin):  
    found_user = await users_collection.find_one({"email": user.email})
    if not found_user or not verify_password(user.password, found_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": found_user["email"], "is_admin": found_user["is_admin"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}