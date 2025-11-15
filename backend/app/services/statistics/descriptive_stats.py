"""
Descriptive Statistics Service
Implements SPSS-equivalent descriptive statistics
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class DescriptiveStatsService:
    """Service for descriptive statistics and data exploration."""

    def __init__(self):
        """Initialize descriptive statistics service."""
        pass

    def compute_descriptives(
        self,
        df: pd.DataFrame,
        variables: Optional[List[str]] = None,
        include_distribution: bool = True
    ) -> Dict[str, Any]:
        """
        Compute comprehensive descriptive statistics (SPSS Descriptives equivalent).

        Args:
            df: Input DataFrame
            variables: List of variables to analyze (None = all numeric)
            include_distribution: Include distribution tests

        Returns:
            Dictionary with descriptive statistics
        """
        if variables is None:
            variables = df.select_dtypes(include=[np.number]).columns.tolist()

        logger.info(f"Computing descriptive statistics for {len(variables)} variables")

        results = {}

        for var in variables:
            if var not in df.columns:
                continue

            data = df[var].dropna()

            if len(data) == 0:
                continue

            var_stats = {
                'variable': var,
                'n': len(data),
                'missing': int(df[var].isna().sum()),
                'mean': float(data.mean()),
                'std': float(data.std()),
                'variance': float(data.var()),
                'min': float(data.min()),
                'max': float(data.max()),
                'range': float(data.max() - data.min()),
                'median': float(data.median()),
                'q1': float(data.quantile(0.25)),
                'q3': float(data.quantile(0.75)),
                'iqr': float(data.quantile(0.75) - data.quantile(0.25)),
                'skewness': float(data.skew()),
                'kurtosis': float(data.kurtosis()),
                'se_mean': float(data.std() / np.sqrt(len(data))),
                'cv': float(data.std() / data.mean() * 100) if data.mean() != 0 else 0
            }

            # Distribution tests
            if include_distribution and len(data) >= 3:
                # Shapiro-Wilk test for normality
                if len(data) <= 5000:  # Shapiro-Wilk limit
                    shapiro_stat, shapiro_p = stats.shapiro(data)
                    var_stats['normality_test'] = {
                        'test': 'Shapiro-Wilk',
                        'statistic': float(shapiro_stat),
                        'p_value': float(shapiro_p),
                        'is_normal': bool(shapiro_p > 0.05)
                    }
                else:
                    # Use Kolmogorov-Smirnov for large samples
                    ks_stat, ks_p = stats.kstest(data, 'norm')
                    var_stats['normality_test'] = {
                        'test': 'Kolmogorov-Smirnov',
                        'statistic': float(ks_stat),
                        'p_value': float(ks_p),
                        'is_normal': bool(ks_p > 0.05)
                    }

            results[var] = var_stats

        return {
            'statistics': results,
            'summary': {
                'n_variables': len(results),
                'total_observations': len(df)
            }
        }

    def compute_frequencies(
        self,
        df: pd.DataFrame,
        variable: str,
        bins: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Compute frequency distribution (SPSS Frequencies equivalent).

        Args:
            df: Input DataFrame
            variable: Variable to analyze
            bins: Number of bins for numeric variables

        Returns:
            Frequency table with statistics
        """
        logger.info(f"Computing frequencies for variable: {variable}")

        data = df[variable]

        # Basic counts
        total = len(data)
        valid = data.notna().sum()
        missing = data.isna().sum()

        # Frequency distribution
        if pd.api.types.is_numeric_dtype(data) and bins:
            # Create bins for numeric data
            freq_table = pd.cut(data.dropna(), bins=bins).value_counts().sort_index()
        else:
            # Use value counts for categorical
            freq_table = data.value_counts()

        # Convert to detailed table
        frequencies = []
        cumulative_count = 0
        cumulative_percent = 0

        for value, count in freq_table.items():
            percent = (count / valid) * 100
            cumulative_count += count
            cumulative_percent += percent

            frequencies.append({
                'value': str(value),
                'count': int(count),
                'percent': float(percent),
                'valid_percent': float(percent),
                'cumulative_percent': float(cumulative_percent)
            })

        return {
            'variable': variable,
            'n': total,
            'valid': int(valid),
            'missing': int(missing),
            'frequencies': frequencies,
            'mode': str(data.mode()[0]) if len(data.mode()) > 0 else None,
            'unique_values': int(data.nunique())
        }

    def compute_crosstabs(
        self,
        df: pd.DataFrame,
        row_var: str,
        col_var: str,
        include_chi_square: bool = True
    ) -> Dict[str, Any]:
        """
        Compute crosstabulation (SPSS Crosstabs equivalent).

        Args:
            df: Input DataFrame
            row_var: Row variable
            col_var: Column variable
            include_chi_square: Include chi-square test

        Returns:
            Crosstab table with statistics
        """
        logger.info(f"Computing crosstab: {row_var} x {col_var}")

        # Create crosstab
        crosstab = pd.crosstab(
            df[row_var],
            df[col_var],
            margins=True,
            margins_name='Total'
        )

        # Row percentages
        row_pct = pd.crosstab(
            df[row_var],
            df[col_var],
            normalize='index'
        ) * 100

        # Column percentages
        col_pct = pd.crosstab(
            df[row_var],
            df[col_var],
            normalize='columns'
        ) * 100

        result = {
            'row_variable': row_var,
            'column_variable': col_var,
            'crosstab': crosstab.to_dict(),
            'row_percentages': row_pct.to_dict(),
            'column_percentages': col_pct.to_dict()
        }

        # Chi-square test
        if include_chi_square:
            # Remove margins for chi-square test
            observed = crosstab.iloc[:-1, :-1]

            if observed.shape[0] > 1 and observed.shape[1] > 1:
                chi2, p_value, dof, expected = stats.chi2_contingency(observed)

                result['chi_square'] = {
                    'statistic': float(chi2),
                    'p_value': float(p_value),
                    'df': int(dof),
                    'is_significant': bool(p_value < 0.05)
                }

                # Cramér's V
                n = observed.sum().sum()
                min_dim = min(observed.shape[0], observed.shape[1]) - 1
                cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0

                result['cramers_v'] = float(cramers_v)

        return result

    def explore(
        self,
        df: pd.DataFrame,
        variable: str,
        group_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive exploration (SPSS Explore equivalent).

        Args:
            df: Input DataFrame
            variable: Variable to explore
            group_by: Optional grouping variable

        Returns:
            Exploration results with tests
        """
        logger.info(f"Exploring variable: {variable}")

        if group_by:
            # Group-wise statistics
            groups = df.groupby(group_by)[variable].apply(lambda x: x.dropna())
            results = {}

            for group_name, group_data in groups.items():
                if len(group_data) > 0:
                    results[str(group_name)] = self._compute_explore_stats(group_data)

            return {
                'variable': variable,
                'group_by': group_by,
                'groups': results
            }
        else:
            # Overall statistics
            data = df[variable].dropna()
            return {
                'variable': variable,
                'statistics': self._compute_explore_stats(data)
            }

    def _compute_explore_stats(self, data: pd.Series) -> Dict[str, Any]:
        """Compute exploration statistics for a series."""
        stats_dict = {
            'n': len(data),
            'mean': float(data.mean()),
            'median': float(data.median()),
            'std': float(data.std()),
            'min': float(data.min()),
            'max': float(data.max()),
            'q1': float(data.quantile(0.25)),
            'q3': float(data.quantile(0.75)),
            'skewness': float(data.skew()),
            'kurtosis': float(data.kurtosis())
        }

        # 5% trimmed mean
        trimmed = data.sort_values()
        trim_size = int(len(data) * 0.05)
        if trim_size > 0:
            trimmed_data = trimmed[trim_size:-trim_size]
            stats_dict['trimmed_mean_5'] = float(trimmed_data.mean())

        # Outliers (beyond 1.5 * IQR)
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        stats_dict['n_outliers'] = len(outliers)

        return stats_dict
