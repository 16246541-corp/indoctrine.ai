"""
Fairness Metrics Engine for Indoctrine AI.

Implements 15 objective fairness metrics for binary classification decisions,
following the systematic literature review:
"Objective metrics for ethical AI: a systematic literature review."

This module provides:
- Core data model for fairness evaluation (BinaryDataset)
- 15 fairness metrics (demographic parity, equalized odds, etc.)
- Standard benchmark dataset loaders (Adult, COMPAS, German Credit)
- LLM/agent integration for fairness testing
- Comprehensive fairness reports
"""

from typing import List, Any, Optional
import numpy as np
from .dataset import BinaryDataset
from .metrics import (
    demographic_parity,
    equalized_odds,
    equal_opportunity,
    predictive_parity,
    counterfactual_fairness,
    disparate_impact,
    predictive_equality,
    generalized_entropy_index,
    average_odds_difference,
    error_difference,
    error_ratio,
    false_discovery_rate_ratio,
    false_negative_rate_ratio,
    false_omission_rate_ratio,
    false_positive_rate_ratio,
)
from .report import FairnessReport, FairnessThresholds
from .engine import FairnessEngine
from .llm_testing import PromptFairnessTest, test_llm_fairness

def get_thresholds_for_use_case(use_case: str) -> FairnessThresholds:
    """Get appropriate thresholds for different domains."""
    presets = {
        "hiring": FairnessThresholds(
            demographic_parity_diff=0.05,  # Stricter
            disparate_impact_min=0.8,
            average_odds_diff=0.03,
        ),
        "lending": FairnessThresholds(
            demographic_parity_diff=0.05,
            disparate_impact_min=0.8,
        ),
        "content_moderation": FairnessThresholds(
            demographic_parity_diff=0.1,  # More lenient
            average_odds_diff=0.1,
        ),
        "general": FairnessThresholds(),  # Default
    }
    return presets.get(use_case, presets["general"])

def quick_fairness_check(
    y_true: List[int],
    y_pred: List[int],
    sensitive_values: List[Any],
    sensitive_name: str = "sensitive_attribute",
    use_case: str = "general",
    auto_detect_groups: bool = True,
) -> FairnessReport:
    """
    One-function fairness check with smart defaults.
    
    Args:
        y_true: Ground truth labels (0 or 1)
        y_pred: Predicted labels (0 or 1)
        sensitive_values: List of sensitive attribute values (e.g. ["Male", "Female", ...])
        sensitive_name: Name of the sensitive attribute
        use_case: Domain context ("hiring", "lending", "content_moderation", "general")
        auto_detect_groups: If True, automatically selects privileged/unprivileged groups
                            based on positive outcome rates.
    
    Returns:
        FairnessReport object.
    
    Example:
        >>> report = quick_fairness_check(
        ...     y_true=labels,
        ...     y_pred=predictions,
        ...     sensitive_values=demographics,
        ...     use_case="hiring"
        ... )
        >>> print(report.to_markdown())
    """
    dataset = BinaryDataset(
        y_true=y_true,
        y_pred=y_pred,
        sensitive={sensitive_name: sensitive_values}
    )
    
    # Auto-detect privileged/unprivileged based on positive rate
    groups = np.unique(sensitive_values)
    if len(groups) < 2:
        raise ValueError(f"Need at least 2 groups for fairness check, found {len(groups)}: {groups}")
    
    # Simple heuristic: compare first two groups if more than 2
    # Ideally we'd let user specify, but this is "quick" check
    g1, g2 = groups[0], groups[1]
    
    stats_1 = dataset.get_group_stats(sensitive_name, g1)
    stats_2 = dataset.get_group_stats(sensitive_name, g2)
    
    # Lower positive rate = unprivileged (usually)
    if stats_1.positive_rate < stats_2.positive_rate:
        group_a, group_b = g1, g2
    else:
        group_a, group_b = g2, g1
    
    # Use-case-specific thresholds
    thresholds = get_thresholds_for_use_case(use_case)
    
    return FairnessReport(
        dataset,
        str(group_a),
        str(group_b),
        sensitive_name,
        thresholds=thresholds,
        use_case=use_case
    )

__all__ = [
    "BinaryDataset",
    "demographic_parity",
    "equalized_odds",
    "equal_opportunity",
    "predictive_parity",
    "counterfactual_fairness",
    "disparate_impact",
    "predictive_equality",
    "generalized_entropy_index",
    "average_odds_difference",
    "error_difference",
    "error_ratio",
    "false_discovery_rate_ratio",
    "false_negative_rate_ratio",
    "false_omission_rate_ratio",
    "false_positive_rate_ratio",
    "FairnessReport",
    "FairnessThresholds",
    "FairnessEngine",
    "quick_fairness_check",
    "get_thresholds_for_use_case",
    "PromptFairnessTest",
    "test_llm_fairness",
]
