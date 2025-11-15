from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Manually define the database URL
# NOTE: Replace 'mydatabase' with your actual password if it's different
DATABASE_URL = "postgresql://postgres:mydatabase@localhost:5432/healthlinkdb"

print("DATABASE URL:", DATABASE_URL)  # This will now print the URL string

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# You can remove the unused imports:
# import os
# from dotenv import load_dotenv
# load_dotenv()