"""
Example: Using Objective Fairness Metrics

This example demonstrates how to use the 15 objective fairness metrics
to evaluate AI systems for algorithmic bias.
"""

import numpy as np
from agent_indoctrination.engines.fairness import (
    BinaryDataset,
    FairnessReport,
    FairnessThresholds,
)
from agent_indoctrination.engines.fairness.data_loaders import create_synthetic_fair_dataset


def main():
    """Run fairness evaluation example."""
    
    print("=" * 70)
    print("🎯 OBJECTIVE FAIRNESS METRICS - DEMO")
    print("=" * 70)
    print("\nThis demo evaluates a binary classifier for algorithmic fairness")
    print("using 15 research-backed metrics.\n")
    
    # Step 1: Create synthetic data with some bias
    print("📝 Step 1: Generating synthetic dataset with bias...")
    X, y_true, sensitive_attr = create_synthetic_fair_dataset(
        n_samples=1000,
        bias_factor=0.2  # Inject some bias
    )
    
    # Step 2: Simulate model predictions (with bias)
    print("🤖 Step 2: Generating biased model predictions...")
    # Simulate a model that's less accurate for group A=1
    rng = np.random.default_rng(42)
    y_pred = y_true.copy()
    
    # Introduce more errors for sensitive group A=1
    mask_group_1 = sensitive_attr == 1
    n_errors = int(np.sum(mask_group_1) * 0.15)  # 15% error rate for group 1
    error_indices = rng.choice(
        np.where(mask_group_1)[0], 
        size=n_errors, 
        replace=False
    )
    y_pred[error_indices] = 1 - y_pred[error_indices]  # Flip predictions
    
    # Fewer errors for group A=0
    mask_group_0 = sensitive_attr == 0
    n_errors = int(np.sum(mask_group_0) * 0.05)  # 5% error rate for group 0
    error_indices = rng.choice(
        np.where(mask_group_0)[0], 
        size=n_errors, 
        replace=False
    )
    y_pred[error_indices] = 1 - y_pred[error_indices]
    
    print(f"   - Total samples: {len(y_true)}")
    print(f"   - Group 0 samples: {np.sum(sensitive_attr == 0)}")
    print(f"   - Group 1 samples: {np.sum(sensitive_attr == 1)}")
    
    # Step 3: Create BinaryDataset
    print("\n📊 Step 3: Creating fairness dataset...")
    dataset = BinaryDataset(
        y_true=y_true,
        y_pred=y_pred,
        sensitive={"group": sensitive_attr},
    )
    
    # Step 4: Set fairness thresholds
    print("⚖️  Step 4: Configuring fairness thresholds...")
    thresholds = FairnessThresholds(
        demographic_parity_diff=0.1,
        disparate_impact_min=0.8,
        disparate_impact_max=1.25,
        average_odds_diff=0.05,
    )
    
    # Step 5: Generate fairness report
    print("\n📝 Step 5: Evaluating all 15 fairness metrics...\n")
    report = FairnessReport(
        dataset=dataset,
        group_a=1,  # Unprivileged group
        group_b=0,  # Privileged group
        sensitive_attr="group",
        thresholds=thresholds,
    )
    
    # Step 6: Display results
    print("=" * 70)
    print("📊 FAIRNESS EVALUATION RESULTS")
    print("=" * 70)
    
    print(f"\n✅ Overall Status: {'PASS' if report.overall_pass else 'FAIL'}\n")
    
    # Key metrics
    metrics = report.metric_results
    print("🔍 Key Fairness Metrics:")
    print(f"   • Demographic Parity Difference: {metrics['demographic_parity']:.4f}")
    print(f"   • Disparate Impact Ratio: {metrics['disparate_impact']:.4f}")
    print(f"     (Should be in [0.8, 1.25] - '80% rule')")
    print(f"   • Equal Opportunity Diff: {metrics['equal_opportunity']:.4f}")
    print(f"   • Average Odds Difference: {metrics['average_odds_difference']:.4f}")
    print(f"   • Error Difference: {metrics['error_difference']:.4f}")
    print(f"   • Error Ratio: {metrics['error_ratio']:.4f}")
    print(f"   • Generalized Entropy (Theil): {metrics['generalized_entropy_index']:.4f}")
    
    # Group statistics
    print("\n📈 Per-Group Statistics:")
    stats = report.group_stats
    
    print(f"\n   Group 1 (Unprivileged):")
    print(f"      Samples: {stats[1]['n']}")
    print(f"      True Positive Rate (TPR): {stats[1]['tpr']:.4f}")
    print(f"      False Positive Rate (FPR): {stats[1]['fpr']:.4f}")
    print(f"      Positive Prediction Rate: {stats[1]['positive_rate']:.4f}")
    print(f"      Error Rate: {stats[1]['error_rate']:.4f}")
    
    print(f"\n   Group 0 (Privileged):")
    print(f"      Samples: {stats[0]['n']}")
    print(f"      True Positive Rate (TPR): {stats[0]['tpr']:.4f}")
    print(f"      False Positive Rate (FPR): {stats[0]['fpr']:.4f}")
    print(f"      Positive Prediction Rate: {stats[0]['positive_rate']:.4f}")
    print(f"      Error Rate: {stats[0]['error_rate']:.4f}")
    
    # Pass/fail summary
    print("\n❗ Pass/Fail Summary:")
    for metric_name, passed in report.pass_fail.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {metric_name:.<40} {status}")
    
    # Step 7: Export reports
    print("\n\n📝 Step 7: Exporting reports...")
    
    # Save markdown report
    with open("fairness_report.md", "w") as f:
        f.write(report.to_markdown())
    print("   ✅ Saved: fairness_report.md")
    
    # Save JSON report
    with open("fairness_report.json", "w") as f:
        f.write(report.to_json())
    print("   ✅ Saved: fairness_report.json")
    
    # Save HTML report
    with open("fairness_report.html", "w") as f:
        f.write(report.to_html())
    print("   ✅ Saved: fairness_report.html")
    
    print("\n" + "=" * 70)
    print("🎉 DEMO COMPLETE!")
    print("=" * 70)
    print("\n💡 Next Steps:")
    print("   - Review the generated reports (fairness_report.md/json/html)")
    print("   - Try with real datasets: load_adult(), load_compas(), load_german_credit()")
    print("   - Adjust thresholds for your use case")
    print("   - Integrate into CI/CD pipeline")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
