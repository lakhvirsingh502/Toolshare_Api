from fastapi import FastAPI,Depends,HTTPException,APIRouter
from app.schemas.review import CreateReview,ReviewResponse,UpdateReview
from app.models.review import Review 
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth import get_current_user
from app.models.reservations import Reservation

router = APIRouter(
    prefix="/review",
    tags=["Review"]
)

@router.post("/post",response_model=ReviewResponse)
def create_review(st:CreateReview,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    reservation = db.query(Reservation).filter(Reservation.id == st.reservation_id).first()
    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="reservation not found."
        )
    if reservation.borrower_id!=current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed to do this action."
        )
    if reservation.status != "completed":
        raise HTTPException(
            status_code=409,
            detail="For this reservation review is not allowed."
        )
    review = db.query(Review).filter(Review.reservation_id==st.reservation_id).first()
    if review:
        raise HTTPException(
            status_code=400,
            detail = "This reservation has already being reviewed."
        )
    new_review=Review(
        reservation_id = st.reservation_id,
        rating = st.rating,
        comment = st.comment,
        equipment_id = reservation.equipment_id
    )
    current_user.reviews.append(new_review)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
@router.get("/equipment/{id}", response_model=list[ReviewResponse])
def show_reviews(id:int,db:Session=Depends(get_db)):
    equipment_reviews = db.query(Review).filter(Review.equipment_id==id).all()
    return equipment_reviews
@router.get("/my",response_model=list[ReviewResponse])
def show_my_reviews(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    my_reviews = db.query(Review).filter(Review.reviewer_id==current_user.id).all()
    if not my_reviews:
        raise HTTPException(
            status_code=404,
            detail="not found"
        )
    return my_reviews
@router.delete("/delete/{id}")
def delete_review(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    review = db.query(Review).filter(Review.id==id).first()
    if review is None:
        raise HTTPException(
            status_code=404,
            detail = "Review not found."
        )
    if current_user.id!= review.reviewer_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to do this action."
        )
    db.delete(review)
    db.commit()
    return{
        "message":"Review deleted successfully."
    }

@router.patch("/update/{id}")
def update_review(st:UpdateReview,id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    review=db.query(Review).filter(Review.id==id).first()
    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found."
        )
    if current_user.id != review.reviewer_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to do this action."
        )
    update_data = st.model_dump(exclude_unset=True)
    for field,values in update_data.items():
        setattr(review,field,values)

    db.commit()
    db.refresh(review)
    return review
    
        
