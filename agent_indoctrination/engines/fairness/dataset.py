"""
Core data model for fairness evaluation.

Provides BinaryDataset class for holding predictions, ground truth,
and sensitive attributes for fairness metric computation.
"""

from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd
from dataclasses import dataclass, field


@dataclass
class GroupStats:
    """Cached statistics for a sensitive group."""
    
    tp: int = 0  # True positives
    fp: int = 0  # False positives
    tn: int = 0  # True negatives
    fn: int = 0  # False negatives
    
    @property
    def tpr(self) -> float:
        """True positive rate (sensitivity, recall)."""
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0.0
    
    @property
    def fpr(self) -> float:
        """False positive rate."""
        return self.fp / (self.fp + self.tn) if (self.fp + self.tn) > 0 else 0.0
    
    @property
    def tnr(self) -> float:
        """True negative rate (specificity)."""
        return self.tn / (self.tn + self.fp) if (self.tn + self.fp) > 0 else 0.0
    
    @property
    def fnr(self) -> float:
        """False negative rate (miss rate)."""
        return self.fn / (self.fn + self.tp) if (self.fn + self.tp) > 0 else 0.0
    
    @property
    def ppv(self) -> float:
        """Positive predictive value (precision)."""
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0.0
    
    @property
    def npv(self) -> float:
        """Negative predictive value."""
        return self.tn / (self.tn + self.fn) if (self.tn + self.fn) > 0 else 0.0
    
    @property
    def fdr(self) -> float:
        """False discovery rate."""
        return self.fp / (self.fp + self.tp) if (self.fp + self.tp) > 0 else 0.0
    
    @property
    def for_rate(self) -> float:
        """False omission rate."""
        return self.fn / (self.fn + self.tn) if (self.fn + self.tn) > 0 else 0.0
    
    @property
    def positive_rate(self) -> float:
        """Rate of positive predictions."""
        total = self.tp + self.fp + self.tn + self.fn
        return (self.tp + self.fp) / total if total > 0 else 0.0
    
    @property
    def error_rate(self) -> float:
        """Overall misclassification rate."""
        total = self.tp + self.fp + self.tn + self.fn
        return (self.fp + self.fn) / total if total > 0 else 0.0
    
    @property
    def n(self) -> int:
        """Total samples in group."""
        return self.tp + self.fp + self.tn + self.fn


class BinaryDataset:
    """
    Container for binary classification fairness evaluation.
    
    Holds predictions, ground truth, and sensitive attributes,
    and efficiently computes per-group confusion matrix statistics.
    
    Args:
        y_true: Ground truth binary labels (0 or 1)
        y_pred: Predicted binary labels (0 or 1)
        sensitive: Sensitive attribute(s) - dict of {attr_name: values} or array
        positive_label: Which label is considered positive (default: 1)
        sample_weight: Optional sample weights
        pair_id: Optional IDs for counterfactual pairs
    """
    
    def __init__(
        self,
        y_true: Union[np.ndarray, List],
        y_pred: Union[np.ndarray, List],
        sensitive: Union[Dict[str, Union[np.ndarray, List]], np.ndarray, List],
        positive_label: int = 1,
        sample_weight: Optional[Union[np.ndarray, List]] = None,
        pair_id: Optional[Union[np.ndarray, List]] = None,
    ):
        # Convert to numpy arrays
        self.y_true = np.asarray(y_true)
        self.y_pred = np.asarray(y_pred)
        self.positive_label = positive_label
        
        # Handle sensitive attributes
        if isinstance(sensitive, dict):
            self.sensitive = {k: np.asarray(v) for k, v in sensitive.items()}
            self.sensitive_names = list(sensitive.keys())
        else:
            self.sensitive = {"sensitive": np.asarray(sensitive)}
            self.sensitive_names = ["sensitive"]
        
        # Optional attributes
        self.sample_weight = np.asarray(sample_weight) if sample_weight is not None else None
        self.pair_id = np.asarray(pair_id) if pair_id is not None else None
        
        # Validate
        self._validate()
        
        # Cache for group statistics
        self._stats_cache: Dict[tuple, GroupStats] = {}
    
    def _validate(self):
        """Validate input data."""
        n = len(self.y_true)
        
        if len(self.y_pred) != n:
            raise ValueError(f"y_pred length {len(self.y_pred)} != y_true length {n}")
        
        for name, arr in self.sensitive.items():
            if len(arr) != n:
                raise ValueError(f"sensitive[{name}] length {len(arr)} != y_true length {n}")
        
        if self.sample_weight is not None and len(self.sample_weight) != n:
            raise ValueError(f"sample_weight length {len(self.sample_weight)} != y_true length {n}")
        
        if self.pair_id is not None and len(self.pair_id) != n:
            raise ValueError(f"pair_id length {len(self.pair_id)} != y_true length {n}")
        
        # Check binary labels
        unique_true = np.unique(self.y_true)
        unique_pred = np.unique(self.y_pred)
        
        if not set(unique_true).issubset({0, 1}):
            raise ValueError(f"y_true must be binary (0 or 1), got {unique_true}")
        if not set(unique_pred).issubset({0, 1}):
            raise ValueError(f"y_pred must be binary (0 or 1), got {unique_pred}")
    
    def get_group_stats(self, sensitive_attr: str, group_value) -> GroupStats:
        """
        Get cached confusion matrix statistics for a specific group.
        
        Args:
            sensitive_attr: Name of sensitive attribute
            group_value: Value of the group
            
        Returns:
            GroupStats object with TP, FP, TN, FN and derived rates
        """
        cache_key = (sensitive_attr, group_value)
        
        if cache_key in self._stats_cache:
            return self._stats_cache[cache_key]
        
        # Compute stats
        if sensitive_attr not in self.sensitive:
            raise ValueError(f"Sensitive attribute '{sensitive_attr}' not found")
        
        mask = self.sensitive[sensitive_attr] == group_value
        y_true_group = self.y_true[mask]
        y_pred_group = self.y_pred[mask]
        
        stats = GroupStats(
            tp=int(np.sum((y_true_group == 1) & (y_pred_group == 1))),
            fp=int(np.sum((y_true_group == 0) & (y_pred_group == 1))),
            tn=int(np.sum((y_true_group == 0) & (y_pred_group == 0))),
            fn=int(np.sum((y_true_group == 1) & (y_pred_group == 0))),
        )
        
        self._stats_cache[cache_key] = stats
        return stats
    
    def get_groups(self, sensitive_attr: str) -> List:
        """Get unique values for a sensitive attribute."""
        if sensitive_attr not in self.sensitive:
            raise ValueError(f"Sensitive attribute '{sensitive_attr}' not found")
        return list(np.unique(self.sensitive[sensitive_attr]))
    
    @property
    def n_samples(self) -> int:
        """Total number of samples."""
        return len(self.y_true)
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert to pandas DataFrame."""
        df = pd.DataFrame({
            'y_true': self.y_true,
            'y_pred': self.y_pred,
        })
        
        for name, arr in self.sensitive.items():
            df[name] = arr
        
        if self.sample_weight is not None:
            df['sample_weight'] = self.sample_weight
        
        if self.pair_id is not None:
            df['pair_id'] = self.pair_id
        
        return df

    def check_data_quality(self) -> Dict[str, List[str]]:
        """
        Check for common data quality issues that affect fairness metrics.
        
        Returns:
            Dict with 'errors', 'warnings', 'info' lists.
        """
        issues = {"errors": [], "warnings": [], "info": []}
        
        # 1. Class Imbalance
        pos_rate = np.mean(self.y_true)
        if pos_rate < 0.05 or pos_rate > 0.95:
            issues["warnings"].append(
                f"Severe class imbalance: {pos_rate*100:.1f}% positive class. "
                "Some metrics may be unstable."
            )
        
        # 2. Group Size Imbalance & Empty Groups
        for attr in self.sensitive_names:
            groups = np.unique(self.sensitive[attr])
            sizes = [np.sum(self.sensitive[attr] == g) for g in groups]
            
            if len(sizes) == 0:
                issues["errors"].append(f"Sensitive attribute '{attr}' has no groups.")
                continue
                
            min_size = min(sizes)
            max_size = max(sizes)
            
            if min_size < 10:
                issues["warnings"].append(
                    f"Very small group in '{attr}': min size {min_size}. "
                    "Statistical significance is low."
                )
            
            if min_size / max_size < 0.1:
                issues["info"].append(
                    f"Group imbalance in '{attr}': min/max ratio {min_size/max_size:.2f}."
                )
        
        # 3. Missing Values (NaNs)
        for attr in self.sensitive_names:
            # Check for NaN/None in object arrays or float arrays
            arr = self.sensitive[attr]
            n_missing = 0
            
            if arr.dtype.kind in 'fc':  # float/complex
                n_missing = np.sum(np.isnan(arr))
            elif arr.dtype.kind in 'OSU':  # object/string/unicode
                # Check for None or 'nan' string
                n_missing = sum(1 for x in arr if x is None or (isinstance(x, float) and np.isnan(x)))
                
            if n_missing > 0:
                issues["warnings"].append(
                    f"Missing values in '{attr}': {n_missing} samples. "
                    "These may be excluded from group stats."
                )
                
        return issues
