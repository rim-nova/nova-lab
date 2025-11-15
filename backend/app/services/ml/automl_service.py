"""
AutoML Service
Automatic machine learning with model selection and optimization
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Dict, Any, List, Optional
import logging
from app.services.ml.ml_service import MLService

logger = logging.getLogger(__name__)


class AutoMLService:
    """Service for automated machine learning."""

    def __init__(self):
        """Initialize AutoML service."""
        self.ml_service = MLService()

        # Algorithms to try for each task type
        self.classification_algorithms = [
            'logistic_regression',
            'random_forest',
            'gradient_boosting',
            'xgboost'
        ]

        self.regression_algorithms = [
            'linear_regression',
            'ridge',
            'random_forest',
            'gradient_boosting',
            'xgboost'
        ]

    def auto_train(
        self,
        df: pd.DataFrame,
        target_var: str,
        feature_vars: Optional[List[str]] = None,
        task_type: Optional[str] = None,
        test_size: float = 0.2,
        time_budget: int = 300
    ) -> Dict[str, Any]:
        """
        Automatically train and select best model.

        Args:
            df: Input DataFrame
            target_var: Target variable
            feature_vars: Feature variables (None = use all except target)
            task_type: 'classification' or 'regression' (None = auto-detect)
            test_size: Test set size
            time_budget: Maximum time in seconds (not strictly enforced)

        Returns:
            AutoML results with best model and leaderboard
        """
        logger.info("Starting AutoML process")

        # Determine feature variables
        if feature_vars is None:
            feature_vars = [col for col in df.columns if col != target_var]

        # Auto-detect task type if not specified
        if task_type is None:
            task_type = self._detect_task_type(df[target_var])

        logger.info(f"Task type: {task_type}")
        logger.info(f"Features: {len(feature_vars)}")

        # Select algorithms to try
        if task_type == 'classification':
            algorithms = self.classification_algorithms
        else:
            algorithms = self.regression_algorithms

        # Train multiple models
        results = []
        models = {}

        for algo in algorithms:
            try:
                logger.info(f"Training {algo}...")
                result, model = self.ml_service.train_model(
                    df=df,
                    target_var=target_var,
                    feature_vars=feature_vars,
                    task_type=task_type,
                    algorithm=algo,
                    test_size=test_size
                )

                # Get primary metric
                if task_type == 'classification':
                    score = result['metrics']['test']['accuracy']
                    metric_name = 'accuracy'
                else:
                    score = result['metrics']['test']['r2_score']
                    metric_name = 'r2_score'

                results.append({
                    'algorithm': algo,
                    'score': score,
                    'metric': metric_name,
                    'metrics': result['metrics'],
                    'cv_mean': result['cv_scores']['mean'],
                    'cv_std': result['cv_scores']['std']
                })

                models[algo] = {
                    'model': model,
                    'result': result
                }

            except Exception as e:
                logger.error(f"Error training {algo}: {e}")
                continue

        # Sort by score (descending)
        results.sort(key=lambda x: x['score'], reverse=True)

        if not results:
            raise RuntimeError("AutoML failed: No models were successfully trained")

        # Best model
        best_algo = results[0]['algorithm']
        best_model_info = models[best_algo]

        return {
            'task_type': task_type,
            'target_variable': target_var,
            'n_features': len(feature_vars),
            'feature_variables': feature_vars,
            'n_samples': len(df),
            'test_size': test_size,
            'best_model': {
                'algorithm': best_algo,
                'score': results[0]['score'],
                'metric': results[0]['metric'],
                'metrics': results[0]['metrics'],
                'model_object': best_model_info['model'],
                'model_metadata': best_model_info['result']['model_metadata']
            },
            'leaderboard': results,
            'recommendation': self._generate_recommendation(results, task_type)
        }

    def _detect_task_type(self, target_series: pd.Series) -> str:
        """
        Auto-detect task type based on target variable.

        Args:
            target_series: Target variable series

        Returns:
            'classification' or 'regression'
        """
        # If numeric and many unique values, likely regression
        if pd.api.types.is_numeric_dtype(target_series):
            n_unique = target_series.nunique()
            n_total = len(target_series)

            # If unique values > 20 or > 10% of data, treat as regression
            if n_unique > 20 or (n_unique / n_total) > 0.1:
                return 'regression'
            else:
                return 'classification'
        else:
            # Non-numeric is classification
            return 'classification'

    def _generate_recommendation(
        self,
        results: List[Dict[str, Any]],
        task_type: str
    ) -> str:
        """Generate recommendation based on results."""
        if not results:
            return "No successful models trained."

        best = results[0]
        second_best = results[1] if len(results) > 1 else None

        recommendation = f"The best performing model is {best['algorithm']} "
        recommendation += f"with a {best['metric']} of {best['score']:.4f}. "

        if second_best:
            score_diff = best['score'] - second_best['score']
            if score_diff < 0.01:  # Very close scores
                recommendation += f"However, {second_best['algorithm']} has very similar "
                recommendation += f"performance ({second_best['score']:.4f}) and might be "
                recommendation += "preferred for its interpretability or speed. "

        # Check for overfitting
        if task_type == 'classification':
            train_acc = best['metrics']['train']['accuracy']
            test_acc = best['metrics']['test']['accuracy']
        else:
            train_acc = best['metrics']['train']['r2_score']
            test_acc = best['metrics']['test']['r2_score']

        if train_acc - test_acc > 0.1:
            recommendation += "Note: The model shows signs of overfitting. "
            recommendation += "Consider collecting more data or using regularization. "

        return recommendation
