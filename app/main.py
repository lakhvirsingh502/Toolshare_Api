from fastapi import FastAPI
from app.routers.user import router as users_router
from app.database import Base
from app.database import engine
from app.models.user import User
from app.routers.review import router as review_router
from app.routers.equipment import router as equipment_router
from app.routers.reservation import router as reservation_router

app = FastAPI(
    title = "ToolShare Api",
    version = "1.0.0"

)
@app.get("/")
def home():
    return{
        "message":"Hello World!"
    }

app.include_router(users_router)
app.include_router(equipment_router)
app.include_router(review_router)
app.include_router(reservation_router)