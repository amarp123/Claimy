from sqlalchemy import Column, String, Integer, Text
from backend.database import Base

class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String, unique=True, index=True)
    patient_id = Column(String, index=True)
    documents_cid = Column(String)
    extracted_data = Column(Text)
    status = Column(String)

    # ---- AI Extracted Fields ----
    patient_name = Column(String, nullable=True)
    diagnosis = Column(String, nullable=True)
    treatment = Column(String, nullable=True)
    total_bill = Column(String, nullable=True)

    # Fraud detection score
    fraud_score = Column(String, nullable=True)
