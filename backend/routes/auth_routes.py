from fastapi import APIRouter, HTTPException, Depends, Form
from ..database import SessionLocal
from ..models import Patient
from ..utils.crypto_utils import hash_password, verify_password
from ..utils.jwt_utils import create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import random, string
def generate_patient_id():
    return "P-" + ''.join(random.choices(string.digits, k=6))

@router.post("/register_patient")
def register_patient(
    name: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):

    # 1. Create unique patient ID
    patient_id = generate_patient_id()

    # 2. Hash password
    hashed_pw = hash_password(password)

    # 3. Save into PostgreSQL
    new_patient = Patient(
        patient_id=patient_id,
        name=name,
        phone=phone,
        password_hash=hashed_pw
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {
        "status": "success",
        "patient_id": patient_id,
        "message": "Patient registered successfully"
    }
@router.post("/login")
def login(
    phone: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):

    # 1. Fetch user
    user = db.query(Patient).filter(Patient.phone == phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="Patient not found")

    # 2. Verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # 3. Generate JWT token
    access_token = create_access_token(
        {"user_id": user.id, "patient_id": user.patient_id}
    )

    return {
        "status": "success",
        "message": "Login successful",
        "access_token": access_token
    }