"""
Dashboard Model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Dashboard(Base):
    """Dashboard model for visualization and reporting."""

    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Dashboard configuration
    layout = Column(Text, nullable=False)  # JSON layout configuration
    widgets = Column(Text, nullable=False)  # JSON widget definitions
    filters = Column(Text, nullable=True)  # JSON global filters

    # Sharing
    is_public = Column(Boolean, default=False)

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="dashboards")
    project = relationship("Project", back_populates="dashboards")

    def __repr__(self):
        return f"<Dashboard(id={self.id}, name={self.name})>"
