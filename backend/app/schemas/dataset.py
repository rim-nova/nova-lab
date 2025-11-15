"""
Dataset Schemas
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.dataset import DatasetType


class DatasetBase(BaseModel):
    """Base dataset schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class DatasetCreate(DatasetBase):
    """Schema for creating a dataset."""
    source_type: DatasetType
    source_path: Optional[str] = None
    source_config: Optional[Dict[str, Any]] = None
    project_id: Optional[int] = None


class DatasetUpdate(BaseModel):
    """Schema for updating a dataset."""
    name: Optional[str] = None
    description: Optional[str] = None


class DatasetResponse(DatasetBase):
    """Basic dataset response."""
    id: int
    source_type: DatasetType
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DatasetDetail(DatasetResponse):
    """Detailed dataset response with metadata."""
    file_size: Optional[int] = None
    file_format: Optional[str] = None
    source_path: Optional[str] = None
    owner_id: int
    project_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None

    class Config:
        from_attributes = True


class ColumnInfo(BaseModel):
    """Column information schema."""
    name: str
    dtype: str
    missing_count: int
    missing_percent: float
    unique_count: int
    sample_values: list


class DatasetProfile(BaseModel):
    """Dataset profile schema."""
    dataset_id: int
    row_count: int
    column_count: int
    columns: list[ColumnInfo]
    memory_usage: int
    correlations: Optional[Dict[str, Any]] = None
