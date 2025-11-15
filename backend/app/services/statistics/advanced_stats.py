"""
Advanced Statistics Service
Implements factor analysis, cluster analysis, reliability analysis, etc.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class AdvancedStatsService:
    """Service for advanced statistical analyses."""

    def __init__(self):
        """Initialize advanced statistics service."""
        pass

    def factor_analysis(
        self,
        df: pd.DataFrame,
        variables: List[str],
        n_factors: Optional[int] = None,
        rotation: str = 'varimax',
        method: str = 'principal'
    ) -> Dict[str, Any]:
        """
        Perform Exploratory Factor Analysis (SPSS Factor Analysis equivalent).

        Args:
            df: Input DataFrame
            variables: List of variables
            n_factors: Number of factors (None = auto-determine)
            rotation: 'varimax', 'oblimin', or 'none'
            method: 'principal' (PCA) or 'ml' (maximum likelihood)

        Returns:
            Factor analysis results
        """
        logger.info(f"Performing factor analysis on {len(variables)} variables")

        df_clean = df[variables].dropna()
        data = df_clean.values

        # Determine number of factors if not specified
        if n_factors is None:
            # Use Kaiser criterion (eigenvalue > 1)
            pca_temp = PCA()
            pca_temp.fit(data)
            n_factors = sum(pca_temp.explained_variance_ > 1)
            logger.info(f"Auto-determined {n_factors} factors using Kaiser criterion")

        # Perform factor analysis
        if method == 'principal':
            fa = PCA(n_components=n_factors)
        else:
            fa = FactorAnalysis(n_components=n_factors, rotation=None)

        fa.fit(data)

        # Get loadings
        if method == 'principal':
            loadings = fa.components_.T * np.sqrt(fa.explained_variance_)
        else:
            loadings = fa.components_.T

        # Create loadings dataframe
        loadings_df = pd.DataFrame(
            loadings,
            columns=[f'Factor{i+1}' for i in range(n_factors)],
            index=variables
        )

        # Communalities (proportion of variance explained for each variable)
        communalities = np.sum(loadings**2, axis=1)

        # Eigenvalues and variance explained
        if method == 'principal':
            eigenvalues = fa.explained_variance_
            variance_explained = fa.explained_variance_ratio_
        else:
            # Approximate for ML method
            eigenvalues = np.sum(loadings**2, axis=0)
            variance_explained = eigenvalues / np.sum(eigenvalues)

        # Scree plot data
        scree_data = []
        for i in range(min(len(eigenvalues), 10)):
            scree_data.append({
                'component': i + 1,
                'eigenvalue': float(eigenvalues[i]),
                'variance_explained': float(variance_explained[i]) * 100
            })

        return {
            'n_factors': n_factors,
            'n_variables': len(variables),
            'n_observations': len(df_clean),
            'method': method,
            'rotation': rotation,
            'loadings': loadings_df.to_dict(),
            'communalities': {var: float(comm) for var, comm in zip(variables, communalities)},
            'eigenvalues': [float(x) for x in eigenvalues],
            'variance_explained': [float(x) * 100 for x in variance_explained],
            'cumulative_variance': [float(x) * 100 for x in np.cumsum(variance_explained)],
            'scree_data': scree_data
        }

    def reliability_analysis(
        self,
        df: pd.DataFrame,
        items: List[str]
    ) -> Dict[str, Any]:
        """
        Perform reliability analysis (SPSS Reliability/Cronbach's Alpha).

        Args:
            df: Input DataFrame
            items: List of item variables

        Returns:
            Reliability statistics
        """
        logger.info(f"Performing reliability analysis on {len(items)} items")

        df_clean = df[items].dropna()

        # Cronbach's Alpha
        def cronbach_alpha(df):
            n_items = df.shape[1]
            if n_items < 2:
                return 0

            item_variances = df.var(axis=0, ddof=1)
            total_var = df.sum(axis=1).var(ddof=1)
            return (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_var)

        alpha = cronbach_alpha(df_clean)

        # Item statistics
        item_stats = []
        for item in items:
            item_mean = df_clean[item].mean()
            item_std = df_clean[item].std()

            # Corrected item-total correlation
            total_without_item = df_clean.drop(columns=[item]).sum(axis=1)
            corr = df_clean[item].corr(total_without_item)

            # Alpha if item deleted
            alpha_if_deleted = cronbach_alpha(df_clean.drop(columns=[item]))

            item_stats.append({
                'item': item,
                'mean': float(item_mean),
                'std': float(item_std),
                'item_total_correlation': float(corr),
                'alpha_if_deleted': float(alpha_if_deleted)
            })

        return {
            'n_items': len(items),
            'n_observations': len(df_clean),
            'cronbach_alpha': float(alpha),
            'reliability_level': self._interpret_alpha(alpha),
            'item_statistics': item_stats,
            'scale_mean': float(df_clean.sum(axis=1).mean()),
            'scale_variance': float(df_clean.sum(axis=1).var())
        }

    def _interpret_alpha(self, alpha: float) -> str:
        """Interpret Cronbach's alpha value."""
        if alpha >= 0.9:
            return 'Excellent'
        elif alpha >= 0.8:
            return 'Good'
        elif alpha >= 0.7:
            return 'Acceptable'
        elif alpha >= 0.6:
            return 'Questionable'
        elif alpha >= 0.5:
            return 'Poor'
        else:
            return 'Unacceptable'

    def cluster_analysis(
        self,
        df: pd.DataFrame,
        variables: List[str],
        n_clusters: int,
        method: str = 'kmeans',
        distance_metric: str = 'euclidean'
    ) -> Dict[str, Any]:
        """
        Perform cluster analysis (SPSS Cluster Analysis equivalent).

        Args:
            df: Input DataFrame
            variables: List of variables for clustering
            n_clusters: Number of clusters
            method: 'kmeans' or 'hierarchical'
            distance_metric: Distance metric for hierarchical

        Returns:
            Cluster analysis results
        """
        logger.info(f"Performing {method} clustering with {n_clusters} clusters")

        df_clean = df[variables].dropna()
        data = df_clean.values

        # Perform clustering
        if method == 'kmeans':
            clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        elif method == 'hierarchical':
            clusterer = AgglomerativeClustering(
                n_clusters=n_clusters,
                metric=distance_metric,
                linkage='ward' if distance_metric == 'euclidean' else 'complete'
            )
        else:
            raise ValueError(f"Unknown method: {method}")

        labels = clusterer.fit_predict(data)

        # Compute silhouette score
        if len(set(labels)) > 1:
            silhouette_avg = silhouette_score(data, labels)
        else:
            silhouette_avg = 0

        # Cluster centers (for k-means)
        if method == 'kmeans':
            centers = clusterer.cluster_centers_
            centers_df = pd.DataFrame(
                centers,
                columns=variables,
                index=[f'Cluster {i+1}' for i in range(n_clusters)]
            )
        else:
            # Compute mean for each cluster
            df_with_clusters = df_clean.copy()
            df_with_clusters['Cluster'] = labels
            centers_df = df_with_clusters.groupby('Cluster')[variables].mean()

        # Cluster sizes
        cluster_sizes = pd.Series(labels).value_counts().sort_index()

        # Within-cluster sum of squares
        wcss = 0
        for i in range(n_clusters):
            cluster_data = data[labels == i]
            if len(cluster_data) > 0:
                center = centers_df.iloc[i].values if method == 'kmeans' else cluster_data.mean(axis=0)
                wcss += np.sum((cluster_data - center) ** 2)

        return {
            'method': method,
            'n_clusters': n_clusters,
            'n_observations': len(df_clean),
            'n_variables': len(variables),
            'variables': variables,
            'cluster_labels': labels.tolist(),
            'cluster_sizes': cluster_sizes.to_dict(),
            'cluster_centers': centers_df.to_dict(),
            'silhouette_score': float(silhouette_avg),
            'wcss': float(wcss),
            'quality': self._interpret_silhouette(silhouette_avg)
        }

    def _interpret_silhouette(self, score: float) -> str:
        """Interpret silhouette score."""
        if score >= 0.7:
            return 'Strong structure'
        elif score >= 0.5:
            return 'Reasonable structure'
        elif score >= 0.25:
            return 'Weak structure'
        else:
            return 'No substantial structure'

    def nonparametric_tests(
        self,
        df: pd.DataFrame,
        test_type: str,
        dependent_var: str,
        independent_var: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform nonparametric tests (Mann-Whitney, Wilcoxon, Kruskal-Wallis, etc.).

        Args:
            df: Input DataFrame
            test_type: 'mann_whitney', 'wilcoxon', 'kruskal_wallis', 'friedman'
            dependent_var: Dependent variable
            independent_var: Independent variable (for between-group tests)

        Returns:
            Test results
        """
        logger.info(f"Performing {test_type} test")

        result = {'test_type': test_type, 'dependent_variable': dependent_var}

        if test_type == 'mann_whitney':
            # Mann-Whitney U test (independent samples)
            groups = df.groupby(independent_var)[dependent_var].apply(list)
            if len(groups) != 2:
                raise ValueError("Mann-Whitney requires exactly 2 groups")

            group1 = np.array(groups.iloc[0])
            group2 = np.array(groups.iloc[1])

            statistic, p_value = stats.mannwhitneyu(group1, group2, alternative='two-sided')

            result.update({
                'independent_variable': independent_var,
                'n_group1': len(group1),
                'n_group2': len(group2),
                'u_statistic': float(statistic),
                'p_value': float(p_value),
                'is_significant': bool(p_value < 0.05)
            })

        elif test_type == 'wilcoxon':
            # Wilcoxon signed-rank test (paired samples)
            groups = df.groupby(independent_var)[dependent_var].apply(list)
            if len(groups) != 2:
                raise ValueError("Wilcoxon requires exactly 2 groups")

            group1 = np.array(groups.iloc[0])
            group2 = np.array(groups.iloc[1])

            statistic, p_value = stats.wilcoxon(group1, group2)

            result.update({
                'independent_variable': independent_var,
                'n_pairs': len(group1),
                'w_statistic': float(statistic),
                'p_value': float(p_value),
                'is_significant': bool(p_value < 0.05)
            })

        elif test_type == 'kruskal_wallis':
            # Kruskal-Wallis H test (multiple independent groups)
            groups = df.groupby(independent_var)[dependent_var].apply(list)
            group_data = [np.array(g) for g in groups]

            statistic, p_value = stats.kruskal(*group_data)

            result.update({
                'independent_variable': independent_var,
                'n_groups': len(groups),
                'h_statistic': float(statistic),
                'p_value': float(p_value),
                'is_significant': bool(p_value < 0.05)
            })

        return result
