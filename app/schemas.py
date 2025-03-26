from pydantic import BaseModel  # Pydantic is used for data validation and serialization
from datetime import datetime  # Handles timestamps
from typing import Optional  # Allows fields to be optional

# Schema for creating a new metric
class MetricCreate(BaseModel):
    name: str  # Metric name (Required)
    value: float  # Metric value (Required)
    description: Optional[str] = None  # Optional: Description of the metric
    unit: Optional[str] = None  # Optional: Unit of measurement (e.g., %, USD, count)
    status: Optional[str] = "active"  # Optional: Default status is "active"
    warning_threshold: Optional[float] = None  # Optional: Warning level threshold
    limit_threshold: Optional[float] = None  # Optional: Limit level threshold (critical)
    risk_type: Optional[str] = None  # Optional: Risk type category
    business_unit: Optional[str] = None  # Optional: Business unit associated with the metric
    created_by: Optional[str] = None  # Optional: User who created the metric
    
    class Config:
        from_attributes = True  # Enables compatibility with ORM models (e.g., SQLAlchemy)

# Schema for updating an existing metric
class MetricUpdate(BaseModel):
    # All fields are optional to allow partial updates
    name: Optional[str] = None  
    value: Optional[float] = None  
    description: Optional[str] = None  
    unit: Optional[str] = None  
    status: Optional[str] = None  
    warning_threshold: Optional[float] = None  
    limit_threshold: Optional[float] = None  
    risk_type: Optional[str] = None  
    business_unit: Optional[str] = None  

# Schema for returning metric data in API responses
class MetricResponse(BaseModel):
    id: int  # Unique identifier for the metric
    name: str  # Metric name
    value: float  # Metric value
    description: Optional[str]  # Optional: Description of the metric
    unit: Optional[str]  # Optional: Unit of measurement
    status: Optional[str] = "active"  # Optional: Status with default value "active"
    warning_threshold: Optional[float]  # Optional: Warning threshold
    limit_threshold: Optional[float]  # Optional: Limit threshold
    risk_type: Optional[str]  # Optional: Risk category
    business_unit: Optional[str]  # Optional: Business unit
    created_by: Optional[str]  # Optional: User who created the metric
    created_at: datetime  # Timestamp of when the metric was created
    updated_at: datetime #Optional[datetime] = None  # Optional: Last updated timestamp
    
    # This method was commented out but can be useful for displaying a status indicator
    # @property
    # def status_indicator(self) -> str:
    #     """Calculates status based on thresholds."""
    #     if self.limit_threshold is not None and self.value > self.limit_threshold:
    #         return "Breach 🔴"  # Critical breach if value exceeds limit threshold
    #     elif self.warning_threshold is not None and self.value > self.warning_threshold:
    #         return "Warning 🟠"  # Warning if value exceeds warning threshold
    #     else:
    #         return "Green ✅"  # Normal status if within thresholds

    class Config:
        from_attributes = True  # Enables ORM conversion (e.g., from SQLAlchemy models)
