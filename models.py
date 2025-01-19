from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    diagnosis_code = Column(String, nullable=False)
    procedure_code = Column(String, nullable=False)
    claim_amount = Column(Float, nullable=False)
    status = Column(String, default="PENDING")  # Default status
    submitted_at = Column(DateTime, default=datetime.utcnow)  # Auto timestamp
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")