from fastapi import Depends,APIRouter,HTTPException
from sqlalchemy.orm import Session
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate,EquipmentResponse,EquipmentUpdate
from app.database import get_db
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"]
    
)
@router.post("/create" ,response_model=EquipmentResponse,status_code=201)
def create_equipment(st:EquipmentCreate,db:Session=Depends(get_db),
                     current_user:User=Depends(get_current_user)):
    
        
    new_equipment = Equipment(
        name = st.name,
        description = st.description,
        category = st.category,
        condition = st.condition,
        
        
    )
    current_user.equipments.append(new_equipment)
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    return new_equipment
@router.get("/all",response_model=list[EquipmentResponse])
def show_all_equipments(db:Session = Depends(get_db)):
    return db.query(Equipment).all()


@router.get("/my",response_model=list[EquipmentResponse])
def my_equipment(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    my_equipments = db.query(Equipment).filter(Equipment.owner_id==current_user.id).all()
    if not my_equipments:
        raise HTTPException(
            status_code = 404,
            detail = "Equipments not found."
        )
    return my_equipments


@router.get("/{id}",response_model=EquipmentResponse)
def show_by_id(id:int,db:Session=Depends(get_db)):
    equipments = db.query(Equipment).filter(Equipment.id == id).first()
    if equipments is None:
        raise HTTPException(
            status_code = 404,
            detail = "equipments not found."
        )
    return equipments

@router.patch("/update/{id}",response_model=EquipmentResponse)
def update_equipment(id:int,st:EquipmentUpdate,db:Session = Depends(get_db),
                     current_user:User=Depends(get_current_user)):
    equipment = db.query(Equipment).filter(Equipment.id == id).first()
    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail = "Equipment not found."
        )
    if equipment.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail = "You are not authorized to do this action."
        )
    data_update = st.model_dump(exclude_unset=True)
    for field, value in data_update.items():
        setattr(equipment,field,value)

    
    db.commit()
    db.refresh(equipment)
    return equipment
@router.delete("/{id}")
def delete_equipment(id:int,db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    equipment = db.query(Equipment).filter(Equipment.id == id).first()
    if equipment is None:
        raise HTTPException(
            status_code = 404,
            detail =  "Application not found."
        )
    if current_user.id != equipment.owner_id:
        raise HTTPException(
            status_code = 403,
            detail = "You are not authorized to do this actions."
        )
    db.delete(equipment)
    db.commit()
    return{
        "message":"Application deleted successfully."
    }
