"""
Dataset Management Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import os
from datetime import datetime

from app.db.base import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetResponse, DatasetDetail, DatasetProfile
from app.api.v1.endpoints.auth import get_current_user
from app.services.data.data_loader import DataLoaderService
from app.services.data.data_profiler import DataProfilerService
from app.core.config import settings

router = APIRouter()
data_loader = DataLoaderService()
data_profiler = DataProfilerService()


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = None,
    description: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a dataset file."""
    # Generate filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{current_user.id}_{timestamp}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)

    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Load and validate file
    try:
        df, metadata = data_loader.load_file(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to load file: {str(e)}"
        )

    # Create dataset record
    dataset_name = name or file.filename
    dataset = Dataset(
        name=dataset_name,
        description=description,
        source_type='file',
        source_path=file_path,
        file_format=metadata['file_format'],
        row_count=metadata['row_count'],
        column_count=metadata['column_count'],
        file_size=metadata['file_size'],
        owner_id=current_user.id
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset


@router.get("/", response_model=List[DatasetResponse])
def list_datasets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all datasets for current user."""
    datasets = db.query(Dataset).filter(
        Dataset.owner_id == current_user.id
    ).offset(skip).limit(limit).all()

    return datasets


@router.get("/{dataset_id}", response_model=DatasetDetail)
def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dataset details."""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    # Update last accessed
    dataset.last_accessed = datetime.utcnow()
    db.commit()

    return dataset


@router.get("/{dataset_id}/profile", response_model=DatasetProfile)
def profile_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive dataset profile."""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    # Load data
    df, _ = data_loader.load_file(dataset.source_path)

    # Profile data
    profile = data_profiler.profile_dataset(df)

    return {
        "dataset_id": dataset.id,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": profile['columns'],
        "memory_usage": profile['overview']['memory_usage'],
        "correlations": profile.get('correlations')
    }


@router.get("/{dataset_id}/preview")
def preview_dataset(
    dataset_id: int,
    n_rows: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Preview dataset rows."""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    # Load data
    df, _ = data_loader.load_file(dataset.source_path)

    # Get sample
    sample_df = data_profiler.get_sample_data(df, n_rows=n_rows, strategy='head')

    return {
        "dataset_id": dataset.id,
        "total_rows": len(df),
        "preview_rows": len(sample_df),
        "columns": list(df.columns),
        "data": sample_df.to_dict(orient='records')
    }


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete dataset."""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    # Delete file if exists
    if dataset.source_path and os.path.exists(dataset.source_path):
        os.remove(dataset.source_path)

    db.delete(dataset)
    db.commit()

    return None
