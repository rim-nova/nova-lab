"""
Statistical Analysis Endpoints
Comprehensive SPSS-equivalent statistics
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.schemas.analysis import (
    DescriptiveStatsRequest,
    TTestRequest,
    ANOVARequest,
    CorrelationRequest,
    CrosstabRequest,
    FactorAnalysisRequest,
    ClusterAnalysisRequest,
    RegressionRequest
)
from app.api.v1.endpoints.auth import get_current_user
from app.services.data.data_loader import DataLoaderService
from app.services.statistics.descriptive_stats import DescriptiveStatsService
from app.services.statistics.inferential_stats import InferentialStatsService
from app.services.statistics.advanced_stats import AdvancedStatsService

router = APIRouter()
data_loader = DataLoaderService()
descriptive_service = DescriptiveStatsService()
inferential_service = InferentialStatsService()
advanced_service = AdvancedStatsService()


def get_dataset_df(dataset_id: int, user_id: int, db: Session):
    """Helper to get dataset and load DataFrame."""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == user_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    df, _ = data_loader.load_file(dataset.source_path)
    return df, dataset


@router.post("/descriptives")
def compute_descriptives(
    request: DescriptiveStatsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compute descriptive statistics (SPSS Descriptives)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = descriptive_service.compute_descriptives(
        df=df,
        variables=request.variables,
        include_distribution=request.include_plots
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/frequencies")
def compute_frequencies(
    dataset_id: int,
    variable: str,
    bins: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compute frequency distribution (SPSS Frequencies)."""
    df, dataset = get_dataset_df(dataset_id, current_user.id, db)

    results = descriptive_service.compute_frequencies(
        df=df,
        variable=variable,
        bins=bins
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/crosstabs")
def compute_crosstabs(
    request: CrosstabRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compute crosstabulation (SPSS Crosstabs)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = descriptive_service.compute_crosstabs(
        df=df,
        row_var=request.row_variable,
        col_var=request.column_variable,
        include_chi_square='chi_square' in (request.statistics or [])
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/ttest")
def perform_ttest(
    request: TTestRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform t-test (SPSS T-Test)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = inferential_service.t_test(
        df=df,
        dependent_var=request.dependent_variable,
        test_type=request.test_type,
        independent_var=request.independent_variable,
        alpha=request.alpha
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/anova")
def perform_anova(
    request: ANOVARequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform ANOVA (SPSS ANOVA/GLM)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = inferential_service.anova(
        df=df,
        dependent_var=request.dependent_variable,
        factors=request.factors,
        covariates=request.covariates
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/correlation")
def compute_correlation(
    request: CorrelationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compute correlation matrix (SPSS Correlations)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = inferential_service.correlation(
        df=df,
        variables=request.variables,
        method=request.method
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/regression/linear")
def perform_linear_regression(
    request: RegressionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform linear regression (SPSS Regression)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = inferential_service.linear_regression(
        df=df,
        dependent_var=request.dependent_variable,
        independent_vars=request.independent_variables,
        include_diagnostics=request.include_diagnostics
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/regression/logistic")
def perform_logistic_regression(
    request: RegressionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform logistic regression (SPSS Logistic Regression)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = inferential_service.logistic_regression(
        df=df,
        dependent_var=request.dependent_variable,
        independent_vars=request.independent_variables
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/factor-analysis")
def perform_factor_analysis(
    request: FactorAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform factor analysis (SPSS Factor Analysis)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = advanced_service.factor_analysis(
        df=df,
        variables=request.variables,
        n_factors=request.n_factors,
        rotation=request.rotation
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }


@router.post("/cluster-analysis")
def perform_cluster_analysis(
    request: ClusterAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform cluster analysis (SPSS Cluster Analysis)."""
    df, dataset = get_dataset_df(request.dataset_id, current_user.id, db)

    results = advanced_service.cluster_analysis(
        df=df,
        variables=request.variables,
        n_clusters=request.n_clusters,
        method=request.method
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        **results
    }
