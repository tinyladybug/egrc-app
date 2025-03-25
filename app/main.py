from fastapi import FastAPI
from app.api import router  # Import the router
from app.database import engine, Base

app = FastAPI()

# Ensure tables are created
Base.metadata.create_all(bind=engine)

# Include the API router
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the eGRC API"}
