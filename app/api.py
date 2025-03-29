from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from datetime import datetime

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
        type=metric.type,
        level=metric.level,
        description=metric.description,
        unit=metric.unit,
        status=metric.status,
        warning_threshold=metric.warning_threshold,
        limit_threshold=metric.limit_threshold,
        risk_type_id=metric.risk_type_id,
        risk_type=metric.risk_type.name if metric.risk_type.name else None ,
        business_unit_id=metric.business_unit_id,
        business_unit=metric.business_unit.name if metric.business_unit.name else None ,
        latest_value=metric.latest_value if metric.latest_value is not None else 0.0,
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
        type=metric.type,
        level=metric.level,
        description=metric.description,
        unit=metric.unit,
        status=metric.status,
        warning_threshold=metric.warning_threshold,
        limit_threshold=metric.limit_threshold,
        risk_type_id=metric.risk_type_id,
        risk_type=metric.risk_type.name if metric.risk_type.name else None ,
        business_unit_id=metric.business_unit_id,
        business_unit=metric.business_unit.name if metric.business_unit.name else None ,
        latest_value=metric.latest_value if metric.latest_value is not None else 0.0,
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
def create_metric_result_for_specific_metric(result: schemas.MetricResultCreate, metric_id: int, db: Session = Depends(get_db)):
    # Check if the metric exists
    metric = db.query(models.Metric).filter(models.Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")

    # Create a new MetricResult using the result data
    new_result = models.MetricResult(
        metric_id=metric_id,  # Pass the metric_id explicitly
        value=result.value,
        uploaded_by=result.uploaded_by,

    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result

# Get all results for a specific metric
@router.get("/metrics/{metric_id}/results/", response_model=list[schemas.MetricResultResponse])
def get_all_metric_results_for_specific_metric(metric_id: int, db: Session = Depends(get_db)):
    results = db.query(models.MetricResult).filter(models.MetricResult.metric_id == metric_id).order_by(models.MetricResult.uploaded_at.desc()).all()
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this metric")
    return results

# Get the latest result for a specific metric
@router.get("/metrics/{metric_id}/results/latest/", response_model=schemas.MetricResultResponse)
def get_latest_metric_result_for_specific_metric(metric_id: int, db: Session = Depends(get_db)):
    latest_result = db.query(models.MetricResult).filter(models.MetricResult.metric_id == metric_id).order_by(models.MetricResult.uploaded_at.desc()).first()
    if not latest_result:
        raise HTTPException(status_code=404, detail="No results found for this metric")
    return latest_result

# Update a specific metric result
@router.put("/results/{result_id}", response_model=schemas.MetricResultResponse)
def update_specific_metric_result(result_id: int, updated_result: schemas.MetricResultUpdate, db: Session = Depends(get_db)):
    result = db.query(models.MetricResult).filter(models.MetricResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Metric result not found")
    
    result.uploaded_at = datetime.now()
    
    for key, value in updated_result.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    
    db.commit()
    db.refresh(result)
    return result

# Delete a metric result
@router.delete("/results/{result_id}")
def delete_specific_metric_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(models.MetricResult).filter(models.MetricResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Metric result not found")
    
    db.delete(result)
    db.commit()
    return {"message": "Metric result deleted successfully"}

# Get all metric_results
@router.get("/results/", response_model=list[schemas.MetricResultResponse])
def get_all_results(db: Session = Depends(get_db)):
    metrics_results = db.query(models.MetricResult).all()
    if not metrics_results:
        raise HTTPException(status_code=404, detail="No Metric Results found")
    
    return [
        schemas.MetricResultResponse(
            id=metric_result.id,
            metric_id=metric_result.metric_id,
            value=metric_result.value if metric_result.value is not None else 0.0,  # Ensure float value
            uploaded_by=metric_result.uploaded_by, 
            uploaded_at=metric_result.uploaded_at, 
        )
        for metric_result in metrics_results
    ]
    
# ------------------- Risk Type API -------------------

# Create a metric
@router.post("/risk_types/", response_model=schemas.RiskTypeResponse)
def create_risk_type(risk_type: schemas.RiskTypeCreate, db: Session = Depends(get_db)):
    new_risk_type = models.RiskType(**risk_type.model_dump())
    db.add(new_risk_type)
    db.commit()
    db.refresh(new_risk_type)
    return new_risk_type

# Get all metrics
@router.get("/risk_types/", response_model=list[schemas.RiskTypeResponse])
def get_risk_types(db: Session = Depends(get_db)):
    risk_types = db.query(models.RiskType).all()
    return [schemas.RiskTypeResponse(
        id=risk_type.id,
        level=risk_type.level,
        status=risk_type.status,
        name=risk_type.name,
        description=risk_type.description,
    ) for risk_type in risk_types]

# Get a single metric by ID
@router.get("/risk_types/{id}", response_model=schemas.RiskTypeResponse)
def get_risk_type(id: int, db: Session = Depends(get_db)):
    risk_type = db.query(models.RiskType).filter(models.RiskType.id == id).first()
    if risk_type is None:
        raise HTTPException(status_code=404, detail="Risk Type not found")
    
    return schemas.RiskTypeResponse(
        id=risk_type.id,
        level=risk_type.level,
        status=risk_type.status,
        name=risk_type.name,
        description=risk_type.description
    )

# Update a metric
@router.put("/risk_types/{id}", response_model=schemas.RiskTypeResponse)
def update_risk_type(id: int, updated_risk_type: schemas.RiskTypeUpdate, db: Session = Depends(get_db)):
    risk_type = db.query(models.RiskType).filter(models.RiskType.id == id).first()
    if risk_type is None:
        raise HTTPException(status_code=404, detail="Risk Type not found")
    for key, value in updated_risk_type.model_dump(exclude_unset=True).items():
        setattr(risk_type, key, value)
    db.commit()
    db.refresh(risk_type)
    return risk_type

# Delete a metric
@router.delete("/risk_types/{id}")
def delete_risk_type(id: int, db: Session = Depends(get_db)):
    risk_type = db.query(models.RiskType).filter(models.RiskType.id == id).first()
    if risk_type is None:
        raise HTTPException(status_code=404, detail="Risk Type not found")
    db.delete(risk_type)
    db.commit()
    return {"message": "Risk Type deleted successfully"}

# ------------------- Business Unit API -------------------

# Create a metric
@router.post("/business_units/", response_model=schemas.BusinessUnitResponse)
def create_business_unit(business_unit: schemas.BusinessUnitCreate, db: Session = Depends(get_db)):
    new_business_unit = models.BusinessUnit(**business_unit.model_dump())
    db.add(new_business_unit)
    db.commit()
    db.refresh(new_business_unit)
    return new_business_unit

# Get all metrics
@router.get("/business_units/", response_model=list[schemas.BusinessUnitResponse])
def get_business_units(db: Session = Depends(get_db)):
    business_units = db.query(models.BusinessUnit).all()
    return [schemas.BusinessUnitResponse(
        id=business_unit.id,
        level=business_unit.level,
        status=business_unit.status,
        name=business_unit.name,
        description=business_unit.description,
    ) for business_unit in business_units]

# Get a single metric by ID
@router.get("/business_units/{id}", response_model=schemas.BusinessUnitResponse)
def get_business_unit(id: int, db: Session = Depends(get_db)):
    business_unit = db.query(models.BusinessUnit).filter(models.BusinessUnit.id == id).first()
    if business_unit is None:
        raise HTTPException(status_code=404, detail="Business Unit not found")
    
    return schemas.BusinessUnitResponse(
        id=business_unit.id,
        level=business_unit.level,
        status=business_unit.status,
        name=business_unit.name,
        description=business_unit.description
    )

# Update a metric
@router.put("/business_units/{id}", response_model=schemas.BusinessUnitResponse)
def update_business_unit(id: int, updated_business_unit: schemas.BusinessUnitUpdate, db: Session = Depends(get_db)):
    business_unit = db.query(models.BusinessUnit).filter(models.BusinessUnit.id == id).first()
    if business_unit is None:
        raise HTTPException(status_code=404, detail="Business Unit not found")
    for key, value in updated_business_unit.model_dump(exclude_unset=True).items():
        setattr(business_unit, key, value)
    db.commit()
    db.refresh(business_unit)
    return business_unit

# Delete a metric
@router.delete("/business_units/{id}")
def delete_business_unit(id: int, db: Session = Depends(get_db)):
    business_unit = db.query(models.BusinessUnit).filter(models.BusinessUnit.id == id).first()
    if business_unit is None:
        raise HTTPException(status_code=404, detail="Business Unit not found")
    db.delete(business_unit)
    db.commit()
    return {"message": "Business Unit deleted successfully"}
