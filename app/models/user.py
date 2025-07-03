from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  

class UserInDB(UserBase):
    id: str
    is_admin: bool = False  
    created_at: datetime = datetime.now()

class UserLogin(BaseModel):
    email: EmailStr
    password: str