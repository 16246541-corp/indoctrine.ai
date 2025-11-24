"""
Fairness metrics implementation.

Implements the 15 objective fairness metrics from:
"Objective metrics for ethical AI: a systematic literature review"

All metrics follow the formal definitions and formulas from section 3.3.
"""

from typing import Dict, Optional
import numpy as np
from .dataset import BinaryDataset, GroupStats


def demographic_parity(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    Demographic parity (statistical parity, independence).
    
    Measures difference in positive outcome rates between groups.
    Perfect fairness when difference = 0.
    
    Formula: P(Ŷ=1|A=a) - P(Ŷ=1|A=b)
    
    Args:
        dataset: BinaryDataset with predictions and sensitive attributes
        group_a: Unprivileged group value
        group_b: Privileged group value
        sensitive_attr: Name of sensitive attribute
        
    Returns:
        Difference in positive rates (0 = perfect parity)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    return stats_a.positive_rate - stats_b.positive_rate


def equalized_odds(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> Dict[str, float]:
    """
    Equalized odds (separation, conditional procedure accuracy equality).
    
    Both TPR and FPR should be equal across groups.
    
    Formula: 
        TPR: P(Ŷ=1|Y=1,A=a) = P(Ŷ=1|Y=1,A=b)
        FPR: P(Ŷ=1|Y=0,A=a) = P(Ŷ=1|Y=0,A=b)
    
    Returns:
        Dict with tpr_diff, fpr_diff, and avg_diff
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    tpr_diff = stats_a.tpr - stats_b.tpr
    fpr_diff = stats_a.fpr - stats_b.fpr
    
    return {
        "tpr_diff": tpr_diff,
        "fpr_diff": fpr_diff,
        "avg_diff": (abs(tpr_diff) + abs(fpr_diff)) / 2,
    }


def equal_opportunity(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    Equal opportunity (relaxed equalized odds).
    
    Only TPR should be equal across groups (or equivalently FNR).
    
    Formula: P(Ŷ=1|Y=1,A=a) - P(Ŷ=1|Y=1,A=b)
    
    Returns:
        Difference in TPR (0 = perfect equality)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    return stats_a.tpr - stats_b.tpr


def predictive_parity(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> Dict[str, float]:
    """
    Predictive parity (outcome test, calibration).
    
    PPV and NPV should be equal across groups.
    
    Formula:
        PPV: P(Y=1|Ŷ=1,A=a) = P(Y=1|Ŷ=1,A=b)
        NPV: P(Y=0|Ŷ=0,A=a) = P(Y=0|Ŷ=0,A=b)
    
    Returns:
        Dict with ppv_diff and npv_diff
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    return {
        "ppv_diff": stats_a.ppv - stats_b.ppv,
        "npv_diff": stats_a.npv - stats_b.npv,
    }


def counterfactual_fairness(
    dataset: BinaryDataset,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    Counterfactual fairness.
    
    Predictions should be invariant to changes in sensitive attribute.
    Requires paired counterfactual data with pair_id.
    
    Formula: For paired individuals differing only in A,
        P(Ŷ_{A←a}=y|X=x,A=a) = P(Ŷ_{A←b}=y|X=x,A=a)
    
    Returns:
        Fraction of pairs with different predictions (0 = perfect CF fairness)
    """
    if dataset.pair_id is None:
        raise ValueError("Counterfactual fairness requires pair_id in dataset")
    
    # Group by pair_id
    unique_pairs = np.unique(dataset.pair_id)
    disagreement_count = 0
    
    for pair in unique_pairs:
        mask = dataset.pair_id == pair
        if np.sum(mask) != 2:
            continue  # Skip incomplete pairs
        
        preds = dataset.y_pred[mask]
        if preds[0] != preds[1]:
            disagreement_count += 1
    
    return disagreement_count / len(unique_pairs) if len(unique_pairs) > 0 else 0.0


def disparate_impact(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    Disparate impact (DI ratio, 80% rule).
    
    Ratio of favorable prediction rates between unprivileged and privileged groups.
    Fair if in range [0.8, 1.25]; perfect fairness at 1.0.
    
    Formula: DI = P(Ŷ=1|A=a) / P(Ŷ=1|A=b)
    
    Returns:
        Ratio (1.0 = perfect parity, <0.8 or >1.25 = potential discrimination)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    if stats_b.positive_rate == 0:
        return float('inf') if stats_a.positive_rate > 0 else 1.0
    
    return stats_a.positive_rate / stats_b.positive_rate


def predictive_equality(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    Predictive equality (FPR parity).
    
    False positive rates should be equal across groups.
    
    Formula: P(Ŷ=1|Y=0,A=a) - P(Ŷ=1|Y=0,A=b)
    
    Returns:
        Difference in FPR (0 = perfect equality)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    return stats_a.fpr - stats_b.fpr


def generalized_entropy_index(
    dataset: BinaryDataset,
    alpha: float = 1.0
) -> float:
    """
    Generalized entropy index (inequality measure).
    
    Measures inequality of benefits (correct predictions) across individuals.
    Special cases: α=0 (mean log deviation), α=1 (Theil index).
    
    Formula:
        GE(α) = 1/(n·α·(α-1)) · Σ[(y_i/μ)^α - 1]
        
    For α=0 (mean log deviation):
        GE(0) = -(1/n) · Σ ln(y_i/μ)
        
    For α=1 (Theil index):
        GE(1) = (1/n) · Σ (y_i/μ) · ln(y_i/μ)
    
    Args:
        dataset: BinaryDataset
        alpha: Inequality aversion parameter
        
    Returns:
        GE index (0 = perfect equality, higher = more inequality)
    """
    # Define benefit as 1 for correct prediction, 0 for incorrect
    correct = (dataset.y_true == dataset.y_pred).astype(float)
    correct = np.where(correct == 0, 1e-10, correct)  # Avoid log(0)
    
    mu = np.mean(correct)
    n = len(correct)
    
    if mu == 0:
        return 0.0
    
    ratios = correct / mu
    
    if alpha == 0:
        # Mean log deviation
        return -np.mean(np.log(ratios))
    elif alpha == 1:
        # Theil index
        return np.mean(ratios * np.log(ratios))
    else:
        # General case
        return np.mean(np.power(ratios, alpha) - 1) / (alpha * (alpha - 1))


def average_odds_difference(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    Average odds difference (AOD).
    
    Average of differences in FPR and TPR.
    
    Formula: AOD = 0.5 · [(FPR_a - FPR_b) + (TPR_a - TPR_b)]
    
    Returns:
        Average odds difference (0 = equalized odds)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    fpr_diff = stats_a.fpr - stats_b.fpr
    tpr_diff = stats_a.tpr - stats_b.tpr
    
    return 0.5 * (fpr_diff + tpr_diff)


def error_difference(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    Error difference (error rate parity).
    
    Difference in overall misclassification rates.
    
    Formula: P(Ŷ≠Y,A=a) - P(Ŷ≠Y,A=b)
    
    Returns:
        Difference in error rates (0 = equal error rates)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    return stats_a.error_rate - stats_b.error_rate


def error_ratio(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    Error ratio.
    
    Ratio of overall misclassification rates.
    
    Formula: P(Ŷ≠Y,A=a) / P(Ŷ≠Y,A=b)
    
    Returns:
        Ratio of error rates (1.0 = equal error rates)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    if stats_b.error_rate == 0:
        return float('inf') if stats_a.error_rate > 0 else 1.0
    
    return stats_a.error_rate / stats_b.error_rate


def false_discovery_rate_ratio(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    False discovery rate ratio (FDRR).
    
    Ratio of false discovery rates (FDR = 1 - PPV).
    
    Formula: P(Y=0|Ŷ=1,A=a) / P(Y=0|Ŷ=1,A=b)
    
    Returns:
        Ratio of FDR (1.0 = equal FDR)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    if stats_b.fdr == 0:
        return float('inf') if stats_a.fdr > 0 else 1.0
    
    return stats_a.fdr / stats_b.fdr


def false_negative_rate_ratio(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    False negative rate ratio (FNRR).
    
    Ratio of false negative rates (missed positives).
    
    Formula: P(Ŷ=0|Y=1,A=a) / P(Ŷ=0|Y=1,A=b)
    
    Returns:
        Ratio of FNR (1.0 = equal FNR)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    if stats_b.fnr == 0:
        return float('inf') if stats_a.fnr > 0 else 1.0
    
    return stats_a.fnr / stats_b.fnr


def false_omission_rate_ratio(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    False omission rate ratio (FORR).
    
    Ratio of false omission rates (FOR = 1 - NPV).
    
    Formula: P(Y=1|Ŷ=0,A=a) / P(Y=1|Ŷ=0,A=b)
    
    Returns:
        Ratio of FOR (1.0 = equal FOR)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    if stats_b.for_rate == 0:
        return float('inf') if stats_a.for_rate > 0 else 1.0
    
    return stats_a.for_rate / stats_b.for_rate


def false_positive_rate_ratio(
    dataset: BinaryDataset,
    group_a: str,
    group_b: str,
    sensitive_attr: str = "sensitive"
) -> float:
    """
    False positive rate ratio (FPRR).
    
    Ratio of false positive rates.
    
    Formula: P(Ŷ=1|Y=0,A=a) / P(Ŷ=1|Y=0,A=b)
    
    Returns:
        Ratio of FPR (1.0 = equal FPR)
    """
    stats_a = dataset.get_group_stats(sensitive_attr, group_a)
    stats_b = dataset.get_group_stats(sensitive_attr, group_b)
    
    if stats_b.fpr == 0:
        return float('inf') if stats_a.fpr > 0 else 1.0
    
    return stats_a.fpr / stats_b.fpr
