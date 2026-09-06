from sqlalchemy import Column, Integer, ForeignKey, String,DateTime,Boolean
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True,nullable=False)
    hashed_password = Column(String,nullable=False,)
    role = Column(String, default = "user",nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default =datetime.utcnow,nullable=False)
    equipments = relationship("Equipment", back_populates="user")
    reservations = relationship("Reservation",back_populates="user")
    reviews = relationship("Review",back_populates="user")

