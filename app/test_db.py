from app.database import SessionLocal
from sqlalchemy.sql import text  # Import text() function

# Create a new database session
db = SessionLocal()

try:
    # Run a simple test query
    result = db.execute(text("SELECT 1"))  # Wrap raw SQL in text()
    print("✅ Database connection successful:", result.fetchone())
except Exception as e:
    print("❌ Database connection failed:", e)
finally:
    db.close()
