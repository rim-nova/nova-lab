"""
Dataset Model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, BigInteger, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class DatasetType(str, enum.Enum):
    """Dataset source type."""
    FILE = "file"
    DATABASE = "database"
    API = "api"
    CLOUD = "cloud"


class Dataset(Base):
    """Dataset model for storing uploaded or connected data."""

    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Source information
    source_type = Column(Enum(DatasetType), nullable=False)
    source_path = Column(String, nullable=True)  # File path or connection string
    source_config = Column(Text, nullable=True)  # JSON config for connections

    # Metadata
    row_count = Column(BigInteger, nullable=True)
    column_count = Column(Integer, nullable=True)
    file_size = Column(BigInteger, nullable=True)  # in bytes
    file_format = Column(String, nullable=True)  # csv, excel, parquet, etc.

    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    owner = relationship("User", back_populates="datasets")
    project = relationship("Project", back_populates="datasets")
    analyses = relationship("Analysis", back_populates="dataset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Dataset(id={self.id}, name={self.name}, type={self.source_type})>"
