# app/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    application_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    loan_amount = Column(Float)
    loan_purpose = Column(String)
    duration = Column(Integer)
    status = Column(String, default="pending")
    submission_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
