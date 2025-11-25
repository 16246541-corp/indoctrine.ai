# Documentation

Welcome to the Agent Indoctrination documentation.

---

## Quick Links

- **[Getting Started](getting-started.md)** - Get up and running in 5 minutes
- **[Configuration](configuration.md)** - Complete configuration reference
- **[Testing Engines](testing-engines.md)** - Deep dive into all5 testing capabilities
- **[Examples](examples.md)** - Real-world usage patterns
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

---

## Documentation Structure

### For New Users

1. **[Getting Started](getting-started.md)**
   - Installation
   - Your first test
   - Understanding results
   - Common issues

2. **[Examples](examples.md)**
   - Testing chatbots
   - Testing RAG systems
   - Testing tool-using agents
   - CI/CD integration

### For Configuration

3. **[Configuration Guide](configuration.md)**
   - LLM provider setup (OpenAI, Anthropic, Ollama, LM Studio)
   - Testing engine configuration
   - Threshold settings
   - Environment variables

### For Deep Understanding

4. **[Testing Engines](testing-engines.md)**
   - Attack Engine - Security testing
   - Truth Engine - Accuracy & hallucination detection
   - Governance Engine - Compliance & policy
   - Fairness Engine - Bias & discrimination testing
   - Values Engine - Cultural bias & ethics

### For Troubleshooting

5. **[Troubleshooting](troubleshooting.md)**
   - Installation issues
   - Configuration errors
   - Runtime problems
   - Performance optimization
   - Error message reference

### Advanced Topics

6. **[Best Practices](best-practices.md)**
   - Test suite structuring
   - Threshold selection
   - Performance optimization
   - CI/CD patterns

7. **[Advanced Topics](advanced-topics.md)**
   - Observability & tracing
   - Synthetic data generation
   - Custom engines
   - Distributed testing

8. **[API Reference](api-reference.md)**
   - Core classes
   - Testing engine APIs
   - Configuration objects
   - Utility functions

---

## Common Tasks

### Installation
```bash
pip install indoctrine-ai
```
→ See [Getting Started - Installation](getting-started.md#installation)

### First Test
```python
from agent_indoctrination import Indoctrinator
indo = Indoctrinator("config.yaml")
results = indo.run_full_suite(my_agent)
```
→ See [Getting Started - Your First Test](getting-started.md#your-first-test-3-minutes)

### Configure LLM Provider
```yaml
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"
```
→ See [Configuration - LLM Providers](configuration.md#llm-provider-configuration)

### Test Specific Engine
```python
attack_results = indo.run_attack_tests(agent)
```
→ See [Testing Engines](testing-engines.md) and [Examples](examples.md)

### Fix Configuration Error
→ See [Troubleshooting - Configuration Errors](troubleshooting.md#configuration-errors)

### Optimize Performance
→ See [Troubleshooting - Performance Issues](troubleshooting.md#performance-issues)

---

## Getting Help

- **GitHub Issues:** https://github.com/16246541-corp/indoctrine.ai/issues
- **Discussions:** https://github.com/16246541-corp/indoctrine.ai/discussions
- **Examples:** https://github.com/16246541-corp/indoctrine.ai/tree/main/examples

---

## Contributing

Want to improve the documentation? See [Contributing Guide](https://github.com/16246541-corp/indoctrine.ai/blob/main/CONTRIBUTING.md).
