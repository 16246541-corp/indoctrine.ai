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

#### ✅ Truth Engine
- Groundedness validation against context
- Multi-turn consistency checking
- Hallucination detection
- Response accuracy metrics

#### ⚖️ Governance Engine
- EU AI Act compliance (Articles 9, 10, 52)
- NIST AI Risk Management Framework
- GDPR, CCPA, HIPAA data privacy checks
- Customizable policy framework

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
- Embedding-based analysis not yet implemented
- Async execution mode planned for future release

### Roadmap

- Enhanced multi-modal testing
- Real-time monitoring dashboard
- Expanded compliance framework coverage
- Performance optimizations

---

**Repository**: https://github.com/16246541-corp/agent-indoctrination  
**Issues**: https://github.com/16246541-corp/agent-indoctrination/issues
