"""
Analysis Model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class AnalysisType(str, enum.Enum):
    """Analysis type enumeration."""
    DESCRIPTIVE = "descriptive"
    FREQUENCIES = "frequencies"
    TTEST = "ttest"
    ANOVA = "anova"
    REGRESSION = "regression"
    CORRELATION = "correlation"
    CROSSTABS = "crosstabs"
    FACTOR_ANALYSIS = "factor_analysis"
    CLUSTER = "cluster"
    SURVIVAL = "survival"
    TIMESERIES = "timeseries"
    CUSTOM = "custom"


class AnalysisStatus(str, enum.Enum):
    """Analysis status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Analysis(Base):
    """Analysis model for storing statistical analyses."""

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Analysis configuration
    analysis_type = Column(Enum(AnalysisType), nullable=False)
    configuration = Column(Text, nullable=False)  # JSON configuration

    # Results
    results = Column(Text, nullable=True)  # JSON results
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    error_message = Column(Text, nullable=True)

    # Relationships
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    dataset = relationship("Dataset", back_populates="analyses")
    user = relationship("User", back_populates="analyses")
    project = relationship("Project", back_populates="analyses")

    def __repr__(self):
        return f"<Analysis(id={self.id}, name={self.name}, type={self.analysis_type})>"
