# Getting Started

Get up and running with Agent Indoctrination in under 5 minutes.

---

## Prerequisites

- **Python 3.9+**
- **pip** package manager
- **API key** (optional): OpenAI or Anthropic for LLM-as-a-Judge, or use local LLMs

---

## Installation

### Option 1: PyPI (Recommended)

```bash
# Basic installation
pip install indoctrine-ai

# With attack engine extras
pip install "indoctrine-ai[attack]"

# Install all extras
pip install "indoctrine-ai[all]"
```

### Option 2: From Source

```bash
git clone https://github.com/16246541-corp/indoctrine.ai.git
cd indoctrine.ai
pip install -e .
```

### Option 3: Docker

```bash
docker pull indoctrine/indoctrine-ai:latest
docker run -it indoctrine/indoctrine-ai:latest
```

---

## Verify Installation

```bash
# Check version
python -c "import agent_indoctrination; print(agent_indoctrination.__version__)"

# Run help
indoctrinate --help
```

---

## Your First Test (3 Minutes)

### Step 1: Create Configuration

Create `config.yaml`:

```yaml
# config.yaml
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"

attack:
  enabled: true
truth:
  enabled: true
governance:
  enabled: true
```

Set your API key:
```bash
export OPENAI_API_KEY="sk-..."
```

### Step 2: Create Test Agent

Create `my_agent.py`:

```python
from agent_indoctrination.core import AgentInterface

class MyAgent(AgentInterface):
    """Simple test agent."""
    
    def send_message(self, message: str) -> str:
        """Process message and return response."""
        # Replace this with your actual LLM call
        message_lower = message.lower()
        
        # Basic responses
        if "hello" in message_lower or "hi" in message_lower:
            return "Hello! How can I help you today?"
        
        if "2+2" in message or "2 + 2" in message:
            return "4"
        
        # Safety check
        harmful_keywords = ["hack", "bypass", "illegal"]
        if any(word in message_lower for word in harmful_keywords):
            return "I cannot help with that request."
        
        return "I understand. Could you please provide more details?"

if __name__ == "__main__":
    agent = MyAgent()
    print(agent.send_message("Hello!"))
```

### Step 3: Run Tests

```python
# test_my_agent.py
from agent_indoctrination import Indoctrinator
from my_agent import MyAgent

# Initialize framework
indo = Indoctrinator(config_path="config.yaml")

# Create agent instance
agent = MyAgent()

# Run full test suite
results = indo.run_full_suite(agent)

# Generate report
indo.generate_report(results, output_path="report.pdf")

print("✅ Testing complete! Check report.pdf for results.")
```

Run the test:
```bash
python test_my_agent.py
```

**Expected output:**
```
🌈 Running Agent Indoctrination Tests...
[████████████████████] 100% Complete

✅ Attack Engine: PASSED (robustness_score: 95/100)
✅ Truth Engine: PASSED (truthfulness_score: 88/100)
✅ Governance Engine: PASSED (compliance_score: 92/100)

✅ Testing complete! Check report.pdf for results.
```

---

## Understanding the Results

### Report Structure

Your `report.pdf` contains:

1. **Executive Summary**
   - Overall Nyan Alignment Score
   - Pass/Fail status per engine
   - Critical issues highlighted

2. **Attack Results**
   - Robustness score
   - Successful attacks (if any)
   - Vulnerability breakdown

3. **Truth Results**
   - Truthfulness score
   - Hallucination rate
   - Groundedness metrics

4. **Governance Results**
   - Compliance score
   - Framework-specific results
   - Violations (if any)

5. **Benchmarks**
   - 7-dimensional ethical scores
   - Comparative charts
   - Recommendations

### Understanding Scores

**Nyan Alignment Score (0-100):**
- **85-100:** Excellent - Production ready
- **70-84:** Good - Minor improvements needed
- **50-69:** Moderate - Significant gaps
- **Below 50:** Poor - Major issues

**Per-Engine Scores:**
- **Robustness (Attack):** Higher = more resistant to attacks
- **Truthfulness (Truth):** Higher = more accurate
- **Compliance (Governance):** Higher = better regulatory adherence
- **Fairness:** Higher = less biased
- **Values Alignment:** Higher = more ethical

---

## Common First-Time Issues

### Issue: API Key Error

**Error:** `ValueError: API key is required`

**Solution:**
```bash
# Check if key is set
echo $OPENAI_API_KEY

# Set it correctly
export OPENAI_API_KEY="sk-your-actual-key"
```

### Issue: Agent Not Responding

**Error:** `Agent did not respond within timeout`

**Solution:**
```yaml
# Increase timeout in config
agent:
  timeout: 120  # seconds
```

### Issue: Tests Too Slow

**Solution:**
```yaml
# Reduce test load
attack:
  max_attempts: 10  # Instead of 50
```

---

## Using Local LLMs (No API Key Needed)

### With Ollama

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3

# Start server (auto-starts on install)
ollama serve
```

Update `config.yaml`:
```yaml
evaluator:
  provider: "openai"  # Ollama is OpenAI-compatible
  endpoint: "http://localhost:11434/v1"
  model: "llama3"
  api_key: "ollama"  # Required but ignored
```

### With LM Studio

1. Download LM Studio from https://lmstudio.ai
2. Load a model (e.g., Llama 3)
3. Start local server (default port: 1234)

Update `config.yaml`:
```yaml
evaluator:
  provider: "openai"
  endpoint: "http://localhost:1234/v1"
  model: "local-model"
  api_key: "lm-studio"
```

---

## CLI Usage

### Initialize New Project

```bash
# Create config file
indoctrinate init --output config.yaml

# Create sample agent
indoctrinate init --agent my_agent.py
```

### Run Tests

```bash
# Run full suite
indoctrinate run --config config.yaml --agent my_agent.py

# Run specific engine
indoctrinate run --config config.yaml --agent my_agent.py --engine attack

# Run with nyan progress
indoctrinate run --config config.yaml --agent my_agent.py --nyan
```

### Generate Reports

```bash
# Generate PDF
indoctrinate report --input results.json --output report.pdf --format pdf

# Generate markdown
indoctrinate report --input results.json --output report.md --format markdown
```

### Validate Configuration

```bash
# Check config validity
indoctrinate validate --config config.yaml
```

---

## Python API Examples

### Basic Usage

```python
from agent_indoctrination import Indoctrinator
from my_agent import MyAgent

indo = Indoctrinator("config.yaml")
agent = MyAgent()

# Run tests
results = indo.run_full_suite(agent)

# Generate report
indo.generate_report(results, output_path="report.pdf")
```

### Run Specific Engines

```python
# Run only attack tests
attack_results = indo.run_attack_tests(agent)

# Run only truth tests
truth_results = indo.run_truth_tests(agent)

# Run only governance tests
governance_results = indo.run_governance_tests(agent)
```

### Custom Thresholds

```python
results = indo.run_full_suite(
    agent,
    thresholds={
        'robustness_min': 90,
        'truthfulness_min': 85,
        'compliance_min': 95
    }
)

if results['passed']:
    print("✅ All thresholds met!")
else:
    print("❌ Failed:", results['failed_checks'])
```

### Parallel Execution

```python
results = indo.run_full_suite(
    agent,
    parallel=True,
    workers=4
)
```

---

## Next Steps

Now that you have your first test running, explore:

1. **[Configuration Guide](configuration.md)** - Customize testing parameters
2. **[Testing Engines](testing-engines.md)** - Deep dive into what each engine tests
3. **[Examples](examples.md)** - Real-world usage patterns
4. **[Best Practices](best-practices.md)** - Optimize your testing workflow

---

## Quick Reference

### Essential Commands

```bash
# Install
pip install indoctrine-ai

# Initialize
indoctrinate init

# Run tests
indoctrinate run --config config.yaml --agent my_agent.py

# Generate report
indoctrinate report --input results.json --output report.pdf
```

### Essential Python API

```python
from agent_indoctrination import Indoctrinator

indo = Indoctrinator("config.yaml")
results = indo.run_full_suite(agent)
indo.generate_report(results, "report.pdf")
```

### Essential Config

```yaml
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"

attack:
  enabled: true
truth:
  enabled: true
governance:
  enabled: true
```

---

## Getting Help

- **Documentation:** https://indoctrine.ai/docs
- **GitHub Issues:** https://github.com/16246541-corp/indoctrine.ai/issues
- **Discussions:** https://github.com/16246541-corp/indoctrine.ai/discussions
- **Examples:** https://github.com/16246541-corp/indoctrine.ai/tree/main/examples
