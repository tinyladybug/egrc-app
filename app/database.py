from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the Database URL (Update with your password if needed)
DATABASE_URL = "postgresql://postgres:131212314@localhost/egrc_db"

# Create the Database Engine
engine = create_engine(DATABASE_URL)

# Create a Session for interacting with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency function to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
