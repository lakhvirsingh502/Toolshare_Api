from pydantic import BaseModel,EmailStr
from datetime import datetime
from sqlalchemy import DateTime
class UserCreate(BaseModel):
    name:str
    email:str
    password:str

class UserLogin(BaseModel):
    password:str
    email:EmailStr

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    role:str
    is_active:bool
    created_at:datetime

    model_config = {"from_attributes": True}