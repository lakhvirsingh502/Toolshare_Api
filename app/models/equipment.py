from sqlalchemy import Column, String, Integer, ForeignKey, Boolean,DateTime
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, nullable=False, primary_key=True,index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    condition = Column(String, nullable=True, default="good")
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default = datetime.utcnow,nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    user = relationship("User",back_populates="equipments")
    reservations = relationship("Reservation", back_populates="equipments")
    reviews = relationship("Review",back_populates="equipment")