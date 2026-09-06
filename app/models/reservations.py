from sqlalchemy import Column,String,Integer,ForeignKey,DateTime

from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Boolean
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer,primary_key=True,index=True,unique=True)
    equipment_id = Column(Integer,ForeignKey("equipments.id"),nullable=False)
    borrower_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    start_date= Column(DateTime, default=datetime.utcnow,nullable=False)
    end_date = Column(DateTime,nullable=False)
    created_at = Column(DateTime,default = datetime.utcnow,nullable = False)
    status = Column(String,nullable=False,default = "pending")
    user = relationship("User",back_populates="reservations")
    equipments = relationship("Equipment",back_populates="reservations")
    reviews = relationship("Review",back_populates="reservation",uselist=False)
    reminder_sent = Column(Boolean, default=False)

