"""
Data Transformation Service
Handles data cleaning, transformation, and feature engineering
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
import logging

logger = logging.getLogger(__name__)


class DataTransformerService:
    """Service for data transformation and cleaning operations."""

    def __init__(self):
        """Initialize data transformer service."""
        self.transformers = {}
        self.encoders = {}

    def handle_missing_data(
        self,
        df: pd.DataFrame,
        strategy: str = 'drop',
        columns: Optional[List[str]] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Handle missing data.

        Args:
            df: Input DataFrame
            strategy: 'drop', 'mean', 'median', 'mode', 'constant', 'knn'
            columns: Specific columns to handle (None = all)
            **kwargs: Additional arguments for strategy

        Returns:
            Transformed DataFrame
        """
        df_copy = df.copy()
        target_cols = columns if columns else df_copy.columns.tolist()

        logger.info(f"Handling missing data using strategy: {strategy}")

        if strategy == 'drop':
            df_copy = df_copy.dropna(subset=target_cols)

        elif strategy in ['mean', 'median', 'mode', 'constant']:
            for col in target_cols:
                if df_copy[col].isna().any():
                    if pd.api.types.is_numeric_dtype(df_copy[col]):
                        if strategy == 'mean':
                            df_copy[col].fillna(df_copy[col].mean(), inplace=True)
                        elif strategy == 'median':
                            df_copy[col].fillna(df_copy[col].median(), inplace=True)
                        elif strategy == 'constant':
                            value = kwargs.get('fill_value', 0)
                            df_copy[col].fillna(value, inplace=True)
                    else:
                        if strategy == 'mode':
                            mode_val = df_copy[col].mode()[0] if len(df_copy[col].mode()) > 0 else ''
                            df_copy[col].fillna(mode_val, inplace=True)
                        elif strategy == 'constant':
                            value = kwargs.get('fill_value', 'unknown')
                            df_copy[col].fillna(value, inplace=True)

        elif strategy == 'knn':
            numeric_cols = df_copy[target_cols].select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                imputer = KNNImputer(n_neighbors=kwargs.get('n_neighbors', 5))
                df_copy[numeric_cols] = imputer.fit_transform(df_copy[numeric_cols])

        return df_copy

    def scale_features(
        self,
        df: pd.DataFrame,
        method: str = 'standard',
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Scale numeric features.

        Args:
            df: Input DataFrame
            method: 'standard' (z-score) or 'minmax'
            columns: Columns to scale (None = all numeric)

        Returns:
            Scaled DataFrame
        """
        df_copy = df.copy()

        if columns is None:
            columns = df_copy.select_dtypes(include=[np.number]).columns.tolist()

        if not columns:
            return df_copy

        logger.info(f"Scaling features using method: {method}")

        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")

        df_copy[columns] = scaler.fit_transform(df_copy[columns])
        self.transformers[f'scaler_{method}'] = scaler

        return df_copy

    def encode_categorical(
        self,
        df: pd.DataFrame,
        method: str = 'onehot',
        columns: Optional[List[str]] = None,
        drop_first: bool = False
    ) -> pd.DataFrame:
        """
        Encode categorical variables.

        Args:
            df: Input DataFrame
            method: 'onehot' or 'label'
            columns: Columns to encode (None = all categorical)
            drop_first: Drop first category for onehot

        Returns:
            Encoded DataFrame
        """
        df_copy = df.copy()

        if columns is None:
            columns = df_copy.select_dtypes(include=['object', 'category']).columns.tolist()

        if not columns:
            return df_copy

        logger.info(f"Encoding categorical variables using method: {method}")

        if method == 'onehot':
            df_copy = pd.get_dummies(
                df_copy,
                columns=columns,
                drop_first=drop_first,
                dtype=int
            )

        elif method == 'label':
            for col in columns:
                encoder = LabelEncoder()
                df_copy[col] = encoder.fit_transform(df_copy[col].astype(str))
                self.encoders[col] = encoder

        return df_copy

    def remove_outliers(
        self,
        df: pd.DataFrame,
        method: str = 'iqr',
        columns: Optional[List[str]] = None,
        threshold: float = 1.5
    ) -> pd.DataFrame:
        """
        Remove outliers from numeric columns.

        Args:
            df: Input DataFrame
            method: 'iqr' or 'zscore'
            columns: Columns to check (None = all numeric)
            threshold: Threshold for outlier detection

        Returns:
            DataFrame with outliers removed
        """
        df_copy = df.copy()

        if columns is None:
            columns = df_copy.select_dtypes(include=[np.number]).columns.tolist()

        logger.info(f"Removing outliers using method: {method}")

        for col in columns:
            if method == 'iqr':
                Q1 = df_copy[col].quantile(0.25)
                Q3 = df_copy[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                df_copy = df_copy[
                    (df_copy[col] >= lower_bound) & (df_copy[col] <= upper_bound)
                ]

            elif method == 'zscore':
                z_scores = np.abs((df_copy[col] - df_copy[col].mean()) / df_copy[col].std())
                df_copy = df_copy[z_scores < threshold]

        return df_copy

    def create_bins(
        self,
        df: pd.DataFrame,
        column: str,
        bins: Union[int, List[float]],
        labels: Optional[List[str]] = None,
        new_column: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Create bins (categories) from numeric column.

        Args:
            df: Input DataFrame
            column: Column to bin
            bins: Number of bins or list of bin edges
            labels: Labels for bins
            new_column: Name for new column (None = replace original)

        Returns:
            DataFrame with binned column
        """
        df_copy = df.copy()
        target_col = new_column if new_column else column

        logger.info(f"Creating bins for column: {column}")

        df_copy[target_col] = pd.cut(
            df_copy[column],
            bins=bins,
            labels=labels,
            include_lowest=True
        )

        return df_copy

    def apply_transform(
        self,
        df: pd.DataFrame,
        column: str,
        transform: str,
        new_column: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Apply mathematical transformation.

        Args:
            df: Input DataFrame
            column: Column to transform
            transform: 'log', 'sqrt', 'square', 'inverse'
            new_column: Name for new column (None = replace original)

        Returns:
            Transformed DataFrame
        """
        df_copy = df.copy()
        target_col = new_column if new_column else column

        logger.info(f"Applying {transform} transformation to column: {column}")

        if transform == 'log':
            df_copy[target_col] = np.log1p(df_copy[column])  # log(1 + x) to handle zeros
        elif transform == 'sqrt':
            df_copy[target_col] = np.sqrt(np.abs(df_copy[column]))
        elif transform == 'square':
            df_copy[target_col] = df_copy[column] ** 2
        elif transform == 'inverse':
            df_copy[target_col] = 1 / (df_copy[column] + 1e-10)  # avoid division by zero
        else:
            raise ValueError(f"Unknown transform: {transform}")

        return df_copy

    def create_date_features(
        self,
        df: pd.DataFrame,
        column: str,
        features: List[str] = ['year', 'month', 'day', 'dayofweek']
    ) -> pd.DataFrame:
        """
        Extract date features from datetime column.

        Args:
            df: Input DataFrame
            column: Datetime column
            features: List of features to extract

        Returns:
            DataFrame with new date features
        """
        df_copy = df.copy()

        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(df_copy[column]):
            df_copy[column] = pd.to_datetime(df_copy[column])

        logger.info(f"Extracting date features from column: {column}")

        feature_map = {
            'year': lambda x: x.dt.year,
            'month': lambda x: x.dt.month,
            'day': lambda x: x.dt.day,
            'dayofweek': lambda x: x.dt.dayofweek,
            'quarter': lambda x: x.dt.quarter,
            'week': lambda x: x.dt.isocalendar().week,
            'hour': lambda x: x.dt.hour,
            'minute': lambda x: x.dt.minute
        }

        for feature in features:
            if feature in feature_map:
                df_copy[f"{column}_{feature}"] = feature_map[feature](df_copy[column])

        return df_copy

    def remove_duplicates(
        self,
        df: pd.DataFrame,
        subset: Optional[List[str]] = None,
        keep: str = 'first'
    ) -> pd.DataFrame:
        """
        Remove duplicate rows.

        Args:
            df: Input DataFrame
            subset: Columns to consider for duplicates (None = all)
            keep: 'first', 'last', or False

        Returns:
            DataFrame without duplicates
        """
        logger.info(f"Removing duplicates, keeping: {keep}")
        return df.drop_duplicates(subset=subset, keep=keep)

    def filter_rows(
        self,
        df: pd.DataFrame,
        conditions: List[Dict[str, Any]]
    ) -> pd.DataFrame:
        """
        Filter rows based on conditions.

        Args:
            df: Input DataFrame
            conditions: List of condition dicts with 'column', 'operator', 'value'

        Returns:
            Filtered DataFrame
        """
        df_copy = df.copy()

        for condition in conditions:
            column = condition['column']
            operator = condition['operator']
            value = condition['value']

            if operator == '==':
                df_copy = df_copy[df_copy[column] == value]
            elif operator == '!=':
                df_copy = df_copy[df_copy[column] != value]
            elif operator == '>':
                df_copy = df_copy[df_copy[column] > value]
            elif operator == '>=':
                df_copy = df_copy[df_copy[column] >= value]
            elif operator == '<':
                df_copy = df_copy[df_copy[column] < value]
            elif operator == '<=':
                df_copy = df_copy[df_copy[column] <= value]
            elif operator == 'in':
                df_copy = df_copy[df_copy[column].isin(value)]
            elif operator == 'not in':
                df_copy = df_copy[~df_copy[column].isin(value)]

        return df_copy
