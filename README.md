# Agent Indoctrination – AI Safety, Bias & Compliance Testing Framework 🚀
## PyPI : https://pypi.org/project/agent_indoctrination/
> **Your one‑stop, open‑source solution for rigorous AI agent evaluation** – from prompt‑injection attacks to EU AI Act compliance, with a **Decolonization Score** that quantifies Western‑ce[...]

---


---

## 🛡️ Core Value Proposition
- **Comprehensive 3‑Layer Testing** – Attack, Truth, Governance (EU AI Act, NIST AI RMF, GDPR, SOC2, ISO 42001).
- **Automated, Production‑Ready Reports** – PDF, JSON, Markdown with visual dashboards, 3‑D embedding failure maps, and a **Decolonization Score**.
- **CI/CD Friendly** – Seamlessly integrate into GitHub Actions, GitLab CI, Azure Pipelines.
- **Zero‑Trust, Offline‑First** – Runs locally, preserving data privacy.
- **Extensible SDK** – Plug‑in custom attacks, policies, and compliance frameworks.

---

## ✨ Key Features 
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
pip install indoctrine-ai

# Optional extras for attack engines (PyRIT, Giskard)
pip install "indoctrine-ai"
```

---

## 🛠️ Setup Tutorial
### 1️⃣ Installing and Running Ollama
1. **Download Ollama** – Visit https://ollama.com and download the macOS installer.
2. **Install a model** – Open a terminal and run:
   ```bash
   ollama pull llama2:13b
   ```
   (Replace `llama2:13b` with any model you prefer.)
3. **Start the server** – Run:
   ```bash
   ollama serve
   ```
   The server will listen on `http://localhost:11434`.
4. **Verify** – In a new terminal, execute:
   ```bash
   curl http://localhost:11434/api/tags
   ```
   You should see a JSON list of available models.

### 2️⃣ Installing and Configuring LM Studio
1. **Download LM Studio** – Get the macOS app from https://lmstudio.ai.
2. **Add a model** – In LM Studio, click **Add Model**, choose **Ollama** as the source, and select the model you pulled earlier.
3. **Set the endpoint** – Ensure the endpoint URL is `http://localhost:11434/v1` (OpenAI compatible).
4. **Test a request** – Use the built‑in chat UI to send a prompt and confirm a response is returned.

### 3️⃣ Connecting Indoctrination to Your LLM
Create a simple configuration file `config.yaml`:
```yaml
llm:
  provider: "ollama"
  endpoint: "http://localhost:11434/v1"
  model: "llama2:13b"
```
The framework will use this endpoint for all test runs.

---

## 🚀 Quick Start (30‑second demo)
```python
from indoctrine-ai import Indoctrinator
from indoctrine-ai.core import AgentInterface

class MyAgent(AgentInterface):
    def send_message(self, message: str) -> str:
        # Replace with your LLM call – here we just echo
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

## 📖 Why This Product?
The rapid proliferation of powerful LLM‑driven agents brings unprecedented benefits **and** novel risks. Traditional testing tools focus on isolated model metrics (e.g., perplexity) but ignore the *[...]
- **Prompt‑injection attacks** where an adversary manipulates the agent’s internal reasoning.
- **Hallucinations** that propagate through multi‑step workflows, leading to unsafe decisions.
- **Regulatory non‑compliance** with emerging standards such as the EU AI Act, NIST AI RMF, and GDPR.
- **Cultural bias** where models reinforce Western‑centric viewpoints, marginalising other perspectives.

**Agent Indoctrination** addresses these gaps by providing a **single, unified framework** that evaluates agents across three orthogonal dimensions:
1. **Attack Surface** – Simulated adversarial prompts, jailbreaks, and token‑smuggling.
2. **Truthfulness** – Groundedness, consistency, and context‑adherence across multi‑turn dialogues.
3. **Governance & Bias** – Automated compliance checks against legal frameworks and a novel **Decolonization Score** that quantifies bias across epistemic, linguistic, historical, cultural, and ster[...]

By surfacing these metrics in a single report, teams can **prioritise remediation**, demonstrate compliance to auditors, and build trust with stakeholders.

---

## 📊 What Does It Test?
### Attack Layer
- **Prompt Injection** – Inserts malicious instructions into user prompts.
- **Jailbreak Detection** – Attempts to bypass safety guards.
- **Token‑Smuggling** – Exploits tokenisation quirks to hide malicious intent.
- **Multi‑Turn Crescendo** – Gradually escalates attacks over a conversation.
- **Custom Adversarial Scenarios** – Users can plug‑in their own attack scripts.

### Truth Layer
- **Groundedness** – Checks if responses are supported by supplied knowledge bases.
- **Consistency** – Verifies that the agent gives the same answer to semantically equivalent queries.
- **Hallucination Detection** – Flags statements not present in any reference data.
- **Context‑Adherence** – Measures how well the agent stays within the provided context.
- **3‑D Embedding Failure Maps** – Visualises clusters of erroneous responses.

### Governance Layer
- **EU AI Act** – Automated checks for Articles 9‑15 & 52 compliance.
- **NIST AI RMF** – Maps test results to the NIST risk management framework.
- **GDPR, SOC2, ISO 42001** – Verifies data‑handling and security controls.
- **Custom Policy Engine** – Allows organisations to encode internal policies.

### Colonization Layer (Bias Testing)
- **Epistemic Bias** – Over‑reliance on Western knowledge sources.
- **Linguistic Bias** – Preference for English‑centric phrasing.
- **Historical Bias** – Skewed representation of non‑Western events.
- **Cultural Bias** – Assumptions about norms and values.
- **Stereotyping** – Propagation of harmful stereotypes.
The **Decolonization Score** aggregates these dimensions into a 0‑100 rating, where higher scores indicate lower bias.

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

> **Your one‑stop, open‑source solution for rigorous AI agent evaluation** – from prompt‑injection attacks to EU AI Act compliance, with a **Decolonization Score** that quantifies Western‑ce[...]

---

## �🛡️ Core Value Proposition
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
pip install agent_indoctrination

# Optional extras for attack engines (PyRIT, Giskard)
pip install "agent_indoctrination[attack]"
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

---


**Made with ❤️ for safer, unbiased, and compliant AI**
