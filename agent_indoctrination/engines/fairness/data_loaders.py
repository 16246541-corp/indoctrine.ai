"""
Standard fairness dataset loaders.

Provides loaders for widely-used fairness benchmark datasets:
- Adult Income (UCI Adult / Census Income)
- COMPAS (ProPublica recidivism)
- German Credit (UCI)

Note: These loaders expect data files to be available locally or will
provide instructions for obtaining them.
"""

from typing import Tuple, Dict, Optional
import numpy as np
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_adult(
    data_path: Optional[str] = None,
    sensitive: str = "sex",
    return_dataframe: bool = False,
) -> Tuple:
    """
    Load Adult Income dataset (UCI Adult / Census Income).
    
    Binary classification: income >50K (1) vs <=50K (0)
    Sensitive attributes: sex, race, age
    
    Args:
        data_path: Path to adult.data file (if None, provides download instructions)
        sensitive: Which sensitive attribute to return ('sex', 'race', or 'age')
        return_dataframe: If True, return full DataFrame instead of (X, y, A)
        
    Returns:
        If return_dataframe: DataFrame
        Else: (X, y, sensitive_attr) where X is features, y is binary label, A is sensitive
        
    Dataset info:
        - Source: https://archive.ics.uci.edu/ml/datasets/adult
        - 48,842 instances
        - Binary outcome: >50K income
        - Sensitive: sex (Male/Female), race, age
    """
    if data_path is None:
        raise FileNotFoundError(
            "Adult dataset not found. Download from:\n"
            "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data\n"
            "and pass path via data_path parameter."
        )
    
    # Column names for Adult dataset
    columns = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'
    ]
    
    try:
        df = pd.read_csv(data_path, names=columns, skipinitialspace=True, na_values='?')
        df = df.dropna()  # Remove missing values
        
        # Create binary label: 1 if >50K, 0 otherwise
        df['label'] = (df['income'] == '>50K').astype(int)
        
        # Extract sensitive attribute
        if sensitive == 'sex':
            df['sensitive'] = (df['sex'] == 'Male').astype(int)
        elif sensitive == 'race':
            df['sensitive'] = df['race']
        elif sensitive == 'age':
            df['sensitive'] = (df['age'] >= 45).astype(int)  # Binary age threshold
        else:
            raise ValueError(f"Unknown sensitive attribute: {sensitive}")
        
        if return_dataframe:
            return df
        
        # Return features, labels, sensitive
        feature_cols = ['age', 'education-num', 'hours-per-week', 'capital-gain', 'capital-loss']
        X = df[feature_cols].values
        y = df['label'].values
        A = df['sensitive'].values
        
        logger.info(f"Loaded Adult dataset: {len(df)} samples, sensitive={sensitive}")
        return X, y, A
        
    except Exception as e:
        logger.error(f"Error loading Adult dataset: {e}")
        raise


def load_compas(
    data_path: Optional[str] = None,
    sensitive: str = "race",
    return_dataframe: bool = False,
) -> Tuple:
    """
    Load COMPAS recidivism dataset (ProPublica).
    
    Binary classification: two-year recidivism (1) vs no recidivism (0)
    Sensitive attributes: race, sex, age
    
    Args:
        data_path: Path to compas-scores-two-years.csv (if None, provides instructions)
        sensitive: Which sensitive attribute to return ('race', 'sex', or 'age')
        return_dataframe: If True, return full DataFrame
        
    Returns:
        If return_dataframe: DataFrame
        Else: (X, y, sensitive_attr)
        
    Dataset info:
        - Source: https://github.com/propublica/compas-analysis
        - ~7,000 instances
        - Binary outcome: recidivism within 2 years
        - Sensitive: race (African-American vs Caucasian), sex, age
    """
    if data_path is None:
        raise FileNotFoundError(
            "COMPAS dataset not found. Download from:\n"
            "https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv\n"
            "and pass path via data_path parameter."
        )
    
    try:
        df = pd.read_csv(data_path)
        
        # Standard COMPAS preprocessing
        df = df[
            (df['days_b_screening_arrest'] <= 30) &
            (df['days_b_screening_arrest'] >= -30) &
            (df['is_recid'] != -1) &
            (df['c_charge_degree'] != 'O') &
            (df['score_text'] != 'N/A')
        ]
        
        # Binary label: two-year recidivism
        df['label'] = df['two_year_recid'].astype(int)
        
        # Extract sensitive attribute
        if sensitive == 'race':
            # Binary: African-American (1) vs Caucasian (0)
            df = df[df['race'].isin(['African-American', 'Caucasian'])]
            df['sensitive'] = (df['race'] == 'African-American').astype(int)
        elif sensitive == 'sex':
            df['sensitive'] = (df['sex'] == 'Male').astype(int)
        elif sensitive == 'age':
            df['sensitive'] = (df['age'] >= 45).astype(int)
        else:
            raise ValueError(f"Unknown sensitive attribute: {sensitive}")
        
        if return_dataframe:
            return df
        
        # Return features, labels, sensitive
        feature_cols = ['age', 'priors_count', 'juv_fel_count', 'juv_misd_count']
        X = df[feature_cols].fillna(0).values
        y = df['label'].values
        A = df['sensitive'].values
        
        logger.info(f"Loaded COMPAS dataset: {len(df)} samples, sensitive={sensitive}")
        return X, y, A
        
    except Exception as e:
        logger.error(f"Error loading COMPAS dataset: {e}")
        raise


def load_german_credit(
    data_path: Optional[str] = None,
    sensitive: str = "sex",
    return_dataframe: bool = False,
) -> Tuple:
    """
    Load German Credit dataset (UCI).
    
    Binary classification: good credit (1) vs bad credit (0)
    Sensitive attributes: sex, age
    
    Args:
        data_path: Path to german.data file (if None, provides instructions)
        sensitive: Which sensitive attribute to return ('sex' or 'age')
        return_dataframe: If True, return full DataFrame
        
    Returns:
        If return_dataframe: DataFrame
        Else: (X, y, sensitive_attr)
        
    Dataset info:
        - Source: https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)
        - 1,000 instances
        - Binary outcome: good (1) vs bad (2) credit risk
        - Sensitive: sex (from personal status), age
    """
    if data_path is None:
        raise FileNotFoundError(
            "German Credit dataset not found. Download from:\n"
            "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data\n"
            "and pass path via data_path parameter."
        )
    
    try:
        # German credit has 20 attributes + 1 class
        df = pd.read_csv(data_path, sep=' ', header=None)
        
        # Last column is class: 1 (good) or 2 (bad)
        # Convert to binary: 1 (good) vs 0 (bad)
        df['label'] = (df[20] == 1).astype(int)
        
        # Extract sex from personal status (attribute 9)
        # A91: male divorced/separated, A92: female divorced/separated/married
        # A93: male single, A94: male married/widowed, A95: female single
        personal_status = df[8].astype(str)
        df['sex'] = personal_status.isin(['A91', 'A93', 'A94']).astype(int)  # 1=male, 0=female
        
        # Age is attribute 13
        df['age_num'] = df[12]
        df['age_binary'] = (df[12] >= 25).astype(int)  # Binary age threshold
        
        # Extract sensitive attribute
        if sensitive == 'sex':
            df['sensitive'] = df['sex']
        elif sensitive == 'age':
            df['sensitive'] = df['age_binary']
        else:
            raise ValueError(f"Unknown sensitive attribute: {sensitive}")
        
        if return_dataframe:
            return df
        
        # Return features, labels, sensitive
        # Use numeric features
        feature_cols = [1, 4, 12, 15, 17]  # Some numeric columns
        X = df[feature_cols].values
        y = df['label'].values
        A = df['sensitive'].values
        
        logger.info(f"Loaded German Credit dataset: {len(df)} samples, sensitive={sensitive}")
        return X, y, A
        
    except Exception as e:
        logger.error(f"Error loading German Credit dataset: {e}")
        raise


# Helper function to create example synthetic data for testing
def create_synthetic_fair_dataset(
    n_samples: int = 1000,
    bias_factor: float = 0.2,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create synthetic dataset with controllable bias for testing.
    
    Args:
        n_samples: Number of samples
        bias_factor: How much bias to introduce (0=fair, 1=max bias)
        
    Returns:
        (X, y, sensitive_attr)
    """
    np.random.seed(42)
    
    # Features
    X = np.random.randn(n_samples, 5)
    
    # Sensitive attribute (binary)
    A = np.random.binomial(1, 0.5, n_samples)
    
    # Create labels with bias
    true_scores = X[:, 0] + X[:, 1] * 0.5
    
    # Add bias based on sensitive attribute
    biased_scores = true_scores + A * bias_factor
    
    # Convert to binary labels
    y = (biased_scores > np.median(biased_scores)).astype(int)
    
    logger.info(f"Created synthetic dataset: {n_samples} samples, bias_factor={bias_factor}")
    return X, y, A
