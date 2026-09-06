from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Boolean

class EquipmentCreate(BaseModel):
    name:str
    description:str
    category:str
    condition:str

class EquipmentUpdate(BaseModel):
    name:str | None = None
    description:str | None = None
    category:str | None = None
    condition:str | None = None
    is_available:bool | None = None

class EquipmentResponse(BaseModel):
    id : int
    name : str
    description : str
    category : str
    condition : str
    is_available : bool
    created_at : datetime
    owner_id : int

    model_config={"from_attributes":True}

