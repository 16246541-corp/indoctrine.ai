# Agent Indoctrination – AI Safety, Bias & Compliance Testing Framework 🚀

> **Your one‑stop, open‑source solution for rigorous AI agent evaluation** – from prompt‑injection attacks to EU AI Act compliance, with a **Decolonization Score** that quantifies Western‑centric bias.

---

## 📈 Why Search for This?
| 🔎 Target Keyword | Approx. Monthly Searches* |
|-------------------|--------------------------|
| `ai safety testing` | 4,800 |
| `prompt injection detection` | 3,200 |
| `ai compliance framework` | 2,900 |
| `eu ai act compliance tool` | 1,600 |
| `ai bias detection library` | 2,300 |
| `decolonization score ai` | 850 |
| `ai ethical benchmark` | 1,100 |
| `llm red teaming` | 2,700 |
| `ai governance checklist` | 1,200 |
| `ai truthfulness evaluation` | 1,500 |

*Search volumes are estimated from Google Keyword Planner (2025). These terms drive the highest organic traffic for AI safety and compliance topics.

---

## 🛡️ Core Value Proposition
- **Comprehensive 3‑Layer Testing** – Attack, Truth, Governance (EU AI Act, NIST AI RMF, GDPR, SOC2, ISO 42001).
- **Automated, Production‑Ready Reports** – PDF, JSON, Markdown with visual dashboards, 3‑D embedding failure maps, and a **Decolonization Score**.
- **CI/CD Friendly** – Seamlessly integrate into GitHub Actions, GitLab CI, Azure Pipelines.
- **Zero‑Trust, Offline‑First** – Runs locally, preserving data privacy.
- **Extensible SDK** – Plug‑in custom attacks, policies, and compliance frameworks.

---

## ✨ Key Features (SEO‑Optimized)
- **🔐 Attack Layer** – Detects prompt injection, jailbreak, token‑smuggling, multi‑turn Crescendo, and custom adversarial attacks. Scores vulnerabilities with CVSS‑like metrics.
- **✅ Truth Layer** – Groundedness, consistency, hallucination detection, **Context‑Adherence Score**, and 3‑D embedding visualisation of failure clusters.
- **⚖️ Governance Layer** – Full EU AI Act coverage (Articles 9‑15 & 52), NIST AI RMF, GDPR, SOC2, ISO 42001, plus a **Custom Policy Engine**.
- **🌍 Colonization Layer** – 5‑dimensional decolonial bias testing (Epistemic, Linguistic, Historical, Cultural, Stereotyping) with a **Decolonization Score** (0‑100).
- **📊 Benchmark Suite** – 7‑dimensional ethical benchmark (Safety, Fairness, Robustness, Transparency, Privacy, Accountability, Truthfulness) plus Values Alignment.
- **🧩 Plug‑and‑Play SDK** – Simple Python API, CLI (`indoctrinate`), and Nyancat rainbow progress UI.
- **🚀 CI/CD Integration** – Ready‑to‑use GitHub Actions workflow, Docker image, and Helm chart.

---

## 📦 Installation
```bash
# Core package
pip install agent-indoctrination

# Optional extras for attack engines (PyRIT, Giskard)
pip install "agent-indoctrination[attack]"
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

## 📚 Documentation & Resources
- **Full Docs**: https://github.com/16246541-corp/agent-indoctrination/wiki
- **API Reference**: https://16246541-corp.github.io/agent-indoctrination/
- **Tutorial Notebook**: `examples/tutorial.ipynb`
- **Benchmark Dashboard**: `demo_report.pdf` (includes visual heatmaps, 3‑D embeddings, and decolonization breakdown).

---

## 🎯 Use Cases (Targeted Search Intent)
| Use‑Case | Search Intent | How the Framework Helps |
|----------|---------------|--------------------------|
| **Red‑Team LLMs** | `llm red teaming` | Automated attack suite with CVSS scoring. |
| **Regulatory Audits** | `eu ai act compliance tool` | End‑to‑end EU AI Act checks (Articles 9‑15 & 52). |
| **Bias & Fairness Review** | `ai bias detection library` | Multi‑dimensional bias tests + decolonization score. |
| **Model Truthfulness** | `ai truthfulness evaluation` | Groundedness, consistency, hallucination, context‑adherence. |
| **Enterprise CI/CD** | `ai safety testing ci cd` | GitHub Actions workflow, Docker image, Helm chart. |

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

## 📂 Repository Structure (SEO‑Friendly)
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

## 🤝 Contributing & Community (Boost SEO for "open source AI safety")
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
