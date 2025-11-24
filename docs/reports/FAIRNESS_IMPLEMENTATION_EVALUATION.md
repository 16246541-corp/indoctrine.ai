# Fairness Metrics Implementation - Evaluation Report

**Evaluation Date**: 2025-11-24  
**Framework**: Indoctrine AI - Objective Fairness Metrics Layer  
**Evaluator**: Technical Review

---

## Executive Summary

Your fairness metrics implementation demonstrates **strong mathematical rigor** and **solid architectural design**, but has significant opportunities for improvement in **usability**, **LLM/agent ergonomics**, **interpretability**, and **educational guidance**. The implementation excels at correctness but falls short on the "5 lines of code" promise and lacks the interpretive layer that would make it truly accessible to non-experts.

**Overall Grade**: B+ (Strong Foundation, Needs User-Facing Polish)

---

## 1. 🎯 Usability: "5 Lines of Code" Test

### Current State: ⚠️ **PARTIAL PASS** (6-7/10)

#### What Works ✅
- Clean, Pythonic API design
- Good separation of concerns (dataset, metrics, report, engine)
- Multiple export formats (JSON, Markdown, HTML)
- Standard dataset loaders for common benchmarks

#### The "5 Lines" Reality Check ❌

**Your README claims:**
```python
# 5 lines to get a meaningful report
from agent_indoctrination.engines.fairness import BinaryDataset, FairnessReport

dataset = BinaryDataset(y_true=y_true, y_pred=y_pred, sensitive={"sex": sex_values})
report = FairnessReport(dataset, "Female", "Male", "sex")
print(report.to_markdown())
```

**Reality Check:**
- User still needs to prepare `y_true`, `y_pred`, `sex_values` (data loading/preprocessing)
- For LLM testing, it's actually **10-15 lines minimum** (see `fairness_demo.py`)
- No guidance on *which metrics matter* for their use case
- Requires understanding of group_a vs group_b semantics

**What "5 Lines" Should Look Like:**
```python
from agent_indoctrination.fairness import evaluate_fairness

# One-liner for standard datasets
report = evaluate_fairness.from_adult_dataset("adult.data", model=my_model)

# One-liner for custom binary predictions
report = evaluate_fairness.quick_check(y_true, y_pred, sensitive_attr)

# One-liner for LLM agents
report = evaluate_fairness.test_agent(my_agent, prompts, ground_truth, demographics)
```

### Recommendations for Improvement 🔧

1. **Add convenience wrappers:**
   ```python
   # In fairness/__init__.py
   def quick_fairness_check(
       y_true, y_pred, sensitive_values,
       use_case="hiring"  # Auto-selects relevant thresholds
   ):
       """One-function fairness check with smart defaults."""
       pass
   ```

2. **Smart defaults for common use cases:**
   - `thresholds_for_hiring()` - stricter thresholds
   - `thresholds_for_content_moderation()` - balanced
   - `thresholds_for_research()` - exploratory

3. **Auto-detect privileged/unprivileged groups:**
   ```python
   # Instead of requiring user to specify:
   report = FairnessReport(dataset, "Female", "Male", ...)
   
   # Auto-detect based on positive rate disparity:
   report = FairnessReport(dataset, sensitive_attr="sex")
   # Automatically identifies "Female" as unprivileged if lower positive rate
   ```

4. **Integrated data loading:**
   ```python
   # Currently: Multi-step process
   X, y_true, sensitive = load_adult(...)
   y_pred = model.predict(X)
   dataset = BinaryDataset(y_true, y_pred, sensitive)
   
   # Should be:
   report = evaluate_fairness.from_sklearn_model(
       model, X, y, sensitive_attr="sex", dataset="adult"
   )
   ```

---

## 2. 🤖 LLM/Agent Ergonomics

### Current State: ⚠️ **NEEDS WORK** (5/10)

#### What Works ✅
- `FairnessEngine.evaluate_agent_binary_task()` exists
- Handles agent callable pattern
- Label extraction function is flexible

#### What Feels "Bolted-On" ❌

**Current LLM evaluation workflow:**
```python
engine = FairnessEngine()
results = engine.evaluate_agent_binary_task(
    agent_callable=my_agent,
    prompts=prompts,              # User must create these
    ground_truth=true_labels,     # User must have labels
    sensitive_values=sensitive,   # User must align these
    label_fn=extract_binary_decision,  # User must write this
)
```

**Problems:**
1. **No prompt template helpers** - Users must manually create demographic variants
2. **No counterfactual pair generation** - Critical for LLM fairness, not automated
3. **No async/batch optimization** - Will be slow for LLM calls
4. **No retry logic** - LLM calls fail, no graceful degradation
5. **No token usage tracking** - Cost blindness
6. **No caching** - Re-tests identical prompts

### Critical Missing Feature: Prompt Variant Testing 🚨

**What You Need:**
```python
from agent_indoctrination.fairness import PromptFairnessTest

# Auto-generates demographic variants from template
test = PromptFairnessTest(
    template="Should we hire {name} for the engineering role? "
             "Background: {background}",
    demographic_variants={
        "name": ["Jamal", "Connor", "Mei", "Raj"],
        "gender_pronouns": ["he/him", "she/her", "they/them"]
    },
    task="binary_decision",
    ground_truth_fn=lambda variant: 1  # All should be hired
)

# Test with automatic counterfactual pairing
report = test.evaluate(my_llm_agent, n_trials=100)
```

**Why This Matters:**
- LLMs don't have "predictions" - they have *responses to prompts*
- Fairness testing for LLMs is fundamentally about **counterfactual consistency**
- You need to test: "Does changing name from 'Connor' to 'Jamal' change the decision?"

### Recommendations for Improvement 🔧

1. **Add `PromptFairnessTest` class:**
   - Template-based demographic variant generation
   - Automatic counterfactual pairing
   - Built-in name lists (common names across demographics)
   - Async batch processing with rate limiting

2. **LLM-specific metrics:**
   - Response consistency (same prompt → same decision?)
   - Confidence calibration across groups
   - Explanation fairness (does justification differ by demographic?)

3. **Integration with popular LLM libraries:**
   ```python
   # Direct integration
   from langchain import OpenAI
   from agent_indoctrination.fairness import test_llm_fairness
   
   llm = OpenAI(model="gpt-4")
   report = test_llm_fairness(
       llm, 
       task="resume_screening",  # Pre-built template
       demographics=["race", "gender"]
   )
   ```

4. **Streaming progress for slow LLM calls:**
   - Show real-time progress (current prompt, decisions so far)
   - Early stopping if fairness violations are severe
   - Cost estimation before running full suite

---

## 3. 📚 Interpretability Layer: Beyond Numbers

### Current State: ❌ **MAJOR GAP** (3/10)

This is your **biggest weakness**. Your implementation provides numbers but no *understanding*.

#### What's Missing 🚨

**Current output:**
```
Disparate Impact Ratio: 0.75
```

**What a non-expert sees:** "Is 0.75 good or bad? What does this mean for my hiring process?"

**What they need:**
```
⚠️ DISPARATE IMPACT: 0.75 (FAIL - Below 0.8 threshold)

What this means:
  Women are 25% less likely to receive positive predictions than men.
  
  In a hiring context, this suggests:
  - Out of 100 qualified women, only 75 would be recommended
  - While all 100 equally qualified men would be recommended
  
Legal implications:
  - This violates the "80% rule" used by EEOC in disparate impact cases
  - May expose your organization to discrimination lawsuits
  
Recommended actions:
  1. Audit training data for gender representation
  2. Check if feature engineering inadvertently encodes gender
  3. Consider adversarial debiasing or fairness constraints
  4. Consult legal team before deployment
```

### Critical Missing Features:

1. **No contextual explanations** for metric values
2. **No guidance system** for what to do when metrics fail
3. **No severity scoring** (is 0.75 slightly bad or catastrophic?)
4. **No use-case-specific interpretation** (hiring vs lending vs content moderation)
5. **No educational tooltips** for technical terms (TPR, FPR, etc.)

### Recommendations for Improvement 🔧

#### 1. Add `MetricInterpreter` Class

```python
class MetricInterpreter:
    """Provides human-readable interpretations of fairness metrics."""
    
    def interpret(self, metric_name: str, value: float, use_case: str) -> dict:
        """
        Returns:
            {
                "plain_english": "Women are 25% less likely...",
                "severity": "high",  # low, medium, high, critical
                "legal_risk": "EEOC 80% rule violation",
                "recommended_actions": [...],
                "learn_more_url": "..."
            }
        """
        pass
```

#### 2. Enhanced Report with Guidance

```python
class GuidedFairnessReport(FairnessReport):
    """Extended report with interpretability layer."""
    
    def to_guided_markdown(self) -> str:
        """Include explanations, severity, and recommendations."""
        pass
    
    def get_top_concerns(self, n=3) -> list:
        """Return the N most severe fairness issues with guidance."""
        pass
    
    def get_remediation_plan(self) -> dict:
        """Generate step-by-step plan to address failures."""
        pass
```

#### 3. Interactive Educational Features

```python
# In Markdown/HTML reports:
"""
## 📖 Understanding Your Metrics

### Demographic Parity (Failed: -0.15)

**What it measures:** Whether different groups receive positive outcomes at the same rate.

**Your result:** Group A receives positive outcomes 15% less often than Group B.

**Is this fair?** It depends on your use case:
  ✅ Acceptable if: Groups have genuinely different qualification rates
  ❌ Problematic if: Groups should be equally qualified but aren't treated equally

**Common causes:**
  - Biased training data
  - Proxy features (e.g., zip code → race)
  - Historical discrimination in labels

**Next steps:**
  1. [Check training data distribution]
  2. [Audit feature importance]
  3. [Try fairness interventions]
  
[Learn more about demographic parity →](https://fairmlbook.org/demographic.html)
"""
```

#### 4. Add Comparative Benchmarks

```python
# Show how your model compares to typical values
"""
Your Model: Disparate Impact = 0.75
Industry Average: 0.85-0.95
Best Practice: > 0.95
Legal Threshold: > 0.80 (EEOC 80% rule)

You are: ⚠️ Below legal threshold
"""
```

#### 5. Risk Scoring System

```python
def calculate_unfairness_risk_score(self) -> dict:
    """
    Aggregate risk score across all metrics.
    
    Returns:
        {
            "overall_risk": "HIGH",  # LOW, MEDIUM, HIGH, CRITICAL
            "risk_factors": [
                {"metric": "disparate_impact", "contribution": 0.4, ...},
                ...
            ],
            "deployment_recommendation": "DO NOT DEPLOY - High legal risk"
        }
    """
    pass
```

---

## 4. ⚡ Performance: Million-Scale Data

### Current State: ⚠️ **MOSTLY GOOD** (7/10)

#### What Works ✅
- **Efficient caching** of group stats (`_stats_cache` in `BinaryDataset`)
- **Vectorized operations** with NumPy
- **Minimal redundant computation**
- **Lazy evaluation** via `@property` decorators

#### Performance Analysis

**Estimated Performance:**
- **1,000 samples**: < 1ms ✅
- **100,000 samples**: ~50ms ✅
- **1,000,000 samples**: ~500ms ⚠️ (sub-second, but close)
- **10,000,000 samples**: ~5-10s ❌ (exceeds sub-second)

#### Bottlenecks at Scale 🐌

1. **Confusion matrix computation** (`dataset.py:179-184`)
   - 4 separate `np.sum()` calls per group
   - Could be vectorized into single pass

2. **No parallelization** for multiple group comparisons

3. **HTML/Markdown generation** not optimized for large reports

4. **Memory inefficiency** for repeated evaluations (stores full arrays)

### Recommendations for Improvement 🔧

#### 1. Optimize Confusion Matrix Computation

```python
# Current (4 passes):
tp=int(np.sum((y_true_group == 1) & (y_pred_group == 1))),
fp=int(np.sum((y_true_group == 0) & (y_pred_group == 1))),
tn=int(np.sum((y_true_group == 0) & (y_pred_group == 0))),
fn=int(np.sum((y_true_group == 1) & (y_pred_group == 0))),

# Optimized (1 pass):
from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(
    y_true_group, y_pred_group, labels=[0, 1]
).ravel()
```

#### 2. Add Parallel Processing for Multiple Groups

```python
from concurrent.futures import ProcessPoolExecutor

def run_parallel(self, dataset, group_comparisons, ...):
    """Use multiprocessing for large group comparison sets."""
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(self._evaluate_pair, dataset, a, b)
            for a, b in group_comparisons
        ]
        results = [f.result() for f in futures]
```

#### 3. Streaming for Massive Datasets

```python
class StreamingFairnessEvaluator:
    """Compute fairness metrics on data that doesn't fit in memory."""
    
    def __init__(self):
        self.group_accumulators = {}
    
    def update(self, y_true_batch, y_pred_batch, sensitive_batch):
        """Incrementally update statistics."""
        # Use online algorithms (Welford's method, etc.)
        pass
    
    def finalize(self) -> FairnessReport:
        """Compute final metrics from accumulated stats."""
        pass
```

#### 4. Benchmark Suite

Add a `benchmarks/` directory with:
```python
# benchmarks/performance_test.py
def test_million_scale():
    sizes = [1e3, 1e4, 1e5, 1e6, 1e7]
    for n in sizes:
        dataset = generate_synthetic(n)
        t0 = time.time()
        report = FairnessReport(dataset, ...)
        elapsed = time.time() - t0
        print(f"{n:>10} samples: {elapsed*1000:>8.2f} ms")
```

---

## 5. 🛡️ Robustness: Edge Cases

### Current State: ⚠️ **GAPS EXIST** (6/10)

#### What Works ✅
- **Input validation** in `BinaryDataset._validate()`
- **Zero-rate handling** in ratio metrics (returns `inf`)
- **Missing pair handling** in counterfactual fairness

#### Critical Edge Cases Not Handled ❌

### 1. **Group with Zero Positive Predictions**

```python
# Current behavior in metrics.py:179-180
if stats_b.positive_rate == 0:
    return float('inf') if stats_a.positive_rate > 0 else 1.0
```

**Problem:** Returns `inf`, which breaks JSON serialization and report generation.

**Fix:**
```python
if stats_b.positive_rate == 0:
    if stats_a.positive_rate == 0:
        return 1.0  # Both zero = parity
    else:
        # Return sentinel value, add warning
        warnings.warn(f"Group {group_b} has zero positive rate")
        return np.nan  # Or a large sentinel like 999.0
```

### 2. **Severe Class Imbalance** (99% negative class)

**Current:** No warnings, metrics may be misleading

**Fix:**
```python
def check_class_balance(dataset: BinaryDataset) -> dict:
    """Warn if severe imbalance exists."""
    pos_rate = np.mean(dataset.y_true)
    
    if pos_rate < 0.01 or pos_rate > 0.99:
        return {
            "severe_imbalance": True,
            "warning": f"Only {pos_rate*100:.1f}% positive class. "
                      "Metrics may be unreliable. Consider stratified sampling."
        }
```

### 3. **Empty Groups After Filtering**

```python
# In dataset.py:175-177
mask = self.sensitive[sensitive_attr] == group_value
y_true_group = self.y_true[mask]
# What if mask.sum() == 0?
```

**Fix:**
```python
if mask.sum() == 0:
    raise ValueError(
        f"No samples found for group '{group_value}' "
        f"in attribute '{sensitive_attr}'"
    )
```

### 4. **Missing Sensitive Attributes (NaN/None)**

**Current:** No handling of missing demographic data

**Fix:**
```python
# In BinaryDataset.__init__:
if np.any(pd.isna(self.sensitive[attr])):
    warnings.warn(
        f"Sensitive attribute '{attr}' contains {np.sum(pd.isna(...))} "
        "missing values. Consider:\n"
        "  - Imputing with separate 'Unknown' category\n"
        "  - Dropping samples with missing demographics\n"
        "  - Using demographic inference (with caution)"
    )
```

### 5. **Extreme Group Size Imbalance** (95% Group A, 5% Group B)

**Current:** Metrics computed but may have high variance for small group

**Fix:**
```python
def check_group_size_balance(stats_a, stats_b):
    ratio = min(stats_a.n, stats_b.n) / max(stats_a.n, stats_b.n)
    
    if ratio < 0.1:  # More than 10:1 imbalance
        return {
            "warning": f"Severe group size imbalance: {stats_a.n} vs {stats_b.n}. "
                      "Metrics for smaller group may have high variance. "
                      "Consider bootstrapping for confidence intervals."
        }
```

### 6. **Perfect Predictions (100% accuracy)**

**Current:** Most metrics return 0, which is correct but uninformative

**Fix:**
```python
if np.all(dataset.y_true == dataset.y_pred):
    return {
        "note": "Model has perfect accuracy. "
                "Fairness metrics are trivially satisfied. "
                "Consider testing on holdout data or adversarial examples."
    }
```

### Recommendations for Improvement 🔧

#### 1. Add `DataQualityChecker`

```python
class FairnessDataQualityChecker:
    """Pre-flight checks before fairness evaluation."""
    
    def check(self, dataset: BinaryDataset) -> dict:
        """
        Returns warnings/errors for:
          - Class imbalance
          - Group size imbalance
          - Missing values
          - Zero-rate groups
          - Perfect accuracy
          - Suspicious patterns
        """
        issues = {
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        # Check class balance
        # Check group sizes
        # Check for zero rates
        # etc.
        
        return issues
```

#### 2. Graceful Degradation

```python
# In FairnessReport._compute_all_metrics:
results = {}
for metric_name, metric_fn in METRICS.items():
    try:
        results[metric_name] = metric_fn(...)
    except (ZeroDivisionError, ValueError) as e:
        results[metric_name] = {
            "value": None,
            "error": str(e),
            "skipped": True
        }
        warnings.warn(f"Metric {metric_name} failed: {e}")
```

#### 3. Statistical Significance Testing

```python
def compute_with_confidence_intervals(
    dataset: BinaryDataset, 
    group_a, group_b,
    n_bootstrap=1000
) -> dict:
    """Use bootstrapping to get confidence intervals on metrics."""
    # Especially important for small groups
    pass
```

#### 4. Comprehensive Test Suite

```python
# tests/test_edge_cases.py
def test_zero_positive_rate():
    y_true = [0, 0, 0, 0, 0]
    y_pred = [0, 0, 0, 0, 0]
    sensitive = [0, 0, 1, 1, 1]
    # Should not crash, should warn

def test_class_imbalance_99_1():
    # ...

def test_empty_group():
    # Should raise informative error

def test_missing_sensitive_attr():
    sensitive = [0, 1, np.nan, 0, 1]
    # Should warn or error
```

---

## 6. 🎨 Additional Recommendations

### A. Documentation Improvements

1. **Add "Quick Start by Use Case" guide:**
   - Hiring/Recruitment
   - Lending/Credit
   - Content Moderation
   - Healthcare Triage
   - Criminal Justice

2. **Create decision tree for metric selection:**
   ```
   What are you optimizing for?
   ├─ Equal treatment regardless of qualification → Demographic Parity
   ├─ Equal opportunity for qualified individuals → Equal Opportunity
   ├─ Equal prediction accuracy → Equalized Odds
   └─ Causal fairness (counterfactual) → Counterfactual Fairness
   ```

3. **Add troubleshooting guide:**
   - "My disparate impact is 0.6, what now?"
   - "Metrics conflict with each other"
   - "How to choose thresholds for my industry?"

### B. Integration Improvements

1. **One-line CI/CD integration:**
   ```yaml
   # .github/workflows/fairness.yml
   - name: Fairness Check
     run: |
       indoctrinate fairness-check \
         --model models/latest.pkl \
         --test-data data/test.csv \
         --sensitive-attr gender,race \
         --fail-on-threshold
   ```

2. **Integration with MLOps tools:**
   - MLflow integration (log metrics as artifacts)
   - Weights & Biases integration
   - TensorBoard plugin

### C. Advanced Features

1. **Multi-attribute intersectional fairness:**
   ```python
   # Currently: Binary comparisons
   # Needed: Intersectional (e.g., Black Women vs White Men)
   report = IntersectionalFairnessReport(
       dataset,
       intersections=[
           {"race": "Black", "gender": "Female"},
           {"race": "White", "gender": "Male"}
       ]
   )
   ```

2. **Temporal fairness tracking:**
   ```python
   # Track how fairness evolves as model is retrained
   tracker = FairnessTracker()
   tracker.add_snapshot("v1.0", report_v1)
   tracker.add_snapshot("v2.0", report_v2)
   tracker.plot_trend("disparate_impact")
   ```

3. **Fairness intervention suggestions:**
   ```python
   interventions = suggest_fairness_interventions(report)
   # Returns:
   # - Reweighting
   # - Threshold optimization
   # - Adversarial debiasing
   # - Data augmentation
   ```

---

## 7. 🏁 Final Evaluation Summary

| Criterion | Score | Status | Priority |
|-----------|-------|--------|----------|
| **Usability** | 6/10 | Needs Work | 🔥 High |
| **LLM/Agent Ergonomics** | 5/10 | Needs Major Work | 🔥 Critical |
| **Interpretability** | 3/10 | Major Gap | 🔥🔥 Critical |
| **Performance** | 7/10 | Good | Medium |
| **Robustness** | 6/10 | Needs Work | 🔥 High |

### Top 5 Priorities

1. **🚨 Add Interpretability Layer** (Biggest Impact)
   - Metric interpreters with plain-English explanations
   - Severity scoring
   - Remediation guidance

2. **🚨 LLM-First Fairness Testing** (Differentiator)
   - Prompt template system
   - Automatic demographic variant generation
   - Counterfactual consistency testing

3. **📝 True "5-Line" Convenience API** (User Experience)
   - `quick_fairness_check()` wrapper
   - Use-case-specific presets
   - Smart defaults

4. **🛡️ Robustness Hardening** (Production-Ready)
   - Data quality pre-flight checks
   - Graceful degradation
   - Comprehensive edge case tests

5. **📚 Educational Content** (Accessibility)
   - In-tool tooltips and explanations
   - Use-case-specific guides
   - Interactive examples

---

## 8. 📊 Competitive Positioning

### How Your Implementation Compares

| Feature | Your Implementation | Fairlearn | AIF360 | Google's What-If Tool |
|---------|-------------------|-----------|--------|----------------------|
| Mathematical Rigor | ✅ Excellent | ✅ Excellent | ✅ Excellent | ⚠️ Good |
| Usability | ⚠️ Medium | ✅ Good | ⚠️ Medium | ✅ Excellent |
| LLM Support | ❌ Basic | ❌ None | ❌ None | ⚠️ Limited |
| Interpretability | ❌ Minimal | ⚠️ Medium | ⚠️ Medium | ✅ Excellent |
| Performance | ✅ Good | ✅ Good | ⚠️ Medium | ✅ Excellent |
| Documentation | ⚠️ Good | ✅ Excellent | ✅ Excellent | ✅ Excellent |

**Your Unique Advantage:** First-class LLM/agent support *when you build it out*

**Your Biggest Gap:** Interpretability and educational layer

---

## 9. 🎯 Roadmap Suggestion

### Phase 1: Foundation Fixes (2-3 weeks)
- [ ] Add `MetricInterpreter` class
- [ ] Implement `quick_fairness_check()` wrapper
- [ ] Fix edge case handling (zero rates, class imbalance)
- [ ] Add data quality pre-flight checks

### Phase 2: LLM Excellence (3-4 weeks)
- [ ] `PromptFairnessTest` with template system
- [ ] Demographic variant auto-generation
- [ ] Async batch processing for LLM calls
- [ ] Example gallery for common LLM tasks

### Phase 3: Polish & Scale (2-3 weeks)
- [ ] Performance optimization for 10M+ samples
- [ ] Comprehensive test suite (>95% coverage)
- [ ] Tutorial notebooks for each use case
- [ ] Integration with MLflow, W&B

### Phase 4: Advanced Features (Ongoing)
- [ ] Intersectional fairness
- [ ] Temporal fairness tracking
- [ ] Automated intervention suggestions
- [ ] Interactive dashboard (Streamlit/Gradio)

---

## 💡 Conclusion

You've built a **mathematically sound, architecturally clean fairness metrics library**. The implementation is correct and comprehensive.

**However**, you're competing in a space with mature tools (Fairlearn, AIF360). To win:

1. **Be 10x easier** - True "5 lines" with smart defaults
2. **Be LLM-native** - This is your killer feature
3. **Teach, don't just measure** - Interpretability is everything

**Your current implementation is a B+ technical foundation. With the interpretability layer and LLM ergonomics, it could be an A+ product that people actually use and recommend.**

The question isn't "does the math work?" (it does). The question is: **"Will a PM at a startup choose your library over Fairlearn?"**

Right now: Probably not (unless they need LLM testing).

After Phase 1-2: Almost certainly yes.

---

**Next Steps:**
1. Run `examples/fairness_demo.py` to experience current UX
2. Prototype `MetricInterpreter` class with 2-3 metrics
3. Build one end-to-end LLM fairness example
4. Get user feedback from non-ML-expert stakeholders

**Questions to Consider:**
- Who is your primary user? (Data scientist, PM, legal/compliance, researcher?)
- What's the #1 action you want them to take after seeing a report?
- How can you make fairness testing *delightful* instead of *dutiful*?
