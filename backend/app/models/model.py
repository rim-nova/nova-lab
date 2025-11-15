"""
ML Model Model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class ModelType(str, enum.Enum):
    """ML model type enumeration."""
    LINEAR_REGRESSION = "linear_regression"
    LOGISTIC_REGRESSION = "logistic_regression"
    DECISION_TREE = "decision_tree"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    SVM = "svm"
    KNN = "knn"
    NEURAL_NETWORK = "neural_network"
    AUTOML = "automl"


class MLModel(Base):
    """Machine Learning model storage."""

    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Model configuration
    model_type = Column(Enum(ModelType), nullable=False)
    task_type = Column(String, nullable=False)  # classification, regression
    algorithm = Column(String, nullable=False)
    hyperparameters = Column(Text, nullable=True)  # JSON

    # Performance metrics
    metrics = Column(Text, nullable=True)  # JSON with accuracy, precision, etc.
    score = Column(Float, nullable=True)  # Primary metric score

    # Storage
    model_path = Column(String, nullable=True)  # Path to saved model file
    feature_names = Column(Text, nullable=True)  # JSON array

    # Relationships
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    trained_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="models")
    project = relationship("Project", back_populates="models")

    def __repr__(self):
        return f"<MLModel(id={self.id}, name={self.name}, type={self.model_type})>"
