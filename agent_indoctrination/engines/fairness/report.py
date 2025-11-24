"""
Fairness report generation.

Provides comprehensive fairness evaluation reports with all 15 metrics,
group statistics, and pass/fail indicators based on thresholds.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json
from .dataset import BinaryDataset
from . import metrics


@dataclass
class FairnessThresholds:
    """Thresholds for pass/fail determination."""
    
    # Difference-based metrics (absolute value should be < threshold)
    demographic_parity_diff: float = 0.1
    equal_opportunity_diff: float = 0.1
    average_odds_diff: float = 0.05
    predictive_equality_diff: float = 0.1
    error_diff: float = 0.05
    
    # Ratio-based metrics (should be in [1-threshold, 1+threshold])
    disparate_impact_min: float = 0.8
    disparate_impact_max: float = 1.25
    error_ratio_min: float = 0.9
    error_ratio_max: float = 1.11
    rate_ratio_min: float = 0.8
    rate_ratio_max: float = 1.25
    
    # Entropy-based
    generalized_entropy_max: float = 0.1
    
    # Counterfactual
    counterfactual_max: float = 0.05


class FairnessReport:
    """
    Comprehensive fairness evaluation report.
    
    Computes all 15 fairness metrics and provides structured output
    with pass/fail indicators, group statistics, and export methods.
    """
    
    def __init__(
        self,
        dataset: BinaryDataset,
        group_a: str,
        group_b: str,
        sensitive_attr: str = "sensitive",
        thresholds: Optional[FairnessThresholds] = None,
        use_case: str = "general",
    ):
        """
        Initialize fairness report.
        
        Args:
            dataset: BinaryDataset with predictions and sensitive attributes
            group_a: Unprivileged group value
            group_b: Privileged group value
            sensitive_attr: Name of sensitive attribute
            thresholds: Optional thresholds for pass/fail
            use_case: Domain context (hiring, lending, etc.) for interpretations
        """
        self.dataset = dataset
        self.group_a = group_a
        self.group_b = group_b
        self.sensitive_attr = sensitive_attr
        self.thresholds = thresholds or FairnessThresholds()
        self.use_case = use_case
        
        # Check data quality
        self.data_quality_issues = self.dataset.check_data_quality()
        
        # Compute all metrics
        self.metric_results = self._compute_all_metrics()
        self.group_stats = self._get_group_statistics()
        self.pass_fail = self._evaluate_pass_fail()
        
        # Initialize interpreter
        from .interpreter import MetricInterpreter
        self.interpreter = MetricInterpreter(use_case=use_case)
        self.interpretations = self.interpreter.interpret_all_metrics(
            self.metric_results,
            group_a=str(group_a),
            group_b=str(group_b)
        )
    
    # ... (methods _compute_all_metrics, _get_group_statistics, _evaluate_pass_fail remain unchanged) ...

    def _compute_all_metrics(self) -> Dict:
        """Compute all 15 fairness metrics."""
        ds = self.dataset
        a, b = self.group_a, self.group_b
        attr = self.sensitive_attr
        
        results = {
            "demographic_parity": metrics.demographic_parity(ds, a, b, attr),
            "equalized_odds": metrics.equalized_odds(ds, a, b, attr),
            "equal_opportunity": metrics.equal_opportunity(ds, a, b, attr),
            "predictive_parity": metrics.predictive_parity(ds, a, b, attr),
            "disparate_impact": metrics.disparate_impact(ds, a, b, attr),
            "predictive_equality": metrics.predictive_equality(ds, a, b, attr),
            "generalized_entropy_index": metrics.generalized_entropy_index(ds, alpha=1.0),
            "average_odds_difference": metrics.average_odds_difference(ds, a, b, attr),
            "error_difference": metrics.error_difference(ds, a, b, attr),
            "error_ratio": metrics.error_ratio(ds, a, b, attr),
            "false_discovery_rate_ratio": metrics.false_discovery_rate_ratio(ds, a, b, attr),
            "false_negative_rate_ratio": metrics.false_negative_rate_ratio(ds, a, b, attr),
            "false_omission_rate_ratio": metrics.false_omission_rate_ratio(ds, a, b, attr),
            "false_positive_rate_ratio": metrics.false_positive_rate_ratio(ds, a, b, attr),
        }
        
        # Add counterfactual if pair_id available
        if ds.pair_id is not None:
            results["counterfactual_fairness"] = metrics.counterfactual_fairness(ds, attr)
        
        return results
    
    def _get_group_statistics(self) -> Dict:
        """Get detailed confusion matrix statistics per group."""
        stats_a = self.dataset.get_group_stats(self.sensitive_attr, self.group_a)
        stats_b = self.dataset.get_group_stats(self.sensitive_attr, self.group_b)
        
        return {
            self.group_a: {
                "n": stats_a.n,
                "tp": stats_a.tp,
                "fp": stats_a.fp,
                "tn": stats_a.tn,
                "fn": stats_a.fn,
                "tpr": stats_a.tpr,
                "fpr": stats_a.fpr,
                "tnr": stats_a.tnr,
                "fnr": stats_a.fnr,
                "ppv": stats_a.ppv,
                "npv": stats_a.npv,
                "positive_rate": stats_a.positive_rate,
                "error_rate": stats_a.error_rate,
            },
            self.group_b: {
                "n": stats_b.n,
                "tp": stats_b.tp,
                "fp": stats_b.fp,
                "tn": stats_b.tn,
                "fn": stats_b.fn,
                "tpr": stats_b.tpr,
                "fpr": stats_b.fpr,
                "tnr": stats_b.tnr,
                "fnr": stats_b.fnr,
                "ppv": stats_b.ppv,
                "npv": stats_b.npv,
                "positive_rate": stats_b.positive_rate,
                "error_rate": stats_b.error_rate,
            }
        }
    
    def _evaluate_pass_fail(self) -> Dict[str, bool]:
        """Evaluate pass/fail for each metric based on thresholds."""
        r = self.metric_results
        t = self.thresholds
        
        pass_fail = {
            "demographic_parity": abs(r["demographic_parity"]) < t.demographic_parity_diff,
            "equal_opportunity": abs(r["equal_opportunity"]) < t.equal_opportunity_diff,
            "average_odds_difference": abs(r["average_odds_difference"]) < t.average_odds_diff,
            "predictive_equality": abs(r["predictive_equality"]) < t.predictive_equality_diff,
            "error_difference": abs(r["error_difference"]) < t.error_diff,
            "disparate_impact": t.disparate_impact_min <= r["disparate_impact"] <= t.disparate_impact_max,
            "error_ratio": t.error_ratio_min <= r["error_ratio"] <= t.error_ratio_max,
            "false_discovery_rate_ratio": t.rate_ratio_min <= r["false_discovery_rate_ratio"] <= t.rate_ratio_max,
            "false_negative_rate_ratio": t.rate_ratio_min <= r["false_negative_rate_ratio"] <= t.rate_ratio_max,
            "false_omission_rate_ratio": t.rate_ratio_min <= r["false_omission_rate_ratio"] <= t.rate_ratio_max,
            "false_positive_rate_ratio": t.rate_ratio_min <= r["false_positive_rate_ratio"] <= t.rate_ratio_max,
            "generalized_entropy_index": r["generalized_entropy_index"] < t.generalized_entropy_max,
        }
        
        if "counterfactual_fairness" in r:
            pass_fail["counterfactual_fairness"] = r["counterfactual_fairness"] < t.counterfactual_max
        
        return pass_fail
    
    @property
    def overall_pass(self) -> bool:
        """Whether all metrics pass thresholds."""
        return all(self.pass_fail.values())
    
    def to_dict(self) -> Dict:
        """Export as dictionary."""
        # Convert interpretations to dicts
        interp_dict = {
            k: v.to_dict() for k, v in self.interpretations.items()
        }
        
        return {
            "groups": {
                "group_a": str(self.group_a),
                "group_b": str(self.group_b),
                "sensitive_attr": self.sensitive_attr,
            },
            "metrics": self.metric_results,
            "group_statistics": self.group_stats,
            "pass_fail": self.pass_fail,
            "overall_pass": self.overall_pass,
            "interpretations": interp_dict,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Export as JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    def to_markdown(self) -> str:
        """Export as Markdown report with interpretations."""
        md = []
        md.append(f"# Fairness Evaluation Report\n")
        md.append(f"**Comparison**: `{self.group_a}` (unprivileged) vs `{self.group_b}` (privileged)\n")
        md.append(f"**Sensitive Attribute**: {self.sensitive_attr}\n")
        md.append(f"**Overall Result**: {'✅ PASS' if self.overall_pass else '❌ FAIL'}\n")
        
        # Data Quality Warnings
        if self.data_quality_issues["errors"] or self.data_quality_issues["warnings"]:
            md.append("\n## ⚠️ Data Quality Issues\n")
            for error in self.data_quality_issues["errors"]:
                md.append(f"- 🔴 **ERROR**: {error}\n")
            for warning in self.data_quality_issues["warnings"]:
                md.append(f"- 🟠 **WARNING**: {warning}\n")
        
        # Executive Summary / Top Concerns
        top_concerns = self.interpreter.get_top_concerns(self.interpretations, n=3)
        if top_concerns:
            md.append("\n## 🚨 Top Fairness Concerns\n")
            for concern in top_concerns:
                icon = self._get_severity_icon(concern.severity)
                md.append(f"### {icon} {concern.metric_name} ({concern.severity.value.upper()})\n")
                md.append(f"**Value**: {concern.value:.4f}\n")
                md.append(f"> {concern.plain_english}\n")
                if concern.legal_implications:
                    md.append(f"**Legal Risk**: {concern.legal_implications}\n")
                if concern.recommended_actions:
                    md.append("**Recommended Actions**:")
                    for action in concern.recommended_actions:
                        md.append(f"- {action}")
                md.append("\n")

        # Group statistics
        md.append("\n## Group Statistics\n")
        md.append("| Metric | " + str(self.group_a) + " | " + str(self.group_b) + " |")
        md.append("|--------|" + "-" * len(str(self.group_a)) + "|" + "-" * len(str(self.group_b)) + "|")
        
        stats_a = self.group_stats[self.group_a]
        stats_b = self.group_stats[self.group_b]
        
        for key in ["n", "tp", "fp", "tn", "fn"]:
            md.append(f"| {key.upper()} | {stats_a[key]} | {stats_b[key]} |")
        
        md.append("| **Rates** | | |")
        for key in ["tpr", "fpr", "tnr", "fnr", "ppv", "npv", "positive_rate", "error_rate"]:
            md.append(f"| {key.upper()} | {stats_a[key]:.4f} | {stats_b[key]:.4f} |")
        
        # Fairness metrics table
        md.append("\n## Fairness Metrics Detail\n")
        md.append("| Metric | Value | Status | Severity |")
        md.append("|--------|-------|--------|----------|")
        
        for key, value in self.metric_results.items():
            status = "✅ PASS" if self.pass_fail.get(key, False) else "❌ FAIL"
            
            # Get severity if available
            severity = "-"
            if key in self.interpretations:
                sev = self.interpretations[key].severity
                severity = f"{self._get_severity_icon(sev)} {sev.value.upper()}"
            
            if isinstance(value, dict):
                # Handle multi-value metrics like equalized_odds
                for sub_key, sub_value in value.items():
                    md.append(f"| {key}.{sub_key} | {sub_value:.4f} | - | - |")
            else:
                md.append(f"| {key} | {value:.4f} | {status} | {severity} |")
        
        # Detailed Interpretations
        md.append("\n## 📖 Detailed Interpretations\n")
        for key, interp in self.interpretations.items():
            md.append(f"### {interp.metric_name}\n")
            md.append(f"**Value**: {interp.value:.4f}\n")
            md.append(f"**Explanation**: {interp.plain_english}\n")
            md.append(f"**Impact**: {interp.impact_explanation}\n")
            if interp.learn_more_url:
                md.append(f"[Learn more]({interp.learn_more_url})\n")
            md.append("\n")
            
        return "\n".join(md)
    
    def to_html(self) -> str:
        """Export as HTML report."""
        # Convert markdown to basic HTML
        md = self.to_markdown()
        # Basic markdown to HTML conversion (simplified)
        html = md.replace("# ", "<h1>").replace("</h1>\n", "</h1>\n")
        html = html.replace("## ", "<h2>").replace("</h2>\n", "</h2>\n")
        html = html.replace("### ", "<h3>").replace("</h3>\n", "</h3>\n")
        html = html.replace("**", "<strong>").replace("</strong>", "</strong>")
        html = html.replace("`", "<code>").replace("</code>", "</code>")
        html = html.replace("> ", "<blockquote>").replace("\n\n", "<br><br>")
        
        # Convert tables
        lines = html.split("\n")
        in_table = False
        result = []
        
        result.append("""
        <style>
            body { font-family: system-ui, -apple-system, sans-serif; line-height: 1.5; max_width: 800px; margin: 0 auto; padding: 20px; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            blockquote { border-left: 4px solid #ccc; margin: 0; padding-left: 16px; color: #555; }
            h1 { border-bottom: 2px solid #eee; padding-bottom: 10px; }
            h2 { margin-top: 30px; border-bottom: 1px solid #eee; }
        </style>
        """)
        
        for line in lines:
            if line.startswith("|"):
                if not in_table:
                    result.append("<table>")
                    in_table = True
                
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if all(c.startswith("-") for c in cells):
                    continue  # Skip separator rows
                
                tag = "th" if "Metric" in line or "**" in line else "td"
                row = "<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>"
                result.append(row)
            else:
                if in_table:
                    result.append("</table>")
                    in_table = False
                result.append(line)
        
        if in_table:
            result.append("</table>")
        
        return "\n".join(result)

    def _get_severity_icon(self, severity) -> str:
        """Get emoji icon for severity level."""
        # Handle string or enum
        sev_str = severity if isinstance(severity, str) else severity.value
        icons = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }
        return icons.get(sev_str, "⚪")
