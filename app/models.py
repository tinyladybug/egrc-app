from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Metric name
    type = Column(String, nullable=False) # Metric Type
    level = Column(String, nullable=False) # Metric level
    description = Column(String, nullable=True)  # Optional description
    unit = Column(String, nullable=True)  # Unit of measurement (%, $, count, etc.)
    status = Column(String, default="active")  # Status: active/inactive/archived
    warning_threshold = Column(Float, nullable=True)  # Warning threshold
    limit_threshold = Column(Float, nullable=True)  # Limit threshold (critical)
    # risk_type = Column(String, nullable=True)  # Risk category/type
    risk_type_id = Column(Integer, ForeignKey("risk_types.id"), nullable=False)  # Foreign Key to RiskType
    risk_type = relationship("RiskType", back_populates="metric")  # Establish relationship
    business_unit = Column(String, nullable=True)  # Business unit related to metric
    business_unit_id = Column(Integer, ForeignKey("business_units.id"), nullable=False)  # Foreign Key to RiskType
    business_unit = relationship("BusinessUnit", back_populates="metric")  # Establish relationship
    created_by = Column(String, nullable=True)  # User who created the metric
    created_at = Column(DateTime, default=func.now())  # Auto timestamp on creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Auto update timestamp
    
    # Relationship to MetricResult (1-to-Many)
    results = relationship("MetricResult", back_populates="metric", order_by="MetricResult.uploaded_at.desc()", cascade="all, delete-orphan")
    
    @property
    def latest_value(self):
        """Return the most recent metric result value (if available)."""
        return self.results[0].value if self.results else None
    
class MetricResult(Base):
    __tablename__ = "metric_results"

    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(Integer, ForeignKey("metrics.id", ondelete="CASCADE"), nullable=False)  # Foreign key to Metric
    value = Column(Float, nullable=False)  # Recorded value
    uploaded_by = Column(String, nullable=True)  # User who created the metric
    uploaded_at = Column(DateTime, default=func.now())  # Auto timestamp on creation
    
    # Relationship back to Metric
    metric = relationship("Metric", back_populates="results")
    
    
class RiskType(Base):
    __tablename__ = "risk_types"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False)
    status = Column(String, default="active")
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # # Self-referential foreign key to create hierarchy
    parent_id = Column(Integer, ForeignKey("risk_types.id"), nullable=True)

    # # Relationship for hierarchical structure
    parent = relationship("RiskType", remote_side=[id], back_populates="sub_risks")
    sub_risks = relationship("RiskType", back_populates="parent", cascade="all, delete")

    # Establish a one-to-many relationship with metrics
    metric = relationship("Metric", back_populates="risk_type")
    
class BusinessUnit(Base):
    __tablename__ = "business_units"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False)
    status = Column(String, default="active")
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # # Self-referential foreign key to create hierarchy
    parent_id = Column(Integer, ForeignKey("business_units.id"), nullable=True)

    # # Relationship for hierarchical structure
    parent = relationship("BusinessUnit", remote_side=[id], back_populates="sub_business_units")
    sub_business_units = relationship("BusinessUnit", back_populates="parent", cascade="all, delete")

    # Establish a one-to-many relationship with metrics
    metric = relationship("Metric", back_populates="business_unit")