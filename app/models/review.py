from sqlalchemy import Column,Integer,ForeignKey,String,DateTime
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer,primary_key=True,index=True)
    equipment_id = Column(Integer,ForeignKey("equipments.id"),nullable=False)
    reviewer_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    reservation_id = Column(Integer,ForeignKey("reservations.id"),nullable=False)
    rating = Column(Integer,nullable=False)
    comment = Column(String,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow,nullable=False)
    user = relationship("User",back_populates="reviews")
    equipment = relationship("Equipment",back_populates="reviews")
    reservation = relationship("Reservation",back_populates="reviews")