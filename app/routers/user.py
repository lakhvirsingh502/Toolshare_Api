from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,APIRouter,HTTPException
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.schemas.user import UserLogin
from app.services.auth import get_current_user
from app.services.auth import create_hash_password, verify_hash_password, create_token
from app.rate_limiter import rate_limiter


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/register", response_model=UserResponse, status_code=201)
def create_user(st:UserCreate ,db:Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == st.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exist."
        )
    password = create_hash_password(st.password)
    new_user = User(
        name = st.name,
        email = st.email,
        hashed_password = password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post("/login")
async def create_login(st:UserLogin,db:Session = Depends(get_db),_:None=Depends(rate_limiter)):
    existing_user = db.query(User).filter(User.email == st.email).first()
    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail = "Invalid email or password."
        )
    password = verify_hash_password(st.password,existing_user.hashed_password)
    if not password:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid email or password."
        )
   

    token = create_token(existing_user.id)
    return{
        "Token":token
        }
