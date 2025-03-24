from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Create a metric
@router.post("/metrics/", response_model=schemas.MetricResponse)
def create_metric(metric: schemas.MetricCreate, db: Session = Depends(get_db)):
    new_metric = models.Metric(**metric.dict())
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric

# Get all metrics
@router.get("/metrics/", response_model=list[schemas.MetricResponse])
def get_metrics(db: Session = Depends(get_db)):
    return db.query(models.Metric).all()

# Get a single metric by ID
@router.get("/metrics/{id}", response_model=schemas.MetricResponse)
def get_metric(id: int, db: Session = Depends(get_db)):
    metric = db.query(models.Metric).filter(models.Metric.id == id).first()
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

# Update a metric
@router.put("/metrics/{id}", response_model=schemas.MetricResponse)
def update_metric(id: int, updated_metric: schemas.MetricUpdate, db: Session = Depends(get_db)):
    metric = db.query(models.Metric).filter(models.Metric.id == id).first()
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    for key, value in updated_metric.dict(exclude_unset=True).items():
        setattr(metric, key, value)
    db.commit()
    db.refresh(metric)
    return metric

# Delete a metric
@router.delete("/metrics/{id}")
def delete_metric(id: int, db: Session = Depends(get_db)):
    metric = db.query(models.Metric).filter(models.Metric.id == id).first()
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(metric)
    db.commit()
    return {"message": "Metric deleted successfully"}
