from pydantic import BaseModel  # Pydantic is used for data validation and serialization
from datetime import datetime  # Handles timestamps
from typing import Optional  # Allows fields to be optional

# Schema for creating a new metric
class MetricCreate(BaseModel):
    name: str  # Metric name (Required)
    type: str 
    level: int # Metric level
    description: Optional[str] = None  # Optional: Description of the metric
    unit: Optional[str] = None  # Optional: Unit of measurement (e.g., %, USD, count)
    status: Optional[str] = "active"  # Optional: Default status is "active"
    warning_threshold: Optional[float] = None  # Optional: Warning level threshold
    limit_threshold: Optional[float] = None  # Optional: Limit level threshold (critical)
    risk_type_id: Optional[int] = None  # Optional: Risk type category
    business_unit_id: Optional[int] = None  # Optional: Business unit associated with the metric
    created_by: Optional[str] = None  # Optional: User who created the metric
    
    class Config:
        from_attributes = True  # Enables compatibility with ORM models (e.g., SQLAlchemy)

# Schema for updating an existing metric
class MetricUpdate(BaseModel):
    # All fields are optional to allow partial updates
    name: Optional[str] = None  
    type:  Optional[str] = None  
    level: Optional[int] = None  
    description: Optional[str] = None  
    unit: Optional[str] = None  
    status: Optional[str] = None  
    warning_threshold: Optional[float] = None  
    limit_threshold: Optional[float] = None  
    risk_type_id: Optional[int] = None  
    business_unit_id: Optional[int] = None  

# Schema for returning metric data in API responses
class MetricResponse(BaseModel):
    id: int  # Unique identifier for the metric
    name: str  # Metric name
    type: str
    level: int # Metric level
    description: Optional[str]  # Optional: Description of the metric
    unit: Optional[str]  # Optional: Unit of measurement
    status: Optional[str] = "active"  # Optional: Status with default value "active"
    warning_threshold: Optional[float]  # Optional: Warning threshold
    limit_threshold: Optional[float]  # Optional: Limit threshold
    risk_type_id: Optional[int]  # Optional: Risk category
    risk_type: Optional[str] = None  
    business_unit_id: Optional[int]  # Optional: Risk category
    business_unit: Optional[str]  = None  # Optional: Business unit
    
    created_by: Optional[str]  # Optional: User who created the metric
    created_at: datetime  # Timestamp of when the metric was created
    updated_at: datetime #Optional[datetime] = None  # Optional: Last updated timestamp
    
    latest_value: Optional[float] = None
    
    class Config:
        from_attributes = True  # Enables ORM conversion (e.g., from SQLAlchemy models)

###############################################################################################
###############################################################################################

# Schema for creating a metric result (Requires metric_id)
class MetricResultCreate(BaseModel):
    # id: int  # The ID of the metric this result belongs to
    value: float
    uploaded_by: Optional[str] = None  # Optional: User who created the metric


# Schema for updating a metric result
class MetricResultUpdate(BaseModel):
    value: Optional[float] = None  # Allows partial updates
    uploaded_by: Optional[str] = None # Optional: User who created the metric


# Schema for returning metric results
class MetricResultResponse(BaseModel):
    id: int
    metric_id: int
    value: float
    uploaded_by: Optional[str] = None  # Optional: User who created the metric
    uploaded_at: Optional[datetime]  # Timestamp of when the metric was created

    class Config:
        from_attributes = True  # Ensures ORM compatibility
        
###############################################################################################
###############################################################################################

# Schema for creating a new metric
class RiskTypeCreate(BaseModel):
    # id = int
    level: int
    name: str
    status: Optional[str] = "active"
    description: Optional[str] = None
    parent_id : Optional[int] = None
    
    # class Config:
    #     from_attributes = True  # Enables compatibility with ORM models (e.g., SQLAlchemy)

# Schema for updating an existing metric
class RiskTypeUpdate(BaseModel):
    # All fields are optional to allow partial updates
    level: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    parent_id : Optional[int]

    
# Schema for returning metric data in API responses
class RiskTypeResponse(BaseModel):
    id: int  # Unique identifier for the metric
    level: int
    name: str  # Metric name
    status: Optional[str] = "Active"  # Optional: Status with default value "active"
    description: Optional[str] = None # Optional: Description of the metric
    parent_id : Optional[int] = None

    class Config:
        from_attributes = True  # Enables ORM conversion (e.g., from SQLAlchemy models)
        
# ###############################################################################################
# ###############################################################################################


# Schema for creating a new metric
class BusinessUnitCreate(BaseModel):
    # id = int
    level: int
    name: str
    status: Optional[str] = "active"
    description: Optional[str] = None
    
    # class Config:
    #     from_attributes = True  # Enables compatibility with ORM models (e.g., SQLAlchemy)

# Schema for updating an existing metric
class BusinessUnitUpdate(BaseModel):
    # All fields are optional to allow partial updates
    level: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    
# Schema for returning metric data in API responses
class BusinessUnitResponse(BaseModel):
    id: int  # Unique identifier for the metric
    level: int
    name: str  # Metric name
    status: Optional[str] = "Active"  # Optional: Status with default value "active"
    description: Optional[str] = None # Optional: Description of the metric

    class Config:
        from_attributes = True  # Enables ORM conversion (e.g., from SQLAlchemy models)