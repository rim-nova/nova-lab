"""
Inferential Statistics Service
Implements SPSS-equivalent inferential tests (t-tests, ANOVA, regression, etc.)
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class InferentialStatsService:
    """Service for inferential statistical tests."""

    def __init__(self):
        """Initialize inferential statistics service."""
        pass

    def t_test(
        self,
        df: pd.DataFrame,
        dependent_var: str,
        test_type: str,
        independent_var: Optional[str] = None,
        test_value: float = 0,
        paired: bool = False,
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        Perform t-test (SPSS T-Test equivalent).

        Args:
            df: Input DataFrame
            dependent_var: Dependent variable
            test_type: 'one_sample', 'independent', or 'paired'
            independent_var: Independent variable (for independent/paired tests)
            test_value: Test value for one-sample test
            paired: Whether samples are paired
            alpha: Significance level

        Returns:
            T-test results
        """
        logger.info(f"Performing {test_type} t-test on {dependent_var}")

        result = {
            'test_type': test_type,
            'dependent_variable': dependent_var,
            'alpha': alpha
        }

        if test_type == 'one_sample':
            data = df[dependent_var].dropna()
            t_stat, p_value = stats.ttest_1samp(data, test_value)

            result.update({
                'test_value': test_value,
                'n': len(data),
                'mean': float(data.mean()),
                'std': float(data.std()),
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'df': len(data) - 1,
                'is_significant': bool(p_value < alpha),
                'mean_difference': float(data.mean() - test_value)
            })

            # Confidence interval
            ci = stats.t.interval(
                1 - alpha,
                len(data) - 1,
                loc=data.mean(),
                scale=stats.sem(data)
            )
            result['confidence_interval'] = {
                'lower': float(ci[0]),
                'upper': float(ci[1])
            }

        elif test_type == 'independent':
            if not independent_var:
                raise ValueError("independent_var required for independent t-test")

            groups = df.groupby(independent_var)[dependent_var].apply(list)

            if len(groups) != 2:
                raise ValueError("Independent variable must have exactly 2 groups")

            group_names = list(groups.index)
            group1_data = np.array(groups.iloc[0])
            group2_data = np.array(groups.iloc[1])

            # Remove NaN values
            group1_data = group1_data[~pd.isna(group1_data)]
            group2_data = group2_data[~pd.isna(group2_data)]

            # Levene's test for equality of variances
            levene_stat, levene_p = stats.levene(group1_data, group2_data)

            # t-test (equal and unequal variances)
            t_stat_equal, p_value_equal = stats.ttest_ind(group1_data, group2_data, equal_var=True)
            t_stat_unequal, p_value_unequal = stats.ttest_ind(group1_data, group2_data, equal_var=False)

            result.update({
                'independent_variable': independent_var,
                'group1': str(group_names[0]),
                'group2': str(group_names[1]),
                'group1_n': len(group1_data),
                'group2_n': len(group2_data),
                'group1_mean': float(np.mean(group1_data)),
                'group2_mean': float(np.mean(group2_data)),
                'group1_std': float(np.std(group1_data, ddof=1)),
                'group2_std': float(np.std(group2_data, ddof=1)),
                'mean_difference': float(np.mean(group1_data) - np.mean(group2_data)),
                'levene_test': {
                    'statistic': float(levene_stat),
                    'p_value': float(levene_p),
                    'equal_variances': bool(levene_p > 0.05)
                },
                'equal_variances': {
                    't_statistic': float(t_stat_equal),
                    'p_value': float(p_value_equal),
                    'df': len(group1_data) + len(group2_data) - 2,
                    'is_significant': bool(p_value_equal < alpha)
                },
                'unequal_variances': {
                    't_statistic': float(t_stat_unequal),
                    'p_value': float(p_value_unequal),
                    'is_significant': bool(p_value_unequal < alpha)
                }
            })

        elif test_type == 'paired':
            if not independent_var:
                raise ValueError("independent_var required for paired t-test")

            groups = df.groupby(independent_var)[dependent_var].apply(list)

            if len(groups) != 2:
                raise ValueError("Independent variable must have exactly 2 groups for paired test")

            group_names = list(groups.index)
            group1_data = np.array(groups.iloc[0])
            group2_data = np.array(groups.iloc[1])

            # Ensure equal length
            if len(group1_data) != len(group2_data):
                raise ValueError("Paired samples must have equal length")

            t_stat, p_value = stats.ttest_rel(group1_data, group2_data)

            result.update({
                'independent_variable': independent_var,
                'group1': str(group_names[0]),
                'group2': str(group_names[1]),
                'n_pairs': len(group1_data),
                'mean_difference': float(np.mean(group1_data - group2_data)),
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'df': len(group1_data) - 1,
                'is_significant': bool(p_value < alpha)
            })

        return result

    def anova(
        self,
        df: pd.DataFrame,
        dependent_var: str,
        factors: List[str],
        covariates: Optional[List[str]] = None,
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        Perform ANOVA (SPSS ANOVA/GLM equivalent).

        Args:
            df: Input DataFrame
            dependent_var: Dependent variable
            factors: List of factor variables
            covariates: List of covariates (for ANCOVA)
            alpha: Significance level

        Returns:
            ANOVA results
        """
        logger.info(f"Performing ANOVA on {dependent_var} with factors: {factors}")

        # Prepare data
        df_clean = df[[dependent_var] + factors + (covariates or [])].dropna()

        # Build formula
        formula_parts = [dependent_var, '~']
        formula_parts.append(' + '.join(factors))

        if covariates:
            formula_parts.append(' + ')
            formula_parts.append(' + '.join(covariates))

        formula = ''.join(formula_parts)

        # Fit model
        model = ols(formula, data=df_clean).fit()

        # ANOVA table
        anova_table = anova_lm(model, typ=2)  # Type II SS

        # Convert to dict
        anova_results = []
        for index, row in anova_table.iterrows():
            anova_results.append({
                'source': str(index),
                'sum_squares': float(row['sum_sq']),
                'df': int(row['df']),
                'mean_square': float(row['sum_sq'] / row['df']) if row['df'] > 0 else 0,
                'F': float(row['F']) if not pd.isna(row['F']) else None,
                'p_value': float(row['PR(>F)']) if not pd.isna(row['PR(>F)']) else None,
                'is_significant': bool(row['PR(>F)'] < alpha) if not pd.isna(row['PR(>F)']) else False
            })

        result = {
            'dependent_variable': dependent_var,
            'factors': factors,
            'covariates': covariates,
            'n': len(df_clean),
            'r_squared': float(model.rsquared),
            'adj_r_squared': float(model.rsquared_adj),
            'anova_table': anova_results,
            'model_summary': {
                'f_statistic': float(model.fvalue),
                'p_value': float(model.f_pvalue),
                'is_significant': bool(model.f_pvalue < alpha)
            }
        }

        return result

    def post_hoc_tukey(
        self,
        df: pd.DataFrame,
        dependent_var: str,
        factor: str,
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        Perform Tukey HSD post-hoc test.

        Args:
            df: Input DataFrame
            dependent_var: Dependent variable
            factor: Factor variable
            alpha: Significance level

        Returns:
            Tukey HSD results
        """
        logger.info(f"Performing Tukey HSD post-hoc test")

        df_clean = df[[dependent_var, factor]].dropna()

        tukey = pairwise_tukeyhsd(
            endog=df_clean[dependent_var],
            groups=df_clean[factor],
            alpha=alpha
        )

        # Convert to dict
        comparisons = []
        for i in range(len(tukey.summary().data) - 1):  # Skip header
            row = tukey.summary().data[i + 1]
            comparisons.append({
                'group1': str(row[0]),
                'group2': str(row[1]),
                'mean_diff': float(row[2]),
                'lower_ci': float(row[3]),
                'upper_ci': float(row[4]),
                'reject_null': bool(row[5])
            })

        return {
            'dependent_variable': dependent_var,
            'factor': factor,
            'alpha': alpha,
            'comparisons': comparisons
        }

    def correlation(
        self,
        df: pd.DataFrame,
        variables: List[str],
        method: str = 'pearson'
    ) -> Dict[str, Any]:
        """
        Compute correlation matrix (SPSS Correlations equivalent).

        Args:
            df: Input DataFrame
            variables: List of variables
            method: 'pearson', 'spearman', or 'kendall'

        Returns:
            Correlation results
        """
        logger.info(f"Computing {method} correlations for {len(variables)} variables")

        df_clean = df[variables].dropna()

        # Correlation matrix
        if method == 'pearson':
            corr_matrix = df_clean.corr(method='pearson')
        elif method == 'spearman':
            corr_matrix = df_clean.corr(method='spearman')
        elif method == 'kendall':
            corr_matrix = df_clean.corr(method='kendall')
        else:
            raise ValueError(f"Unknown method: {method}")

        # P-values
        n = len(df_clean)
        p_values = pd.DataFrame(np.zeros((len(variables), len(variables))),
                                index=variables, columns=variables)

        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i != j:
                    if method == 'pearson':
                        _, p = stats.pearsonr(df_clean[var1], df_clean[var2])
                    elif method == 'spearman':
                        _, p = stats.spearmanr(df_clean[var1], df_clean[var2])
                    elif method == 'kendall':
                        _, p = stats.kendalltau(df_clean[var1], df_clean[var2])
                    p_values.iloc[i, j] = p

        return {
            'method': method,
            'n': n,
            'variables': variables,
            'correlation_matrix': corr_matrix.to_dict(),
            'p_values': p_values.to_dict(),
            'significant_correlations': self._find_significant_correlations(
                corr_matrix, p_values
            )
        }

    def _find_significant_correlations(
        self,
        corr_matrix: pd.DataFrame,
        p_values: pd.DataFrame,
        alpha: float = 0.05
    ) -> List[Dict[str, Any]]:
        """Find significant correlations."""
        significant = []

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                var1 = corr_matrix.columns[i]
                var2 = corr_matrix.columns[j]
                corr = corr_matrix.iloc[i, j]
                p = p_values.iloc[i, j]

                if p < alpha:
                    significant.append({
                        'variable1': var1,
                        'variable2': var2,
                        'correlation': float(corr),
                        'p_value': float(p)
                    })

        return significant

    def linear_regression(
        self,
        df: pd.DataFrame,
        dependent_var: str,
        independent_vars: List[str],
        include_diagnostics: bool = True
    ) -> Dict[str, Any]:
        """
        Perform linear regression (SPSS Regression equivalent).

        Args:
            df: Input DataFrame
            dependent_var: Dependent variable
            independent_vars: List of independent variables
            include_diagnostics: Include diagnostic plots and tests

        Returns:
            Regression results
        """
        logger.info(f"Performing linear regression: {dependent_var} ~ {independent_vars}")

        # Prepare data
        df_clean = df[[dependent_var] + independent_vars].dropna()

        # Add constant
        X = sm.add_constant(df_clean[independent_vars])
        y = df_clean[dependent_var]

        # Fit model
        model = sm.OLS(y, X).fit()

        # Coefficients
        coefficients = []
        for var in model.params.index:
            coef_data = {
                'variable': str(var),
                'coefficient': float(model.params[var]),
                'std_error': float(model.bse[var]),
                't_statistic': float(model.tvalues[var]),
                'p_value': float(model.pvalues[var]),
                'ci_lower': float(model.conf_int().loc[var, 0]),
                'ci_upper': float(model.conf_int().loc[var, 1]),
                'is_significant': bool(model.pvalues[var] < 0.05)
            }
            coefficients.append(coef_data)

        result = {
            'dependent_variable': dependent_var,
            'independent_variables': independent_vars,
            'n': len(df_clean),
            'r_squared': float(model.rsquared),
            'adj_r_squared': float(model.rsquared_adj),
            'f_statistic': float(model.fvalue),
            'f_p_value': float(model.f_pvalue),
            'coefficients': coefficients,
            'aic': float(model.aic),
            'bic': float(model.bic)
        }

        if include_diagnostics:
            # VIF for multicollinearity
            from statsmodels.stats.outliers_influence import variance_inflation_factor

            vif_data = []
            for i, var in enumerate(independent_vars):
                vif = variance_inflation_factor(X.values, i + 1)  # +1 for constant
                vif_data.append({
                    'variable': var,
                    'vif': float(vif),
                    'has_multicollinearity': bool(vif > 10)
                })

            result['vif'] = vif_data

            # Durbin-Watson statistic
            from statsmodels.stats.stattools import durbin_watson
            dw = durbin_watson(model.resid)
            result['durbin_watson'] = float(dw)

        return result

    def logistic_regression(
        self,
        df: pd.DataFrame,
        dependent_var: str,
        independent_vars: List[str]
    ) -> Dict[str, Any]:
        """
        Perform logistic regression (SPSS Logistic Regression equivalent).

        Args:
            df: Input DataFrame
            dependent_var: Binary dependent variable
            independent_vars: List of independent variables

        Returns:
            Logistic regression results
        """
        logger.info(f"Performing logistic regression: {dependent_var} ~ {independent_vars}")

        # Prepare data
        df_clean = df[[dependent_var] + independent_vars].dropna()

        # Add constant
        X = sm.add_constant(df_clean[independent_vars])
        y = df_clean[dependent_var]

        # Fit model
        model = sm.Logit(y, X).fit(disp=0)

        # Coefficients and odds ratios
        coefficients = []
        for var in model.params.index:
            odds_ratio = np.exp(model.params[var])
            coef_data = {
                'variable': str(var),
                'coefficient': float(model.params[var]),
                'std_error': float(model.bse[var]),
                'z_statistic': float(model.tvalues[var]),
                'p_value': float(model.pvalues[var]),
                'odds_ratio': float(odds_ratio),
                'or_ci_lower': float(np.exp(model.conf_int().loc[var, 0])),
                'or_ci_upper': float(np.exp(model.conf_int().loc[var, 1])),
                'is_significant': bool(model.pvalues[var] < 0.05)
            }
            coefficients.append(coef_data)

        return {
            'dependent_variable': dependent_var,
            'independent_variables': independent_vars,
            'n': len(df_clean),
            'pseudo_r_squared': float(model.prsquared),
            'log_likelihood': float(model.llf),
            'aic': float(model.aic),
            'bic': float(model.bic),
            'coefficients': coefficients
        }
