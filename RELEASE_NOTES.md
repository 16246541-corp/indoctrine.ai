# Release Notes - v0.1.0

## Agent Indoctrination Framework - Initial Release

### Overview

First public release of the Agent Indoctrination framework - an open-source tool for comprehensive AI agent testing across security, truthfulness, and regulatory compliance dimensions.

### Features

#### 🔐 Attack Engine
- Prompt injection testing with multiple strategies
- Jailbreak attempt detection
- Token smuggling and encoding attack tests
- Crescendo multi-turn escalation attacks
- CVSS-based vulnerability scoring
- Optional PyRIT and Giskard integrations
- **Adaptive Red-Teaming**: New "Attacker Agent" that dynamically generates attack prompts using LLMs (OpenAI, Anthropic, or Local) to exploit target weaknesses.
- **Adaptive Crescendo**: Multi-turn attack strategy that evolves based on target responses.
- **Tool Use Security**: New attack module to test for tool injection vulnerabilities and sensitive output leakage.

#### 🖼️ Multi-Modal Support
- **Message Dataclass**: Updated core `Message` object to support image payloads (base64/URL) and audio.
- **Image Injection Attack**: New attack engine to test for visual jailbreaks in VLMs.
- **Agent Interface Update**: Agents can now receive structured `Message` objects containing multi-modal data.

#### ✅ Truth Engine
- Groundedness validation against context
- Multi-turn consistency checking
- Hallucination detection
- Response accuracy metrics
- **RAG Triad Evaluation**: Full support for Context Relevance, Groundedness, and Answer Relevance checks.
- **RAG Score**: Composite score for RAG system performance.
- **Semantic Similarity**: Real cosine similarity checks using `sentence-transformers` embeddings.
- **Embedding Visualization**: 3D PCA plots of response vectors for cluster analysis.

#### ⚖️ Governance Engine
- EU AI Act compliance (Articles 9, 10, 52)
- NIST AI Risk Management Framework
- GDPR, CCPA, HIPAA data privacy checks
- Customizable policy framework
- **Guardrail Export**: Automatically generates NeMo Guardrails configuration files (`config.yml`, `prompts.co`) when Data Privacy violations are detected.
- **Auto-Remediation Loop**: New orchestration logic that re-tests the agent with the generated guardrails to verify the fix immediately.

#### 🧪 Synthetic Data Generation
- **GoldenDataset**: New class for managing regression test cases.
- **SyntheticDataGenerator**: Automatically generates adversarial prompts using LLMs based on agent descriptions.
- **Auto-Population**: Populate datasets with 100+ test cases in seconds.

#### 📊 Reporting & Benchmarking
- 7-dimension ethical benchmarks (Safety, Fairness, Robustness, Transparency, Privacy, Accountability, Truthfulness)
- Markdown and JSON report generation
- Comprehensive test result analysis

#### 🛠️ Developer Experience
- Simple Python SDK
- CLI interface (`indoctrinate` command)
- YAML/JSON configuration
- HTTP and Python agent support
- Extensible plugin architecture

### Installation

```bash
pip install agent-indoctrination
```

### Quick Start

```python
from agent_indoctrination import Indoctrinator
from agent_indoctrination.core.agent import HTTPAgent

agent = HTTPAgent(endpoint="http://localhost:8000/chat")
indoc = Indoctrinator(config_path="config.yaml")
results = indoc.run_full_suite(agent)
report = indoc.generate_report(results)
```

### Documentation

- Comprehensive quickstart guide
- Configuration examples
- API documentation
- Compliance framework guides

### Requirements

- Python 3.10+
- Core dependencies: pydantic, pyyaml, requests, click, rich

### License

MIT License

### Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.

### Known Limitations

- PDF report generation placeholder (requires reportlab implementation)
- Async execution mode planned for future release

### Roadmap

- Enhanced multi-modal testing
- Real-time monitoring dashboard
- Expanded compliance framework coverage
- Performance optimizations

---

**Repository**: https://github.com/16246541-corp/agent-indoctrination  
**Issues**: https://github.com/16246541-corp/agent-indoctrination/issues
