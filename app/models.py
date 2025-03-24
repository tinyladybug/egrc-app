from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Metric name
    value = Column(Float, nullable=False)  # Metric value
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
