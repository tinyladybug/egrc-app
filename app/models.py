from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Metric name
    description = Column(String, nullable=True)  # Optional description
    unit = Column(String, nullable=True)  # Unit of measurement (%, $, count, etc.)
    status = Column(String, default="active")  # Status: active/inactive/archived
    warning_threshold = Column(Float, nullable=True)  # Warning threshold
    limit_threshold = Column(Float, nullable=True)  # Limit threshold (critical)
    risk_type = Column(String, nullable=True)  # Risk category/type
    business_unit = Column(String, nullable=True)  # Business unit related to metric
    created_by = Column(String, nullable=True)  # User who created the metric
    created_at = Column(DateTime, default=func.now())  # Auto timestamp on creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Auto update timestamp
    
    # Relationship to MetricResult (1-to-Many)
    results = relationship("MetricResult", back_populates="metric", order_by="MetricResult.timestamp.desc()", cascade="all, delete-orphan")
    
    @property
    def latest_value(self):
        """Return the most recent metric result value (if available)."""
        return self.results[0].value if self.results else None
    
class MetricResult(Base):
    __tablename__ = "metric_results"

    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(Integer, ForeignKey("metrics.id", ondelete="CASCADE"), nullable=False)  # Foreign key to Metric
    value = Column(Float, nullable=False)  # Recorded value
    timestamp = Column(DateTime, default=func.now())  # Timestamp of the result

    # Relationship back to Metric
    metric = relationship("Metric", back_populates="results")