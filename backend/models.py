from .database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String, index=True)
    ipfs_cid = Column(String)
    file_hash = Column(String)
    tx_hash = Column(String)
    enc_file_key = Column(Text)
    file_name = Column(String)
    uploaded_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    claim_id = Column(String, unique=True)
    patient_id = Column(String)
    ipfs_cid = Column(String)
    status = Column(String, default="PENDING")
    amount = Column(Integer, default=0)
    tx_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # --- ADDED COLUMN ---
    fraud_score = Column(Integer, default=0)
    # --------------------