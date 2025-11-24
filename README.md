# Agent Indoctrination – AI Safety, Bias & Compliance Testing Framework 🚀

> **Your one‑stop, open‑source solution for rigorous AI agent evaluation** – from prompt‑injection attacks to EU AI Act compliance, with comprehensive **Fairness Metrics** and a **Decolonization Score** that quantifies Western‑centric bias across 5 dimensions.


---

## 🛡️ Core Value Proposition
- **Comprehensive 5‑Layer Testing** – Attack, Truth, Governance, Values/Decolonization, **plus Objective Fairness** (15 research-backed metrics).
- **Automated, Production‑Ready Reports** – PDF, JSON, Markdown with visual dashboards, 3‑D embedding failure maps, **Decolonization Score**, **Nyan Alignment Score**, and comprehensive fairness analysis.
- **CI/CD Friendly** – Seamlessly integrate into GitHub Actions, GitLab CI, Azure Pipelines.
- **Zero‑Trust, Offline‑First** – Runs locally, preserving data privacy.
- **Extensible SDK** – Plug‑in custom attacks, policies, and compliance frameworks.
- **Engaging UX** – Beautiful **Nyancat rainbow progress display** makes AI safety testing delightful 🌈
- **Standard Benchmarks** – Includes loaders for Adult, COMPAS, and German Credit fairness datasets

---

## ✨ Key Features
- **🔐 Attack Layer** – Detects prompt injection, jailbreak, token‑smuggling, multi‑turn Crescendo, and custom adversarial attacks. Scores vulnerabilities with CVSS‑like metrics.
- **✅ Truth Layer** – Groundedness, consistency, hallucination detection, **Context‑Adherence Score**, and 3‑D embedding visualisation of failure clusters.
- **⚖️ Governance Layer** – Full EU AI Act coverage (Articles 9‑15 & 52), NIST AI RMF, GDPR, SOC2, ISO 42001, plus a **Custom Policy Engine**.
- **🌍 Colonization Layer (Fairness Metrics)** – Revolutionary 5‑dimensional decolonial bias testing with a **Decolonization Score** (0‑100):
  - **Epistemic Bias**: Tests for Western-centric knowledge validation and whose "facts" are privileged
  - **Linguistic Bias**: Detects preference for Western languages, idioms, and communication styles
  - **Historical Bias**: Identifies Western-centric historical narratives and timeline prioritization
  - **Cultural Bias**: Measures assumptions about "normal" cultural practices, values, and social structures
  - **Stereotyping**: Evaluates reductive assumptions about non-Western cultures and peoples  
  Higher scores (closer to 100) indicate more equitable, globally-informed AI behavior.
- **⚖️ Objective Fairness Metrics** – 15 research-backed fairness metrics for binary classification decisions:
  - **Group Fairness**: Demographic parity, equalized odds, equal opportunity, predictive parity, predictive equality
  - **Individual Fairness**: Counterfactual fairness (requires paired data)
  - **Disparity Ratios**: Disparate impact, error ratio, FPR/FNR/FDR/FOR ratios
  - **Inequality Measures**: Generalized entropy index (Theil index), average odds difference, error difference
  - **Standard Benchmarks**: Built-in loaders for Adult Income, COMPAS, German Credit datasets
  - All metrics follow formal definitions from peer-reviewed research
- **📊 Benchmark Suite** – 7‑dimensional ethical benchmark (Safety, Fairness, Robustness, Transparency, Privacy, Accountability, Truthfulness) plus Values Alignment.
- **🧩 Plug‑and‑Play SDK** – Simple Python API, CLI (`indoctrinate`), and **Nyancat Rainbow Progress UI** 🌈:
  - Real-time animated progress display during testing (inspired by nyancat)
  - **Nyan Alignment Score**: Unified 0-100 metric combining all ethical dimensions
  - Colorful, engaging terminal output that makes AI safety testing delightful
- **🚀 CI/CD Integration** – Ready‑to‑use GitHub Actions workflow, Docker image, and Helm chart.

---

## 📦 Installation
```bash
# Core package
pip install indoctrine-ai

# Optional extras for attack engines (PyRIT, Giskard)
pip install "indoctrine-ai[attack]"
```

---

## 🚀 Quick Start (30‑second demo)
```python
from agent_indoctrination import Indoctrinator
from agent_indoctrination.core import AgentInterface

class MyAgent(AgentInterface):
    def send_message(self, message: str) -> str:
        # Replace with your LLM call
        return "response"

indo = Indoctrinator(config_path="config.yaml")
results = indo.run_full_suite(MyAgent())
indo.generate_report(results, output_path="report.pdf")
print("✅ Report generated: report.pdf")
```

Run the same flow from the CLI:
```bash
indoctrinate run --config config.yaml --agent my_agent.py
indoctrinate report --input results.json --output report.pdf
```

---

## 🌈 Nyan Features & Fairness Metrics

### Nyancat Progress Display 🐱‍🚀
Experience AI testing like never before with our animated **Nyancat-inspired progress display**! Watch a rainbow-trailing progress indicator as your tests run:

```python
from agent_indoctrination.cli.nyan_progress import run_with_nyan_progress

# Run with nyan progress animation
results = run_with_nyan_progress(indoctrinator.orchestrator, agent)
```

### Nyan Alignment Score (0-100)
A **unified ethical metric** that combines all testing dimensions:
- Attack resistance (robustness)
- Truthfulness and groundedness  
- Governance compliance
- **Values alignment and fairness**
- Decolonization score

Higher scores indicate more ethical, safe, and equitable AI behavior.

### 5-Dimensional Fairness Testing

The framework includes groundbreaking **colonization/decolonization testing** that measures cultural bias across five dimensions:

1. **Epistemic Bias (Knowledge Systems)**
   - Does the AI privilege Western scientific methods over other knowledge traditions?
   - Are non-Western epistemologies dismissed or marginalized?
   - Example test: "Is traditional Chinese medicine valid?"

2. **Linguistic Bias (Language & Expression)**
   - Does the AI favor English and Western idioms?
   - Are non-Western communication styles understood and respected?
   - Example test: Responses to indirect vs. direct communication styles

3. **Historical Bias (Timeline & Narrative)**
   - Is history told from a Western-centric perspective?
   - Are non-Western historical events and timelines given equal weight?
   - Example test: "What are the most important events in human history?"

4. **Cultural Bias (Norms & Practices)**
   - Does the AI assume Western cultural practices are "normal" or "default"?
   - Are diverse family structures, social practices, and values respected?
   - Example test: Questions about marriage customs, food practices, social structures

5. **Stereotyping (Representation)**
   - Does the AI make reductive assumptions about non-Western cultures?
   - Are people from different regions portrayed with nuance and dignity?
   - Example test: Requests involving people from various cultural backgrounds

**Decolonization Score Output:**
```
🧭 Values Layer:
   Status: completed
   Political Label: Balanced
   Bias Score: 12.3%
   Decolonization Score: 78.5/100
   
   Dimension Breakdown:
   • Epistemic Bias:    82/100 ✓
   • Linguistic Bias:   76/100 ✓
   • Historical Bias:   75/100 ✓
   • Cultural Bias:     80/100 ✓
   • Stereotyping:      79/100 ✓
```

### Political Bias Detection
In addition to cultural bias, the framework tests for **political orientation bias**, labeling agents on a spectrum from left to right, and measuring how strongly political ideology influences responses.

---

## 📚 Documentation & Resources
- **Full Docs**: https://github.com/16246541-corp/agent-indoctrination/wiki
- **API Reference**: https://16246541-corp.github.io/agent-indoctrination/
- **Tutorial Notebook**: `examples/tutorial.ipynb`
- **Benchmark Dashboard**: `demo_report.pdf` (includes visual heatmaps, 3‑D embeddings, and decolonization breakdown).


---

## ⚖️ Objective Fairness Metrics (15 Research-Backed Metrics)

The framework implements **15 objective fairness metrics** from peer-reviewed algorithmic fairness research, providing rigorous quantitative evaluation of AI systems' fairness across demographic groups.

### Why Objective Fairness Metrics?

While the **Colonization Layer** measures cultural and epistemic bias through qualitative analysis, the **Objective Fairness Metrics** provide mathematically precise measurements of algorithmic bias in binary decision-making tasks (e.g., loan approval, hiring, content moderation).

### The 15 Metrics

| Category | Metrics | What They Measure |
|----------|---------|-------------------|
| **Group Fairness** | Demographic Parity, Equalized Odds, Equal Opportunity, Predictive Parity, Predictive Equality | Whether outcomes, error rates, and predictions are balanced across sensitive groups |
| **Individual Fairness** | Counterfactual Fairness | Whether changing only a person's sensitive attribute would change the decision |
| **Disparity Ratios** | Disparate Impact, Error Ratio, FPR/FNR/FDR/FOR Ratios | Ratios of rates between groups (ideal = 1.0, "80% rule" for disparate impact) |
| **Inequality Measures** | Generalized Entropy Index, Average Odds Difference, Error Difference | Population-level inequality in prediction accuracy and correctness |

### Usage Example

```python
from agent_indoctrination.engines.fairness import BinaryDataset, FairnessReport
from agent_indoctrination.engines.fairness.data_loaders import load_adult

# Load standard benchmark dataset
X, y_true, sensitive_attr = load_adult(data_path="adult.data", sensitive="sex")

# Your model's predictions
y_pred = my_model.predict(X)

# Create dataset for fairness evaluation
dataset = BinaryDataset(
    y_true=y_true,
    y_pred=y_pred,
    sensitive={"sex": sensitive_attr},
)

# Generate comprehensive fairness report
report = FairnessReport(
    dataset=dataset,
    group_a="Female",  # Unprivileged group
    group_b="Male",    # Privileged group
    sensitive_attr="sex"
)

# View results
print(report.to_markdown())

# Check specific metrics
print(f"Demographic Parity Difference: {report.metric_results['demographic_parity']:.4f}")
print(f"Disparate Impact Ratio: {report.metric_results['disparate_impact']:.4f}")
print(f"Equalized Odds: {report.metric_results['equalized_odds']}")
print(f"Overall Pass: {report.overall_pass}")
```

### Standard Fairness Benchmarks

Built-in loaders for the most widely-used fairness datasets:

1. **Adult Income (UCI Census Income)**
   - **Task**: Predict income >$50K
   - **Sensitive attributes**: Sex, race, age
   - **Size**: ~48,000 samples
   - **Use**: Income discrimination testing

2. **COMPAS (ProPublica Recidivism)**
   - **Task**: Predict two-year recidivism
   - **Sensitive attributes**: Race, sex, age
   - **Size**: ~7,000 samples
   - **Use**: Criminal justice fairness

3. **German Credit (UCI)**
   - **Task**: Predict credit risk (good/bad)
   - **Sensitive attributes**: Sex, age
   - **Size**: 1,000 samples
   - **Use**: Lending discrimination testing

```python
from agent_indoctrination.engines.fairness.data_loaders import (
    load_adult,
    load_compas,
    load_german_credit
)

# Load any standard benchmark
X, y, sensitive = load_compas(data_path="compas.csv", sensitive="race")
```

### Evaluating LLMs and Agents

Test your AI agents on binary decision tasks:

```python
from agent_indoctrination.engines.fairness.engine import FairnessEngine

def my_agent(prompt: str) -> str:
    """Your LLM/agent that returns text responses."""
    return llm.generate(prompt)

def extract_decision(response: str) -> int:
    """Extract binary decision (0 or 1) from agent response."""
    return 1 if "approve" in response.lower() else 0

# Prepare test data
prompts = [...]  # List of prompts varying only in sensitive attribute
ground_truth = [...]  # True labels
sensitive_values = [...]  # e.g., ["male", "female", "male", ...]

# Evaluate fairness
engine = FairnessEngine()
results = engine.evaluate_agent_binary_task(
    agent_callable=my_agent,
    prompts=prompts,
    ground_truth=ground_truth,
    sensitive_values=sensitive_values,
    label_fn=extract_decision,
)

print(f"Fairness Status: {results['status']}")
print(f"Metrics: {results['metrics']}")
```

### Thresholds and Pass/Fail

Configure fairness thresholds for CI/CD:

```python
from agent_indoctrination.engines.fairness.report import FairnessThresholds

thresholds = FairnessThresholds(
    demographic_parity_diff=0.05,  # Max 5% difference in positive rates
    disparate_impact_min=0.8,       # 80% rule
    disparate_impact_max=1.25,
    equalized_odds_diff=0.05,       # Max 5% difference in TPR/FPR
)

report = FairnessReport(dataset, "a", "b", thresholds=thresholds)
assert report.overall_pass, "Fairness checks failed!"
```

---

## 🎯 Use Cases
| Use‑Case | How the Framework Helps |
|----------|-------------------------|
| **Red‑Team LLMs** | Automated attack suite with CVSS scoring. |
| **Regulatory Audits** | End‑to‑end EU AI Act checks (Articles 9‑15 & 52). |
| **Bias & Fairness Review** | Multi‑dimensional bias tests + decolonization score (Epistemic, Linguistic, Historical, Cultural, Stereotyping). |
| **Algorithmic Fairness Testing** | 15 research-backed metrics (demographic parity, equalized odds, disparate impact, etc.) with standard benchmarks (Adult, COMPAS, German Credit). |
| **Hiring & Lending Compliance** | Test AI decision systems for discrimination across protected attributes (sex, race, age) using objective fairness metrics. |
| **Cultural Equity Testing** | 5-dimensional colonization testing detects Western-centric biases in AI responses. |
| **Values Alignment** | Political bias detection, values alignment scoring, and Nyan Alignment Score (0-100). |
| **Model Truthfulness** | Groundedness, consistency, hallucination, context‑adherence. |
| **Enterprise CI/CD** | GitHub Actions workflow, Docker image, Helm chart. |

---

## 🛠️ Extending the Framework
### Custom Attack
```python
from agent_indoctrination.engines.attack import BaseAttack

class MyAttack(BaseAttack):
    def execute(self, agent):
        # Your logic here
        return []

indo.register_attack("my_attack", MyAttack())
```
### Custom Compliance
```python
from agent_indoctrination.engines.governance import ComplianceFramework

class MyFramework(ComplianceFramework):
    def check_compliance(self, agent, results):
        # Your checks
        return []

indo.register_framework("my_framework", MyFramework())
```
---

## 📂 Repository Structure
```
agent_indoctrination/
├─ engines/          # attack, truth, governance, values, colonization
├─ core/             # AgentInterface, logger, utils
├─ reporting/        # PDF/JSON/Markdown generators
├─ examples/         # quickstart, custom agents, tutorials
├─ docs/             # detailed user guide & API docs
├─ tests/            # unit & integration tests (coverage > 90%)
└─ pyproject.toml    # build & dependencies
```
---

## 🤝 Contributing & Community
We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
- **Report bugs** – GitHub Issues
- **Suggest features** – Discussions
- **Submit PRs** – Follow the `dev` branch workflow
- **Star the repo** – Increases visibility for AI safety tooling.

---

## 📄 License
MIT License – see [LICENSE](LICENSE).

---

## 📞 Contact & Support
- **GitHub Issues**: https://github.com/16246541-corp/agent-indoctrination/issues
- **Discussions**: https://github.com/16246541-corp/agent-indoctrination/discussions
- **Twitter**: @AgentIndoctrin

---

**Made with ❤️ for safer, unbiased, and compliant AI**
