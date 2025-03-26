from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router  # Import the router
from app.database import engine, Base

app = FastAPI()

# Ensure tables are created
Base.metadata.create_all(bind=engine)

# Include the API router
app.include_router(router)

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the eGRC API"}
