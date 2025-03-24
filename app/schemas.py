from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MetricCreate(BaseModel):
    name: str
    value: float
    description: Optional[str] = None
    unit: Optional[str] = None
    status: Optional[str] = "active"
    warning_threshold: Optional[float] = None
    limit_threshold: Optional[float] = None
    risk_type: Optional[str] = None
    business_unit: Optional[str] = None
    created_by: Optional[str] = None
    
    class Config:
        from_attributes = True

class MetricUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    warning_threshold: Optional[float] = None
    limit_threshold: Optional[float] = None
    risk_type: Optional[str] = None
    business_unit: Optional[str] = None

class MetricResponse(BaseModel):
    id: int
    name: str
    value: float
    description: Optional[str]
    unit: Optional[str]
    status: str
    warning_threshold: Optional[float]
    limit_threshold: Optional[float]
    risk_type: Optional[str]
    business_unit: Optional[str]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    
    # @property
    # def status_indicator(self) -> str:
    #     """Calculates status based on thresholds."""
    #     if self.limit_threshold is not None and self.value > self.limit_threshold:
    #         return "Breach 🔴"
    #     elif self.warning_threshold is not None and self.value > self.warning_threshold:
    #         return "Warning 🟠"
    #     else:
    #         return "Green ✅"


    class Config:
        from_attributes = True  # Enables ORM conversion
