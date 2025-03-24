from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Metrics

def insert_test_data():
    db: Session = SessionLocal()

    new_metric = Metrics(
        name="CPU Usage",
        value=75.3
    )

    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    print(f"✅ Inserted metric: {new_metric.id} - {new_metric.name} = {new_metric.value}")

    db.close()

if __name__ == "__main__":
    insert_test_data()
