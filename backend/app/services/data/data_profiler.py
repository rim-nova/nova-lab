"""
Data Profiling Service
Provides comprehensive data profiling and EDA
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class DataProfilerService:
    """Service for profiling and analyzing datasets."""

    def __init__(self):
        """Initialize data profiler service."""
        pass

    def profile_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive data profile.

        Args:
            df: Pandas DataFrame

        Returns:
            Dictionary with profile information
        """
        logger.info(f"Profiling dataset with {len(df)} rows and {len(df.columns)} columns")

        profile = {
            'overview': self._get_overview(df),
            'columns': self._profile_columns(df),
            'correlations': self._get_correlations(df),
            'missing_data': self._analyze_missing_data(df),
            'warnings': self._generate_warnings(df)
        }

        return profile

    def _get_overview(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get dataset overview."""
        return {
            'row_count': len(df),
            'column_count': len(df.columns),
            'memory_usage': int(df.memory_usage(deep=True).sum()),
            'duplicated_rows': int(df.duplicated().sum()),
            'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns),
            'datetime_columns': len(df.select_dtypes(include=['datetime']).columns)
        }

    def _profile_columns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Profile each column."""
        columns_info = []

        for col in df.columns:
            col_info = {
                'name': col,
                'dtype': str(df[col].dtype),
                'missing_count': int(df[col].isna().sum()),
                'missing_percent': float(df[col].isna().sum() / len(df) * 100),
                'unique_count': int(df[col].nunique()),
                'unique_percent': float(df[col].nunique() / len(df) * 100)
            }

            # Type-specific statistics
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info.update(self._profile_numeric_column(df[col]))
            elif pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == 'object':
                col_info.update(self._profile_categorical_column(df[col]))
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                col_info.update(self._profile_datetime_column(df[col]))

            columns_info.append(col_info)

        return columns_info

    def _profile_numeric_column(self, series: pd.Series) -> Dict[str, Any]:
        """Profile numeric column."""
        valid_data = series.dropna()

        if len(valid_data) == 0:
            return {}

        return {
            'min': float(valid_data.min()),
            'max': float(valid_data.max()),
            'mean': float(valid_data.mean()),
            'median': float(valid_data.median()),
            'std': float(valid_data.std()),
            'q1': float(valid_data.quantile(0.25)),
            'q3': float(valid_data.quantile(0.75)),
            'skewness': float(valid_data.skew()),
            'kurtosis': float(valid_data.kurtosis()),
            'zeros': int((valid_data == 0).sum()),
            'negatives': int((valid_data < 0).sum())
        }

    def _profile_categorical_column(self, series: pd.Series) -> Dict[str, Any]:
        """Profile categorical column."""
        valid_data = series.dropna()

        if len(valid_data) == 0:
            return {}

        value_counts = valid_data.value_counts()
        top_values = value_counts.head(10).to_dict()

        return {
            'top_values': {str(k): int(v) for k, v in top_values.items()},
            'mode': str(valid_data.mode()[0]) if len(valid_data.mode()) > 0 else None,
            'mode_frequency': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0
        }

    def _profile_datetime_column(self, series: pd.Series) -> Dict[str, Any]:
        """Profile datetime column."""
        valid_data = series.dropna()

        if len(valid_data) == 0:
            return {}

        return {
            'min': str(valid_data.min()),
            'max': str(valid_data.max()),
            'range_days': (valid_data.max() - valid_data.min()).days
        }

    def _get_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate correlations for numeric columns."""
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.shape[1] < 2:
            return {}

        corr_matrix = numeric_df.corr()

        # Get strong correlations (> 0.7 or < -0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': float(corr_value)
                    })

        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'strong_correlations': strong_correlations
        }

    def _analyze_missing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing data patterns."""
        total_cells = df.shape[0] * df.shape[1]
        total_missing = df.isna().sum().sum()

        missing_by_column = df.isna().sum()
        columns_with_missing = missing_by_column[missing_by_column > 0].to_dict()

        missing_by_row = df.isna().sum(axis=1)
        rows_with_missing = int((missing_by_row > 0).sum())

        return {
            'total_missing': int(total_missing),
            'total_missing_percent': float(total_missing / total_cells * 100),
            'columns_with_missing': {str(k): int(v) for k, v in columns_with_missing.items()},
            'rows_with_missing': rows_with_missing,
            'rows_with_missing_percent': float(rows_with_missing / len(df) * 100)
        }

    def _generate_warnings(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate warnings about data quality issues."""
        warnings = []

        # Check for high missing percentages
        for col in df.columns:
            missing_pct = df[col].isna().sum() / len(df) * 100
            if missing_pct > 50:
                warnings.append({
                    'type': 'high_missing',
                    'column': col,
                    'message': f"Column '{col}' has {missing_pct:.1f}% missing values"
                })

        # Check for constant columns
        for col in df.columns:
            if df[col].nunique() == 1:
                warnings.append({
                    'type': 'constant_column',
                    'column': col,
                    'message': f"Column '{col}' has only one unique value"
                })

        # Check for high cardinality in object columns
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() > 0.9 * len(df):
                warnings.append({
                    'type': 'high_cardinality',
                    'column': col,
                    'message': f"Column '{col}' has very high cardinality (possible ID field)"
                })

        # Check for skewed numeric distributions
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].notna().sum() > 0:
                skewness = abs(df[col].skew())
                if skewness > 2:
                    warnings.append({
                        'type': 'highly_skewed',
                        'column': col,
                        'message': f"Column '{col}' is highly skewed (skewness: {skewness:.2f})"
                    })

        return warnings

    def get_sample_data(
        self,
        df: pd.DataFrame,
        n_rows: int = 100,
        strategy: str = 'random'
    ) -> pd.DataFrame:
        """
        Get sample of data.

        Args:
            df: DataFrame
            n_rows: Number of rows to sample
            strategy: 'random', 'head', or 'tail'

        Returns:
            Sampled DataFrame
        """
        if strategy == 'head':
            return df.head(n_rows)
        elif strategy == 'tail':
            return df.tail(n_rows)
        else:  # random
            return df.sample(min(n_rows, len(df)))
