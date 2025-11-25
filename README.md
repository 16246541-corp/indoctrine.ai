# indoctrine.ai

**The Gold Standard for AI Testing: Ethical, Fair, and Compliant**

[![PyPI version](https://badge.fury.io/py/indoctrine-ai.svg)](https://badge.fury.io/py/indoctrine-ai)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

**Open-source AI testing framework** for comprehensive security, bias detection, compliance, and ethical AI evaluation. Production-ready testing for LLMs and AI agents.

---

## What Does indoctrine.ai Test?

### 🔐 AI Security & Robustness
**Detect vulnerabilities before attackers do.**
- **Prompt injection attacks** - Block instruction override attempts
- **Jailbreak detection** - Prevent safety guideline bypasses  
- **Adaptive red-teaming** - AI-powered dynamic attack generation
- **Multi-modal security** - Test image injection and visual jailbreaks
- **Tool use safety** - Validate agent tool-calling security
- **Token smuggling** - Detect encoding-based attacks

→ See [Attack Engine Documentation](docs/testing-engines.md#1-attack-engine)

### ✅ AI Truthfulness & Accuracy
**Eliminate hallucinations and ensure factual accuracy.**
- **Hallucination detection** - Identify fabricated information
- **Groundedness checking** - Verify claims match source material
- **RAG system evaluation** - Full RAG Triad (Context, Groundedness, Answer Relevance)
- **Consistency testing** - Ensure reliable responses
- **Semantic similarity** - Real embedding-based analysis

→ See [Truth Engine Documentation](docs/testing-engines.md#2-truth-engine)

### ⚖️ AI Compliance & Governance
**Meet regulatory requirements automatically.**
- **EU AI Act compliance** - Articles 9-15 & 52 coverage
- **GDPR compliance** - Data privacy and protection
- **NIST AI RMF** - Risk management framework
- **SOC 2 & ISO 42001** - Enterprise standards
- **Auto-generated guardrails** - Export NeMo Guardrails configs
- **Custom policy engine** - Enforce company-specific rules

→ See [Governance Engine Documentation](docs/testing-engines.md#3-governance-engine)

### ⚖️ AI Fairness & Bias Detection
**Eliminate algorithmic discrimination with research-backed metrics.**
- **15 fairness metrics** - Demographic parity, equalized odds, disparate impact
- **Standard benchmarks** - Adult, COMPAS, German Credit datasets
- **LLM-native testing** - Auto-generate demographic variants
- **Interpretability layer** - Plain-English bias explanations
- **Legal compliance** - EEOC 80% rule validation
- **Hiring & lending testing** - Domain-specific thresholds

→ See [Fairness Engine Documentation](docs/testing-engines.md#4-fairness-engine)

### 🌍 AI Ethics & Cultural Equity
**Test for cultural bias and value alignment.**
- **Decolonization score** - 5-dimensional cultural bias testing
  - Epistemic bias (knowledge systems)
  - Linguistic bias (communication styles)
  - Historical bias (narrative perspectives)
  - Cultural bias (norm assumptions)
  - Stereotyping (representation quality)
- **Political bias detection** - Measure ideological skew
- **Values alignment** - Human rights, ethics, inclusivity

→ See [Values Engine Documentation](docs/testing-engines.md#5-values-engine)

---

## How Does indoctrine.ai Test?

### 🤖 LLM-as-a-Judge Evaluation
**Sophisticated AI-powered testing, not brittle keyword matching.**

- Uses GPT-4, Claude, or local LLMs (Ollama, LM Studio) as evaluators
- Contextual understanding of refusals vs. compliance
- Nuanced detection of hallucinations and policy violations
- Supports OpenAI, Anthropic, or fully offline local models

```yaml
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"
```

### ⚔️ Adaptive Red-Teaming
**Dynamic attacks that evolve based on your agent's responses.**

- **Attacker Agent** observes target responses
- Generates new exploits targeting discovered weaknesses  
- Multi-turn interrogation vs. static attack datasets
- Powered by GPT-4, Claude, or local LLMs

### 📊 Objective Fairness Metrics
**Research-backed algorithmic fairness testing.**

- 15 peer-reviewed fairness metrics
- Formal mathematical definitions
- Industry-standard benchmarks (Adult, COMPAS, German Credit)
- Interpretability layer with plain-English explanations

### 🎯 Multi-Modal Testing
**Test both text and vision-language models.**

- Image injection attacks
- QR code exploits
- Steganography detection
- Visual jailbreak testing

### 🌈 Beautiful UX
**AI testing that doesn't feel like a chore.**

- **Nyan Progress Display** - Rainbow-trailing progress animations
- **Nyan Alignment Score** - Unified 0-100 ethical metric
- Automated PDF/JSON/Markdown reports
- 3D embedding visualizations

---

## Why indoctrine.ai?

### ✨ Key Differentiators

| Feature | indoctrine.ai | Alternatives |
|---------|---------------|--------------|
| **Open Source** | ✅ MIT License | ❌ Proprietary |
| **Privacy-First** | ✅ Runs locally | ❌ Cloud-only |
| **Comprehensive** | ✅ 5-layer testing | ⚠️ Partial coverage |
| **Production-Ready** | ✅ CI/CD integration | ⚠️ Research tools |
| **Research-Backed** | ✅ 15 fairness metrics | ⚠️ Ad-hoc metrics |
| **Cultural Equity** | ✅ Decolonization testing | ❌ Not available |
| **Auto-Remediation** | ✅ Guardrail export | ❌ Detection only |

---

## Quick Start

### Installation
```bash
pip install indoctrine-ai
```

### Your First Test (5 Lines)
```python
from agent_indoctrination import Indoctrinator

indo = Indoctrinator("config.yaml")
results = indo.run_full_suite(my_agent)
indo.generate_report(results, "report.pdf")
print(f"Nyan Alignment Score: {results['overall_score']}/100")
```

**Output:**
```
🌈 [████████████████████] 100% Complete
✅ Security: 92/100 | ✅ Accuracy: 88/100 | ✅ Compliance: 95/100
Nyan Alignment Score: 91/100
```

→ **[Get Started in 5 Minutes](docs/getting-started.md)**

---

## Who Uses indoctrine.ai?

### Use Cases

| Industry | What We Test | Why It Matters |
|----------|--------------|----------------|
| **AI/ML Teams** | Security, hallucinations, consistency | Catch bugs before production |
| **Compliance Officers** | EU AI Act, GDPR, SOC 2 | Automated regulatory audits |
| **Red Teams** | Adversarial attacks, jailbreaks | Identify security vulnerabilities |
| **HR/Hiring** | Fairness metrics, bias detection | Avoid discrimination lawsuits |
| **Finance/Lending** | Disparate impact, EEOC compliance | Fair lending requirements |
| **Healthcare** | HIPAA, bias, hallucinations | Patient safety & equity |
| **Enterprise AI** | Governance, security, fairness | Comprehensive AI risk management |

---

## Documentation

### 📚 Complete Guides

- **[Getting Started](docs/getting-started.md)** - Install and run your first test in 5 minutes
- **[Configuration](docs/configuration.md)** - Complete configuration reference
- **[Testing Engines](docs/testing-engines.md)** - Deep dive into all 5 testing capabilities
- **[Examples](docs/examples.md)** - Real-world usage patterns (RAG, tools, CI/CD)
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[Best Practices](docs/best-practices.md)** - Optimization and workflow guidelines
- **[Advanced Topics](docs/advanced-topics.md)** - Observability, distributed testing, custom engines

### 🎯 Quick Links

- [Installation Guide](docs/getting-started.md#installation)
- [First Test Tutorial](docs/getting-started.md#your-first-test-3-minutes)
- [LLM Provider Setup](docs/configuration.md#llm-provider-configuration)
- [CI/CD Integration](docs/examples.md#5-cicd-integration)
- [Fairness Metrics Reference](docs/testing-engines.md#41-the-15-fairness-metrics)
- [Custom Attack Development](docs/examples.md#6-custom-attack-development)

---

## Features at a Glance

### Core Capabilities
✅ Prompt injection & jailbreak detection  
✅ Adaptive AI-powered red-teaming  
✅ Multi-modal security testing (images, QR codes)  
✅ Hallucination & groundedness checking  
✅ RAG Triad evaluation (Context, Groundedness, Answer Relevance)  
✅ EU AI Act, GDPR, NIST AI RMF compliance  
✅ 15 objective fairness metrics  
✅ Decolonization testing (5 cultural dimensions)  
✅ Auto-generated guardrails (NeMo)  
✅ LLM-as-a-Judge evaluation  
✅ OpenAI, Anthropic, Ollama, LM Studio support  
✅ CI/CD integration (GitHub Actions, GitLab)  
✅ PDF/JSON/Markdown reports  
✅ Nyan Progress Display 🌈  

---

## Configuration Example

```yaml
# config.yaml - Works with OpenAI, Anthropic, or local LLMs
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"

# Or use local LLMs (free, offline)
evaluator:
  provider: "openai"
  endpoint: "http://localhost:11434/v1"
  model: "llama3"
  api_key: "ollama"

# Enable testing engines
attack:
  enabled: true
  adaptive: true  # AI-powered attacks
  
truth:
  enabled: true
  enable_rag_triad: true
  
governance:
  enabled: true
  frameworks:
    - eu_ai_act
    - gdpr
    
fairness:
  enabled: true
  use_case: "hiring"  # EEOC thresholds

values:
  enabled: true
```

→ **[Full Configuration Guide](docs/configuration.md)**

---

## CI/CD Integration

```yaml
# .github/workflows/ai-testing.yml
name: AI Safety Testing
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install indoctrine-ai
      - name: Run AI tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: indoctrinate run --config config.yaml --agent my_agent.py
      - name: Check thresholds
        run: indoctrinate validate --results results.json --fail-on-critical
```

→ **[CI/CD Examples](docs/examples.md#5-cicd-integration)**

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Community
- 🐛 **Report bugs** - [GitHub Issues](https://github.com/16246541-corp/indoctrine.ai/issues)
- 💡 **Suggest features** - [Discussions](https://github.com/16246541-corp/indoctrine.ai/discussions)
- 🔀 **Submit PRs** - Follow the `dev` branch workflow
- ⭐ **Star the repo** - Help us reach more AI developers!

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- **Documentation**: [docs/](docs/)
- **GitHub Issues**: https://github.com/16246541-corp/indoctrine.ai/issues
- **Discussions**: https://github.com/16246541-corp/indoctrine.ai/discussions

---

**Built for safer, fairer, and more compliant AI** 🌈
