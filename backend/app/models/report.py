"""
Report Model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class ReportFormat(str, enum.Enum):
    """Report format enumeration."""
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    HTML = "html"
    MARKDOWN = "markdown"


class Report(Base):
    """Report model for generated reports."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Report content
    content = Column(Text, nullable=False)  # JSON or Markdown
    format = Column(Enum(ReportFormat), nullable=False)

    # Storage
    file_path = Column(String, nullable=True)  # Path to generated report file

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="reports")
    project = relationship("Project", back_populates="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, name={self.name}, format={self.format})>"
