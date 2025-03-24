from fastapi import FastAPI
from app.api import router  # Import the router

app = FastAPI()

# Include the API router
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the eGRC API"}
