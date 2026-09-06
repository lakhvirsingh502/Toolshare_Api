from fastapi import Depends,HTTPException,APIRouter,Query,BackgroundTasks
from sqlalchemy.orm import Session
from app.services.auth import get_current_user
from app.schemas.reservation import ReservationCreate,ReservationResponse,ReservationUpdate
from app.database import get_db
from app.models.user import User
from app.models.reservations import Reservation
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentResponse
from app.services.notifications import send_notification
from app.tasks import send_reservation_email
from celery.result import AsyncResult

router = APIRouter(
    prefix="/reservation",
    tags=["Reservation"]
)

@router.post("/create",response_model=ReservationResponse,status_code=201)
def create_reservation(st:ReservationCreate,db:Session=Depends(get_db),
                       current_user:User=Depends(get_current_user)):
    equipment = db.query(Equipment).filter(Equipment.id == st.equipment_id).first()
    if equipment is None:
        raise HTTPException(
            status_code = 404,
            detail = "Equipment not found."
        )
    if current_user.id == equipment.owner_id:
        raise HTTPException(
            status_code=403,
            detail = "You cant borrow your own tools."
        ) 
    if st.start_date >= st.end_date:
        raise HTTPException (
            status_code = 403,
            detail = "Please put valid dates."
        )
    conflict_reservation = db.query(Reservation).filter(Reservation.equipment_id==st.equipment_id,
                            Reservation.status.in_(["accepted","active"]),Reservation.start_date < st.end_date,
                            Reservation.end_date > st.start_date).first()
   
    if conflict_reservation :
        raise HTTPException(
            status_code=409,
            detail = "This item is already booked for these dates."
        )
                                                         
    new_reservation = Reservation(
        equipment_id = st.equipment_id,
        start_date = st.start_date,
        end_date = st.end_date
    )
    current_user.reservations.append(new_reservation)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

@router.get("/my", response_model=list[ReservationResponse])
def show_my_reservations(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    reservations = db.query(Reservation).filter(Reservation.borrower_id==current_user.id).all()
    return reservations

@router.get("/owner",response_model=list[ReservationResponse])
def show_owner(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    reservation_requests = db.query(Reservation).join(Equipment,Reservation.equipment_id == Equipment.id).filter(
        Equipment.owner_id == current_user.id).all()
    if not reservation_requests:
            raise HTTPException(
                status_code = 404,
                detail = "not found"
            )
  
    return reservation_requests

@router.patch("/{id}/status",response_model=ReservationResponse)
def accept_reject(id:int,st:ReservationUpdate,background_tasks:BackgroundTasks,db:Session=Depends(get_db),
                  current_user:User=Depends(get_current_user)
                  ):
    reservation = db.query(Reservation).filter(Reservation.id == id).first()
    
    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail = "Reservation Not found."
        )
    user = db.query(User).filter(User.id==reservation.borrower_id).first()
    equipment = db.query(Equipment).filter(Equipment.id == reservation.equipment_id).first()
    if equipment.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail = "You are not the owner of this tool."
        )
    allowed_status = ["accepted","rejected"]
    if st.status not in allowed_status:
        raise HTTPException(
            status_code=422,
            detail = "Status must be accepted or rejected."
        )
    
    reservation.status = st.status
   
    if reservation.status == "accepted":
        equipment.is_available = False
       
    if reservation.status == "rejected":
        equipment.is_available = True
    db.commit()
    db.refresh(reservation)
    db.refresh(equipment)
   
    task = send_reservation_email.delay(reservation.id)
    
    
  
    return reservation

@router.patch("/{id}/return",response_model = ReservationResponse)
def return_equipment(id:int,db:Session=Depends(get_db),
                     current_user:User=Depends(get_current_user)):
    
    reservation = db.query(Reservation).filter(Reservation.id == id).first()
    
   
    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail= "Reservation not found."
        )
    if reservation.borrower_id != current_user.id:
            raise HTTPException(
                status_code = 403,
                detail = "You are not authorized."
            )
    
    allowed_status = ["accepted","active"]
    if reservation.status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail = "Return cant be made. "
        )
    reservation.status = "completed"
    equipment = db.query(Equipment).filter(Equipment.id == reservation.equipment_id).first()
    equipment.is_available = True
    db.commit()
    db.refresh(equipment)
    db.refresh(reservation)
    return reservation

@router.patch("/{id}/cancel",response_model=ReservationResponse)
def cancel_equipment(id:int,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if reservation is None:
        raise HTTPException(
            status_code = 404,
            detail = "Reservation not found."
        )
    if reservation.borrower_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail = "You are not authorized"
        )
    allowed_status = ["accepted","pending"]
    
    if reservation.status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail = "This request cant be made."
        )
    
    if reservation.status == "accepted":
        equipment = db.query(Equipment).filter(Equipment.id==reservation.equipment_id).first()
        if equipment is None:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found."
            )
        equipment.is_available=True
    reservation.status="cancelled"
    db.commit()
    db.refresh(reservation)
    
    return reservation


@router.get("/available",response_model=list[EquipmentResponse])
def available_equipment(db:Session = Depends(get_db)):
    equipments = db.query(Equipment).filter(Equipment.is_available == True).all()
    return equipments

@router.get("/search")
def search_filter(skip:int=0,limit:int=10,name:str |None = None,sort_by:str |None=None,
                  category:str|None = None,condition:str|None = None,available_only :bool = False,
                  db:Session=Depends(get_db)):
    query = db.query(Equipment)
    if name:
        query = query.filter(Equipment.name.ilike(f"%{name}%"))
    
    if category:
        category_keywords = ["tools","heavyequipments","agritools","assemblytools"]

        if category not in category_keywords:
            
            raise HTTPException(
                status_code=422,
                detail = "Please type tools,heavyequipments,agritools or assemblytools in searchbox."
            )
        query = query.filter(Equipment.category==category)
                
    if condition:
        condition_keyword = ["good","bad","moderate"] 
        if condition not in condition_keyword:
            
        
            raise HTTPException(
                status_code=422,
                detail="Please put good,bad or moderate in search box."
            )
        query = query.filter(Equipment.condition == condition)
        
    if available_only:
            query = query.filter(Equipment.is_available == True)

    if sort_by:
        if sort_by == "name":
            query = query.order_by(Equipment.name.asc())
        elif sort_by == "created_at":
            query = query.order_by(Equipment.created_at.desc())
    

    return query.offset(skip).limit(limit).all()



    
    

@router.get("/{id}",response_model=ReservationResponse)
def reservations_detail(id:int, db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    reservation = db.query(Reservation).filter(Reservation.id == id).first()
    

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found."
        )
    equipment = db.query(Equipment).filter(Equipment.id == reservation.equipment_id).first()
    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail = "Application not found"
        )
    is_borrower = reservation.borrower_id == current_user.id
    is_owner = equipment.owner_id == current_user.id

    if not is_borrower and not is_owner:
        raise HTTPException(
            status_code=403,
            detail = "You are not authorized to do this action."
        )
    return reservation
    


    
    

