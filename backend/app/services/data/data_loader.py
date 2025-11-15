"""
Data Loading Service
Handles loading data from various sources
"""

import pandas as pd
import pyreadstat
from typing import Optional, Dict, Any, Tuple
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class DataLoaderService:
    """Service for loading data from various file formats and sources."""

    def __init__(self):
        """Initialize data loader service."""
        self.supported_formats = {
            'csv': self._load_csv,
            'tsv': self._load_tsv,
            'txt': self._load_txt,
            'excel': self._load_excel,
            'xls': self._load_excel,
            'xlsx': self._load_excel,
            'json': self._load_json,
            'parquet': self._load_parquet,
            'sav': self._load_spss,
            'dta': self._load_stata,
        }

    def load_file(
        self,
        file_path: str,
        file_format: Optional[str] = None,
        **kwargs
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load data from a file.

        Args:
            file_path: Path to the file
            file_format: File format (auto-detected if None)
            **kwargs: Additional arguments for the loader

        Returns:
            Tuple of (DataFrame, metadata)

        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Auto-detect format from extension
        if file_format is None:
            file_format = path.suffix.lstrip('.').lower()

        if file_format not in self.supported_formats:
            raise ValueError(
                f"Unsupported file format: {file_format}. "
                f"Supported formats: {list(self.supported_formats.keys())}"
            )

        logger.info(f"Loading file: {file_path} (format: {file_format})")

        # Load data using appropriate method
        loader = self.supported_formats[file_format]
        df, metadata = loader(file_path, **kwargs)

        # Add common metadata
        metadata.update({
            'file_path': str(file_path),
            'file_format': file_format,
            'row_count': len(df),
            'column_count': len(df.columns),
            'file_size': path.stat().st_size,
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
        })

        logger.info(
            f"Loaded {metadata['row_count']} rows and "
            f"{metadata['column_count']} columns"
        )

        return df, metadata

    def _load_csv(
        self,
        file_path: str,
        encoding: str = 'utf-8',
        delimiter: str = ',',
        **kwargs
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load CSV file."""
        try:
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                delimiter=delimiter,
                **kwargs
            )
            metadata = {
                'encoding': encoding,
                'delimiter': delimiter
            }
            return df, metadata
        except UnicodeDecodeError:
            # Try different encodings
            for enc in ['latin1', 'iso-8859-1', 'cp1252']:
                try:
                    df = pd.read_csv(file_path, encoding=enc, delimiter=delimiter, **kwargs)
                    metadata = {'encoding': enc, 'delimiter': delimiter}
                    return df, metadata
                except UnicodeDecodeError:
                    continue
            raise

    def _load_tsv(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load TSV file."""
        return self._load_csv(file_path, delimiter='\t', **kwargs)

    def _load_txt(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load TXT file (assumes tab or comma delimited)."""
        # Try to detect delimiter
        with open(file_path, 'r') as f:
            first_line = f.readline()
            delimiter = '\t' if '\t' in first_line else ','

        return self._load_csv(file_path, delimiter=delimiter, **kwargs)

    def _load_excel(self, file_path: str, sheet_name: int = 0, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load Excel file."""
        df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
        metadata = {'sheet_name': sheet_name}
        return df, metadata

    def _load_json(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load JSON file."""
        df = pd.read_json(file_path, **kwargs)
        metadata = {}
        return df, metadata

    def _load_parquet(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load Parquet file."""
        df = pd.read_parquet(file_path, **kwargs)
        metadata = {}
        return df, metadata

    def _load_spss(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load SPSS (.sav) file."""
        df, meta = pyreadstat.read_sav(file_path, **kwargs)
        metadata = {
            'variable_labels': meta.column_names_to_labels if hasattr(meta, 'column_names_to_labels') else {},
            'value_labels': meta.variable_value_labels if hasattr(meta, 'variable_value_labels') else {},
            'original_columns': meta.column_names if hasattr(meta, 'column_names') else []
        }
        return df, metadata

    def _load_stata(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load Stata (.dta) file."""
        df = pd.read_stata(file_path, **kwargs)
        metadata = {}
        return df, metadata

    def detect_encoding(self, file_path: str) -> str:
        """
        Detect file encoding.

        Args:
            file_path: Path to file

        Returns:
            Detected encoding
        """
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                continue

        return 'utf-8'  # default

    def preview_file(
        self,
        file_path: str,
        n_rows: int = 10,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Preview file without loading all data.

        Args:
            file_path: Path to file
            n_rows: Number of rows to preview

        Returns:
            Preview data and metadata
        """
        df, metadata = self.load_file(file_path, **kwargs)

        preview_df = df.head(n_rows)

        return {
            'preview': preview_df.to_dict(orient='records'),
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'row_count': len(df),
            'column_count': len(df.columns),
            'metadata': metadata
        }
