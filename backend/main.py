import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ⬅️ ADD THIS
from .database import Base, engine

# ⚠️ IMPORTANT: Import models BEFORE create_all()
from .models_insurance import InsuranceClaim  
from .models import Patient

# Database setup (creates tables)
Base.metadata.create_all(bind=engine)

# FastAPI app
from .routes import auth_routes, report_routes, insurance_routes
app = FastAPI(title="HealthLink Backend")

# ⬇️ ADD CORS MIDDLEWARE HERE ⬇️
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins like ["http://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Route registration
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(report_routes.router)
app.include_router(insurance_routes.router)