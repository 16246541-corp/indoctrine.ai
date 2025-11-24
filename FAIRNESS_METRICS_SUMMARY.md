# Objective Fairness Metrics Layer - Implementation Summary

## Overview

Added a comprehensive **Objective Fairness Metrics** layer to the Indoctrine AI framework, implementing 15 research-backed fairness metrics for evaluating algorithmic bias in AI systems.

## What Was Implemented

### 1. Core Data Model (`dataset.py`)
- **BinaryDataset** class for fairness evaluation
- Efficient caching of per-group confusion matrix statistics
- Support for multiple sensitive attributes
- Automatic computation of TPR, FPR, TNR, FNR, PPV, NPV, FDR, FOR
- Optional support for sample weights and counterfactual pairs

### 2. The 15 Fairness Metrics (`metrics.py`)

All metrics follow formal definitions from "Objective metrics for ethical AI" research paper:

#### Group Fairness Metrics
1. **Demographic Parity** - Equal positive rates across groups
2. **Equalized Odds** - Equal TPR and FPR across groups
3. **Equal Opportunity** - Equal TPR across groups (relaxed equalized odds)
4. **Predictive Parity** - Equal PPV and NPV across groups
5. **Predictive Equality** - Equal FPR across groups

#### Individual Fairness
6. **Counterfactual Fairness** - Predictions invariant to sensitive attribute changes

#### Disparity Ratios
7. **Disparate Impact** - Ratio of positive rates (80% rule)
8. **Error Ratio** - Ratio of error rates
9. **False Positive Rate Ratio (FPRR)**
10. **False Negative Rate Ratio (FNRR)**
11. **False Discovery Rate Ratio (FDRR)**
12. **False Omission Rate Ratio (FORR)**

#### Inequality Measures
13. **Generalized Entropy Index** - Population-level inequality (includes Theil index)
14. **Average Odds Difference** - Average of FPR and TPR differences
15. **Error Difference** - Difference in error rates

### 3. Fairness Report (`report.py`)
- **FairnessReport** class that computes all 15 metrics
- Configurable thresholds for pass/fail determination
- Export to JSON, Markdown, and HTML formats
- Detailed per-group statistics
- Overall fairness assessment

### 4. Fairness Engine (`engine.py`)
- **FairnessEngine** for integration with Indoctrine framework
- Agent/LLM evaluation on binary classification tasks
- Automatic group detection
- Batch evaluation support

### 5. Standard Dataset Loaders (`data_loaders.py`)
Loaders for the three most widely-used fairness benchmarks:

1. **Adult Income (UCI Census Income)**
   - ~48,000 samples
   - Predict income >$50K
   - Sensitive: sex, race, age

2. **COMPAS (ProPublica Recidivism)**
   - ~7,000 samples
   - Predict two-year recidivism
   - Sensitive: race, sex, age

3. **German Credit (UCI)**
   - 1,000 samples
   - Predict credit risk
   - Sensitive: sex, age

Plus a synthetic dataset generator for testing.

### 6. Documentation & Examples
- Updated README.md with comprehensive fairness metrics section
- Added detailed usage examples
- Created `examples/fairness_demo.py` demonstrating all metrics
- Documented thresholds and CI/CD integration

## Architecture

```
agent_indoctrination/
└─ engines/
   └─ fairness/
      ├─ __init__.py         # Module entry point
      ├─ dataset.py          # BinaryDataset & GroupStats
      ├─ metrics.py          # All 15 fairness metrics
      ├─ report.py           # FairnessReport & thresholds
      ├─ engine.py           # FairnessEngine integration
      └─ data_loaders.py     # Adult, COMPAS, German Credit
```

## Usage

### Basic Evaluation
```python
from agent_indoctrination.engines.fairness import BinaryDataset, FairnessReport

dataset = BinaryDataset(
    y_true=y_true,
    y_pred=y_pred,
    sensitive={"sex": sex_values}
)

report = FairnessReport(
    dataset=dataset,
    group_a="Female",
    group_b="Male",
    sensitive_attr="sex"
)

print(report.to_markdown())
print(f"Overall Pass: {report.overall_pass}")
```

### With Standard Benchmarks
```python
from agent_indoctrination.engines.fairness.data_loaders import load_adult

X, y_true, sensitive = load_adult(data_path="adult.data", sensitive="sex")
y_pred = my_model.predict(X)

dataset = BinaryDataset(y_true=y_true, y_pred=y_pred, sensitive={"sex": sensitive})
# ... evaluate
```

### LLM/Agent Evaluation
```python
from agent_indoctrination.engines.fairness.engine import FairnessEngine

engine = FairnessEngine()
results = engine.evaluate_agent_binary_task(
    agent_callable=my_agent,
    prompts=test_prompts,
    ground_truth=true_labels,
    sensitive_values=sensitive_attrs,
    label_fn=extract_binary_decision,
)
```

## Key Features

✅ **Model-Agnostic**: Works with any binary classifier, LLM, or agent  
✅ **Mathematically Rigorous**: All formulas from peer-reviewed research  
✅ **Efficient**: Cached per-group statistics, vectorized operations  
✅ **Comprehensive**: 15 metrics covering all major fairness definitions  
✅ **Production-Ready**: Thresholds, pass/fail, CI/CD integration  
✅ **Standard Benchmarks**: Adult, COMPAS, German Credit included  
✅ **Multiple Exports**: JSON, Markdown, HTML reports  
✅ **Local-First**: No network calls, full privacy  

## Integration with Existing Layers

The Objective Fairness Metrics layer complements existing layers:

- **Attack Layer**: Security testing
- **Truth Layer**: Hallucination/accuracy testing  
- **Governance Layer**: Regulatory compliance
- **Colonization Layer**: Cultural/epistemic bias (qualitative)
- **Objective Fairness**: Algorithmic bias (quantitative)

Together, these provide comprehensive AI safety evaluation.

## Research Foundation

Implementation based on:
- "Objective metrics for ethical AI: a systematic literature review" (2024)
- Standard definitions from algorithmic fairness literature
- Widely-used benchmark datasets (Adult, COMPAS, German Credit)

## Next Steps

1. Run `examples/fairness_demo.py` to see it in action
2. Download standard datasets (Adult, COMPAS, German Credit)
3. Integrate into your testing pipeline
4. Configure thresholds for your use case
5. Add to CI/CD for continuous fairness monitoring
