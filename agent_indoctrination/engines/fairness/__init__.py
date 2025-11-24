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
from .report import FairnessReport
from .engine import FairnessEngine

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
    "FairnessEngine",
]
