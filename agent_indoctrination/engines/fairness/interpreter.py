"""
Interpretability layer for fairness metrics.

Provides human-readable explanations, severity scoring, and remediation
guidance for fairness metric values.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Severity levels for fairness violations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MetricInterpretation:
    """Human-readable interpretation of a fairness metric."""
    
    metric_name: str
    value: float
    severity: Severity
    plain_english: str
    impact_explanation: str
    legal_implications: Optional[str] = None
    recommended_actions: Optional[List[str]] = None
    learn_more_url: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "metric_name": self.metric_name,
            "value": self.value,
            "severity": self.severity.value,
            "plain_english": self.plain_english,
            "impact_explanation": self.impact_explanation,
            "legal_implications": self.legal_implications,
            "recommended_actions": self.recommended_actions,
            "learn_more_url": self.learn_more_url,
        }


class MetricInterpreter:
    """
    Interprets fairness metric values into actionable insights.
    
    Provides:
    - Plain-English explanations
    - Severity scoring
    - Use-case-specific guidance
    - Legal implications
    - Remediation recommendations
    """
    
    def __init__(self, use_case: str = "general"):
        """
        Initialize interpreter.
        
        Args:
            use_case: Domain context (hiring, lending, healthcare, etc.)
        """
        self.use_case = use_case
    
    def interpret_disparate_impact(
        self, 
        value: float,
        group_a: str = "unprivileged",
        group_b: str = "privileged"
    ) -> MetricInterpretation:
        """
        Interpret disparate impact ratio.
        
        Args:
            value: Disparate impact ratio (ideal = 1.0)
            group_a: Unprivileged group name
            group_b: Privileged group name
        """
        # Determine severity
        if 0.9 <= value <= 1.1:
            severity = Severity.LOW
        elif 0.8 <= value < 0.9 or 1.1 < value <= 1.25:
            severity = Severity.MEDIUM
        elif 0.7 <= value < 0.8 or 1.25 < value <= 1.4:
            severity = Severity.HIGH
        else:
            severity = Severity.CRITICAL
        
        # Generate plain English explanation
        if value < 1.0:
            percentage_diff = (1 - value) * 100
            plain_english = (
                f"{group_a.capitalize()} group is {percentage_diff:.0f}% less likely "
                f"to receive positive outcomes than {group_b} group."
            )
        elif value > 1.0:
            percentage_diff = (value - 1) * 100
            plain_english = (
                f"{group_a.capitalize()} group is {percentage_diff:.0f}% more likely "
                f"to receive positive outcomes than {group_b} group."
            )
        else:
            plain_english = "Both groups receive positive outcomes at equal rates."
        
        # Impact explanation
        if abs(value - 1.0) < 0.1:
            impact = "✅ Minimal disparity. Model treats groups fairly in terms of overall positive rate."
        elif value < 0.8:
            impact = (
                f"⚠️ Significant disparity detected. In a real-world scenario with 100 qualified "
                f"{group_a} individuals and 100 qualified {group_b} individuals, approximately "
                f"{int(value * 100)} {group_a} would receive positive outcomes while all 100 "
                f"{group_b} would receive them."
            )
        elif value > 1.25:
            impact = (
                f"⚠️ Significant reverse disparity. {group_a.capitalize()} group is favored "
                f"over {group_b} group."
            )
        else:
            impact = "⚠️ Moderate disparity. Consider reviewing if this is justified."
        
        # Legal implications
        legal = None
        if value < 0.8 or value > 1.25:
            legal = (
                "🚨 LEGAL RISK: This violates the '80% rule' (also known as the four-fifths rule) "
                "used by the U.S. Equal Employment Opportunity Commission (EEOC) in disparate "
                "impact cases. Ratios below 0.8 or above 1.25 may expose your organization to "
                "discrimination lawsuits under Title VII of the Civil Rights Act."
            )
        
        # Recommendations
        recommendations = []
        if severity in [Severity.HIGH, Severity.CRITICAL]:
            recommendations = [
                "📊 Audit training data for demographic representation and label bias",
                "🔍 Check if features inadvertently act as proxies for sensitive attributes",
                "⚙️ Consider fairness interventions (reweighting, threshold optimization, or adversarial debiasing)",
                "👥 Conduct bias audit with diverse stakeholders",
                "⚖️ Consult legal/compliance team before deployment",
            ]
        elif severity == Severity.MEDIUM:
            recommendations = [
                "📊 Review training data quality and representation",
                "🔍 Investigate if disparity is due to genuine group differences or bias",
                "📈 Monitor metric over time and with additional data",
            ]
        
        return MetricInterpretation(
            metric_name="Disparate Impact",
            value=value,
            severity=severity,
            plain_english=plain_english,
            impact_explanation=impact,
            legal_implications=legal,
            recommended_actions=recommendations,
            learn_more_url="https://en.wikipedia.org/wiki/Disparate_impact#The_80%_rule"
        )
    
    def interpret_demographic_parity(
        self,
        value: float,
        group_a: str = "unprivileged",
        group_b: str = "privileged"
    ) -> MetricInterpretation:
        """Interpret demographic parity difference."""
        severity = self._classify_difference_severity(value, [0.05, 0.1, 0.2])
        
        percentage_diff = abs(value) * 100
        
        if value < 0:
            plain_english = (
                f"{group_a.capitalize()} group receives positive outcomes "
                f"{percentage_diff:.1f} percentage points less often than {group_b} group."
            )
        elif value > 0:
            plain_english = (
                f"{group_a.capitalize()} group receives positive outcomes "
                f"{percentage_diff:.1f} percentage points more often than {group_b} group."
            )
        else:
            plain_english = "Both groups receive positive outcomes at equal rates."
        
        # Use-case specific impact
        impact_templates = {
            "hiring": f"In a hiring scenario, this means for every 100 applicants from each group with identical qualifications, {abs(value)*100:.0f} fewer {group_a if value < 0 else group_b} candidates would be recommended.",
            "lending": f"In lending, this translates to {percentage_diff:.1f}% difference in loan approval rates between groups.",
            "healthcare": f"In healthcare triage, this represents {percentage_diff:.1f}% difference in patients being flagged for intervention.",
            "general": f"This represents a {percentage_diff:.1f} percentage point gap in positive outcome rates."
        }
        
        impact = impact_templates.get(self.use_case, impact_templates["general"])
        
        recommendations = None
        if severity in [Severity.HIGH, Severity.CRITICAL]:
            recommendations = [
                "Consider if outcome difference is justified by legitimate factors",
                "Review if protected attributes or their proxies influence predictions",
                "Implement fairness constraints during model training",
                "Use threshold optimization to balance group outcome rates",
            ]
        
        return MetricInterpretation(
            metric_name="Demographic Parity Difference",
            value=value,
            severity=severity,
            plain_english=plain_english,
            impact_explanation=impact,
            recommended_actions=recommendations,
            learn_more_url="https://fairmlbook.org/demographic.html"
        )
    
    def interpret_error_ratio(
        self,
        value: float,
        group_a: str = "unprivileged",
        group_b: str = "privileged"
    ) -> MetricInterpretation:
        """Interpret error ratio."""
        if 0.9 <= value <= 1.1:
            severity = Severity.LOW
        elif 0.8 <= value < 0.9 or 1.1 < value <= 1.3:
            severity = Severity.MEDIUM
        elif 0.6 <= value < 0.8 or 1.3 < value <= 2.0:
            severity = Severity.HIGH
        else:
            severity = Severity.CRITICAL
        
        if value > 1:
            times_higher = value
            plain_english = (
                f"{group_a.capitalize()} group experiences {times_higher:.1f}x higher "
                f"error rate than {group_b} group."
            )
        else:
            times_higher = 1 / value
            plain_english = (
                f"{group_b.capitalize()} group experiences {times_higher:.1f}x higher "
                f"error rate than {group_a} group."
            )
        
        impact = (
            "⚠️ Unequal error rates mean the model is less accurate for one group. "
            "This can lead to discriminatory outcomes even if overall positive rates are similar."
        )
        
        legal = None
        if severity == Severity.CRITICAL:
            legal = (
                "🚨 CRITICAL: Extreme accuracy disparity may constitute discrimination, "
                "especially in high-stakes domains (hiring, lending, criminal justice)."
            )
        
        recommendations = [
            "Ensure balanced representation in training data",
            "Check if different groups require different feature sets",
            "Consider group-specific calibration or ensemble models",
            "Evaluate if quality of training labels differs between groups",
        ]
        
        return MetricInterpretation(
            metric_name="Error Ratio",
            value=value,
            severity=severity,
            plain_english=plain_english,
            impact_explanation=impact,
            legal_implications=legal,
            recommended_actions=recommendations,
        )
    
    def interpret_all_metrics(
        self,
        metric_results: Dict[str, float],
        group_a: str = "unprivileged",
        group_b: str = "privileged"
    ) -> Dict[str, MetricInterpretation]:
        """
        Interpret all metrics in a fairness report.
        
        Args:
            metric_results: Dictionary of metric names to values
            group_a: Unprivileged group name
            group_b: Privileged group name
            
        Returns:
            Dictionary of metric names to interpretations
        """
        interpretations = {}
        
        # Map metric names to interpretation methods
        if "disparate_impact" in metric_results:
            interpretations["disparate_impact"] = self.interpret_disparate_impact(
                metric_results["disparate_impact"], group_a, group_b
            )
        
        if "demographic_parity" in metric_results:
            interpretations["demographic_parity"] = self.interpret_demographic_parity(
                metric_results["demographic_parity"], group_a, group_b
            )
        
        if "error_ratio" in metric_results:
            interpretations["error_ratio"] = self.interpret_error_ratio(
                metric_results["error_ratio"], group_a, group_b
            )
        
        # Add more metric interpretations as needed
        
        return interpretations
    
    def get_top_concerns(
        self,
        interpretations: Dict[str, MetricInterpretation],
        n: int = 3
    ) -> List[MetricInterpretation]:
        """
        Get the N most severe fairness concerns.
        
        Args:
            interpretations: Dictionary of metric interpretations
            n: Number of top concerns to return
            
        Returns:
            List of top N interpretations sorted by severity
        """
        severity_order = {
            Severity.CRITICAL: 4,
            Severity.HIGH: 3,
            Severity.MEDIUM: 2,
            Severity.LOW: 1,
        }
        
        sorted_interpretations = sorted(
            interpretations.values(),
            key=lambda x: (severity_order[x.severity], abs(x.value - 1.0)),
            reverse=True
        )
        
        return sorted_interpretations[:n]
    
    @staticmethod
    def _classify_difference_severity(value: float, thresholds: List[float]) -> Severity:
        """Classify severity for difference-based metrics."""
        abs_val = abs(value)
        
        if abs_val < thresholds[0]:
            return Severity.LOW
        elif abs_val < thresholds[1]:
            return Severity.MEDIUM
        elif abs_val < thresholds[2]:
            return Severity.HIGH
        else:
            return Severity.CRITICAL
