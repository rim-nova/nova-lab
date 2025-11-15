"""
Machine Learning Service
Comprehensive ML training, evaluation, and prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, r2_score, mean_absolute_error
)
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor
)
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from typing import Dict, Any, List, Optional, Tuple
import joblib
import json
import logging

logger = logging.getLogger(__name__)


class MLService:
    """Service for machine learning model training and prediction."""

    def __init__(self):
        """Initialize ML service."""
        self.models = {
            'classification': {
                'logistic_regression': LogisticRegression,
                'decision_tree': DecisionTreeClassifier,
                'random_forest': RandomForestClassifier,
                'gradient_boosting': GradientBoostingClassifier,
                'xgboost': XGBClassifier,
                'lightgbm': LGBMClassifier,
                'svm': SVC,
                'knn': KNeighborsClassifier
            },
            'regression': {
                'linear_regression': LinearRegression,
                'ridge': Ridge,
                'lasso': Lasso,
                'decision_tree': DecisionTreeRegressor,
                'random_forest': RandomForestRegressor,
                'gradient_boosting': GradientBoostingRegressor,
                'xgboost': XGBRegressor,
                'lightgbm': LGBMRegressor,
                'svr': SVR,
                'knn': KNeighborsRegressor
            }
        }

        self.default_params = {
            'random_forest': {'n_estimators': 100, 'max_depth': 10, 'random_state': 42},
            'gradient_boosting': {'n_estimators': 100, 'learning_rate': 0.1, 'random_state': 42},
            'xgboost': {'n_estimators': 100, 'learning_rate': 0.1, 'random_state': 42},
            'lightgbm': {'n_estimators': 100, 'learning_rate': 0.1, 'random_state': 42},
            'svm': {'kernel': 'rbf', 'C': 1.0},
            'knn': {'n_neighbors': 5}
        }

    def train_model(
        self,
        df: pd.DataFrame,
        target_var: str,
        feature_vars: List[str],
        task_type: str,
        algorithm: str,
        test_size: float = 0.2,
        cv_folds: int = 5,
        hyperparameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Train a machine learning model.

        Args:
            df: Input DataFrame
            target_var: Target variable name
            feature_vars: List of feature variable names
            task_type: 'classification' or 'regression'
            algorithm: Algorithm name
            test_size: Test set size (0.0 to 1.0)
            cv_folds: Number of cross-validation folds
            hyperparameters: Model hyperparameters

        Returns:
            Training results with metrics and model info
        """
        logger.info(f"Training {algorithm} model for {task_type}")

        # Prepare data
        df_clean = df[[target_var] + feature_vars].dropna()
        X = df_clean[feature_vars]
        y = df_clean[target_var]

        # Encode target if classification
        label_encoder = None
        if task_type == 'classification':
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(y)

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y if task_type == 'classification' else None
        )

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Get model class
        if task_type not in self.models:
            raise ValueError(f"Unknown task type: {task_type}")

        if algorithm not in self.models[task_type]:
            raise ValueError(f"Unknown algorithm: {algorithm} for {task_type}")

        model_class = self.models[task_type][algorithm]

        # Get hyperparameters
        params = hyperparameters or self.default_params.get(algorithm, {})

        # Train model
        model = model_class(**params)
        model.fit(X_train_scaled, y_train)

        # Predictions
        y_pred_train = model.predict(X_train_scaled)
        y_pred_test = model.predict(X_test_scaled)

        # Evaluate
        if task_type == 'classification':
            metrics = self._evaluate_classification(
                y_train, y_pred_train, y_test, y_pred_test,
                model, X_test_scaled, label_encoder
            )
        else:
            metrics = self._evaluate_regression(
                y_train, y_pred_train, y_test, y_pred_test
            )

        # Cross-validation score
        cv_scores = cross_val_score(
            model, X_train_scaled, y_train, cv=cv_folds,
            scoring='accuracy' if task_type == 'classification' else 'r2'
        )

        # Feature importance
        feature_importance = self._get_feature_importance(model, feature_vars)

        result = {
            'algorithm': algorithm,
            'task_type': task_type,
            'n_samples': len(df_clean),
            'n_features': len(feature_vars),
            'test_size': test_size,
            'hyperparameters': params,
            'metrics': metrics,
            'cv_scores': {
                'scores': [float(s) for s in cv_scores],
                'mean': float(cv_scores.mean()),
                'std': float(cv_scores.std())
            },
            'feature_importance': feature_importance,
            'feature_names': feature_vars,
            'target_name': target_var
        }

        # Save model metadata
        result['model_metadata'] = {
            'scaler': scaler,
            'label_encoder': label_encoder,
            'feature_vars': feature_vars,
            'target_var': target_var
        }

        return result, model

    def _evaluate_classification(
        self,
        y_train, y_pred_train, y_test, y_pred_test,
        model, X_test_scaled, label_encoder
    ) -> Dict[str, Any]:
        """Evaluate classification model."""
        metrics = {
            'train': {
                'accuracy': float(accuracy_score(y_train, y_pred_train)),
                'precision': float(precision_score(y_train, y_pred_train, average='weighted', zero_division=0)),
                'recall': float(recall_score(y_train, y_pred_train, average='weighted', zero_division=0)),
                'f1_score': float(f1_score(y_train, y_pred_train, average='weighted', zero_division=0))
            },
            'test': {
                'accuracy': float(accuracy_score(y_test, y_pred_test)),
                'precision': float(precision_score(y_test, y_pred_test, average='weighted', zero_division=0)),
                'recall': float(recall_score(y_test, y_pred_test, average='weighted', zero_division=0)),
                'f1_score': float(f1_score(y_test, y_pred_test, average='weighted', zero_division=0))
            }
        }

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred_test)
        metrics['confusion_matrix'] = cm.tolist()

        # ROC AUC (if binary and probability predictions available)
        if len(np.unique(y_test)) == 2 and hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test_scaled)[:, 1]
            metrics['test']['roc_auc'] = float(roc_auc_score(y_test, y_proba))

        return metrics

    def _evaluate_regression(
        self,
        y_train, y_pred_train, y_test, y_pred_test
    ) -> Dict[str, Any]:
        """Evaluate regression model."""
        return {
            'train': {
                'r2_score': float(r2_score(y_train, y_pred_train)),
                'rmse': float(np.sqrt(mean_squared_error(y_train, y_pred_train))),
                'mae': float(mean_absolute_error(y_train, y_pred_train))
            },
            'test': {
                'r2_score': float(r2_score(y_test, y_pred_test)),
                'rmse': float(np.sqrt(mean_squared_error(y_test, y_pred_test))),
                'mae': float(mean_absolute_error(y_test, y_pred_test))
            }
        }

    def _get_feature_importance(
        self,
        model,
        feature_names: List[str]
    ) -> Optional[List[Dict[str, Any]]]:
        """Get feature importance if available."""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            return [
                {'feature': name, 'importance': float(imp)}
                for name, imp in sorted(
                    zip(feature_names, importances),
                    key=lambda x: x[1],
                    reverse=True
                )
            ]
        elif hasattr(model, 'coef_'):
            coefs = model.coef_
            if len(coefs.shape) == 1:  # Single output
                return [
                    {'feature': name, 'coefficient': float(coef)}
                    for name, coef in zip(feature_names, coefs)
                ]

        return None

    def hyperparameter_tuning(
        self,
        df: pd.DataFrame,
        target_var: str,
        feature_vars: List[str],
        task_type: str,
        algorithm: str,
        param_grid: Dict[str, List[Any]],
        cv_folds: int = 5
    ) -> Dict[str, Any]:
        """
        Perform hyperparameter tuning using GridSearchCV.

        Args:
            df: Input DataFrame
            target_var: Target variable
            feature_vars: Feature variables
            task_type: 'classification' or 'regression'
            algorithm: Algorithm name
            param_grid: Parameter grid for search
            cv_folds: Number of CV folds

        Returns:
            Best parameters and scores
        """
        logger.info(f"Performing hyperparameter tuning for {algorithm}")

        # Prepare data
        df_clean = df[[target_var] + feature_vars].dropna()
        X = df_clean[feature_vars]
        y = df_clean[target_var]

        # Encode target if classification
        if task_type == 'classification':
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(y)

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Get model
        model_class = self.models[task_type][algorithm]
        model = model_class()

        # Grid search
        scoring = 'accuracy' if task_type == 'classification' else 'r2'
        grid_search = GridSearchCV(
            model, param_grid, cv=cv_folds, scoring=scoring, n_jobs=-1
        )
        grid_search.fit(X_scaled, y)

        return {
            'best_params': grid_search.best_params_,
            'best_score': float(grid_search.best_score_),
            'all_results': [
                {
                    'params': params,
                    'mean_score': float(score),
                    'std_score': float(std)
                }
                for params, score, std in zip(
                    grid_search.cv_results_['params'],
                    grid_search.cv_results_['mean_test_score'],
                    grid_search.cv_results_['std_test_score']
                )
            ]
        }

    def predict(
        self,
        model,
        df: pd.DataFrame,
        feature_vars: List[str],
        scaler: StandardScaler,
        label_encoder: Optional[LabelEncoder] = None
    ) -> np.ndarray:
        """
        Make predictions using a trained model.

        Args:
            model: Trained model
            df: Input DataFrame
            feature_vars: Feature variable names
            scaler: Fitted scaler
            label_encoder: Fitted label encoder (for classification)

        Returns:
            Predictions array
        """
        X = df[feature_vars]
        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)

        if label_encoder:
            predictions = label_encoder.inverse_transform(predictions.astype(int))

        return predictions

    def save_model(
        self,
        model,
        metadata: Dict[str, Any],
        filepath: str
    ) -> None:
        """
        Save model and metadata.

        Args:
            model: Trained model
            metadata: Model metadata
            filepath: Path to save model
        """
        model_data = {
            'model': model,
            'metadata': metadata
        }
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath: str) -> Tuple[Any, Dict[str, Any]]:
        """
        Load model and metadata.

        Args:
            filepath: Path to model file

        Returns:
            Tuple of (model, metadata)
        """
        model_data = joblib.load(filepath)
        return model_data['model'], model_data['metadata']
