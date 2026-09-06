from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import DateTime

class ReservationCreate(BaseModel):
    equipment_id:int
    start_date:datetime
    end_date:datetime
    

class ReservationUpdate(BaseModel):
    status:str

class ReservationResponse(BaseModel):
    id:int
    equipment_id:int
    borrower_id:int
    start_date:datetime
    end_date:datetime
    status:str
    created_at:datetime

    model_config={
        "from_attributes":True
    }