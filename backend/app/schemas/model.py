"""
ML Model Schemas
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.model import ModelType


class MLModelBase(BaseModel):
    """Base ML model schema."""
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class ModelTrainRequest(BaseModel):
    """Request for training a model."""
    dataset_id: int
    target_variable: str
    feature_variables: List[str]
    model_type: Optional[ModelType] = None  # None for AutoML
    task_type: str = Field(..., pattern="^(classification|regression)$")
    test_size: float = Field(default=0.2, ge=0.1, le=0.5)
    cv_folds: int = Field(default=5, ge=2, le=10)
    auto_ml: bool = False
    hyperparameters: Optional[Dict[str, Any]] = None


class MLModelCreate(MLModelBase):
    """Schema for creating an ML model record."""
    model_type: ModelType
    task_type: str
    algorithm: str
    dataset_id: int
    project_id: Optional[int] = None


class MLModelResponse(MLModelBase):
    """ML model response schema."""
    id: int
    model_type: ModelType
    task_type: str
    algorithm: str
    score: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    trained_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ModelPredictRequest(BaseModel):
    """Request for model prediction."""
    model_id: int
    dataset_id: int
    save_predictions: bool = True


class AutoMLRequest(BaseModel):
    """Request for AutoML."""
    dataset_id: int
    target_variable: str
    feature_variables: Optional[List[str]] = None  # None = use all
    task_type: str = Field(..., pattern="^(classification|regression)$")
    time_budget: int = Field(default=300, ge=60, le=3600)  # seconds
    metric: Optional[str] = None  # auto-detect based on task
