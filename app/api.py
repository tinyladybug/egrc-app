from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Create a metric
@router.post("/metrics/", response_model=schemas.MetricResponse)
def create_metric(metric: schemas.MetricCreate, db: Session = Depends(get_db)):
    new_metric = models.Metric(**metric.model_dump())
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric

# Get all metrics
@router.get("/metrics/", response_model=list[schemas.MetricResponse])
def get_metrics(db: Session = Depends(get_db)):
    metrics = db.query(models.Metric).all()
    return [schemas.MetricResponse(
        id=metric.id,
        name=metric.name,
        value=metric.latest_value if metric.latest_value is not None else 0.0,  # Ensure float value
        description=metric.description,
        unit=metric.unit,
        status=metric.status,
        warning_threshold=metric.warning_threshold,
        limit_threshold=metric.limit_threshold,
        risk_type=metric.risk_type,
        business_unit=metric.business_unit,
        created_by=metric.created_by,
        created_at=metric.created_at,
        updated_at=metric.updated_at
    ) for metric in metrics]

# Get a single metric by ID
@router.get("/metrics/{id}", response_model=schemas.MetricResponse)
def get_metric(id: int, db: Session = Depends(get_db)):
    metric = db.query(models.Metric).filter(models.Metric.id == id).first()
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    return schemas.MetricResponse(
        id=metric.id,
        name=metric.name,
        value=metric.latest_value if metric.latest_value is not None else 0.0,
        description=metric.description,
        unit=metric.unit,
        status=metric.status,
        warning_threshold=metric.warning_threshold,
        limit_threshold=metric.limit_threshold,
        risk_type=metric.risk_type,
        business_unit=metric.business_unit,
        created_by=metric.created_by,
        created_at=metric.created_at,
        updated_at=metric.updated_at
    )

# Update a metric
@router.put("/metrics/{id}", response_model=schemas.MetricResponse)
def update_metric(id: int, updated_metric: schemas.MetricUpdate, db: Session = Depends(get_db)):
    metric = db.query(models.Metric).filter(models.Metric.id == id).first()
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    for key, value in updated_metric.model_dump(exclude_unset=True).items():
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



# ------------------- Metric Results API -------------------

# Create a new metric result
@router.post("/metrics/{metric_id}/results/", response_model=schemas.MetricResultResponse)
def create_metric_result(result: schemas.MetricResultCreate, metric_id: int, db: Session = Depends(get_db)):
    # Check if the metric exists
    metric = db.query(models.Metric).filter(models.Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")

    # Create a new MetricResult using the result data
    new_result = models.MetricResult(
        metric_id=metric_id,  # Pass the metric_id explicitly
        value=result.value
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result

# Get all results for a specific metric
@router.get("/metrics/{metric_id}/results/", response_model=list[schemas.MetricResultResponse])
def get_metric_results(metric_id: int, db: Session = Depends(get_db)):
    results = db.query(models.MetricResult).filter(models.MetricResult.metric_id == metric_id).order_by(models.MetricResult.timestamp.desc()).all()
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this metric")
    return results

# Get the latest result for a specific metric
@router.get("/metrics/{metric_id}/results/latest/", response_model=schemas.MetricResultResponse)
def get_latest_metric_result(metric_id: int, db: Session = Depends(get_db)):
    latest_result = db.query(models.MetricResult).filter(models.MetricResult.metric_id == metric_id).order_by(models.MetricResult.timestamp.desc()).first()
    if not latest_result:
        raise HTTPException(status_code=404, detail="No results found for this metric")
    return latest_result

# Update a specific metric result
@router.put("/results/{result_id}", response_model=schemas.MetricResultResponse)
def update_metric_result(result_id: int, updated_result: schemas.MetricResultUpdate, db: Session = Depends(get_db)):
    result = db.query(models.MetricResult).filter(models.MetricResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Metric result not found")
    
    for key, value in updated_result.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    
    db.commit()
    db.refresh(result)
    return result

# Delete a metric result
@router.delete("/results/{result_id}")
def delete_metric_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(models.MetricResult).filter(models.MetricResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Metric result not found")
    
    db.delete(result)
    db.commit()
    return {"message": "Metric result deleted successfully"}