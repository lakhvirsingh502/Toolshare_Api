import bcrypt
from jose import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from app.database import get_db
from app.models.user import User 
security = HTTPBearer()
SECRET_KEY = "123456"
def create_hash_password(password:str):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verify_hash_password(password:str,hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),hashed_password.encode("utf-8")

    )

def create_token(id:int):
   
    data = {
        "user_id":id
    }
    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm="HS256"

    )
def verify_token(token):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms="HS256"
    )
def get_current_user(credentials = Depends(security),db:Session = Depends(get_db)):
    token = credentials.credentials
    data = verify_token(token)
    current_user = db.query(User).filter(User.id == data["user_id"]).first()
    if current_user is None:
        raise HTTPException(
            status_code=404,
            detail = "User Not Found."
        )
    return current_user

