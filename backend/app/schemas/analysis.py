"""
Analysis Schemas
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.analysis import AnalysisType, AnalysisStatus


class AnalysisConfig(BaseModel):
    """Analysis configuration schema."""
    variables: List[str]
    method: str
    options: Optional[Dict[str, Any]] = None


class AnalysisCreate(BaseModel):
    """Schema for creating an analysis."""
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    analysis_type: AnalysisType
    dataset_id: int
    configuration: AnalysisConfig
    project_id: Optional[int] = None


class AnalysisResponse(BaseModel):
    """Analysis response schema."""
    id: int
    name: str
    description: Optional[str] = None
    analysis_type: AnalysisType
    status: AnalysisStatus
    dataset_id: int
    user_id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class DescriptiveStatsRequest(BaseModel):
    """Request for descriptive statistics."""
    dataset_id: int
    variables: List[str]
    include_plots: bool = True


class TTestRequest(BaseModel):
    """Request for t-test."""
    dataset_id: int
    dependent_variable: str
    independent_variable: Optional[str] = None  # For independent samples
    test_type: str = Field(..., pattern="^(one_sample|independent|paired)$")
    alpha: float = 0.05


class ANOVARequest(BaseModel):
    """Request for ANOVA."""
    dataset_id: int
    dependent_variable: str
    factors: List[str]
    covariates: Optional[List[str]] = None
    post_hoc: Optional[List[str]] = None


class RegressionRequest(BaseModel):
    """Request for regression analysis."""
    dataset_id: int
    dependent_variable: str
    independent_variables: List[str]
    regression_type: str = Field(..., pattern="^(linear|logistic|multinomial)$")
    include_diagnostics: bool = True


class CorrelationRequest(BaseModel):
    """Request for correlation analysis."""
    dataset_id: int
    variables: List[str]
    method: str = Field(default="pearson", pattern="^(pearson|spearman|kendall)$")


class CrosstabRequest(BaseModel):
    """Request for crosstabulation."""
    dataset_id: int
    row_variable: str
    column_variable: str
    statistics: Optional[List[str]] = ["chi_square"]


class FactorAnalysisRequest(BaseModel):
    """Request for factor analysis."""
    dataset_id: int
    variables: List[str]
    n_factors: Optional[int] = None
    rotation: str = Field(default="varimax", pattern="^(varimax|oblimin|none)$")


class ClusterAnalysisRequest(BaseModel):
    """Request for cluster analysis."""
    dataset_id: int
    variables: List[str]
    n_clusters: int = Field(..., ge=2)
    method: str = Field(default="kmeans", pattern="^(kmeans|hierarchical)$")
