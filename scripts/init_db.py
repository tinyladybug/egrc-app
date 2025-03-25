from app.database import engine, Base
from app import models  # ✅ Make sure this is imported!

Base.metadata.drop_all(bind=engine)  # Drop tables (caution: deletes data)
Base.metadata.create_all(bind=engine)  # Recreate tables

print("✅ Tables dropped and recreated successfully!")
