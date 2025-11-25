# Troubleshooting Guide

Common issues and solutions for using the Agent Indoctrination framework.

---

## Installation Issues

### Dependency Conflicts

**Error:** `ERROR: Cannot install indoctrine-ai because these package versions have conflicts`

**Solution:**
```bash
# Create a fresh virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with specific Python version
python3.11 -m pip install indoctrine-ai
```

### Python Version Mismatch

**Error:** `indoctrine-ai requires Python >=3.9`

**Solution:**
- Check your Python version: `python --version`
- Install Python 3.9+ from [python.org](https://python.org)
- Use pyenv to manage multiple Python versions:
  ```bash
  pyenv install 3.11
  pyenv local 3.11
  ```

### Optional Extras Not Installing

**Error:** `ModuleNotFoundError: No module named 'pyrit'`

**Solution:**
```bash
# Install attack extras explicitly
pip install "indoctrine-ai[attack]"

# Or install all extras
pip install "indoctrine-ai[all]"
```

### Platform-Specific Issues

**macOS M1/M2 ARM Issues:**
```bash
# Install architecture-specific wheels
arch -arm64 pip install indoctrine-ai
```

**Windows Long Path Issues:**
```powershell
# Enable long paths in Windows
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

---

## Configuration Errors

### Invalid YAML Syntax

**Error:** `yaml.scanner.ScannerError: mapping values are not allowed here`

**Solution:**
- Ensure proper YAML indentation (use spaces, not tabs)
- Quote strings containing special characters:
  ```yaml
  # Wrong
  endpoint: http://localhost:1234/v1
  
  # Correct
  endpoint: "http://localhost:1234/v1"
  ```

### Missing API Keys

**Error:** `ValueError: API key is required for provider 'openai'`

**Solutions:**

**Option 1 - Environment Variable:**
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Option 2 - Config File:**
```yaml
evaluator:
  provider: "openai"
  api_key: "${OPENAI_API_KEY}"  # Reads from env
```

**Option 3 - Direct (Not Recommended for Production):**
```yaml
evaluator:
  provider: "openai"
  api_key: "sk-..."  # Never commit this!
```

### Endpoint Connection Failures

**Error:** `Connection refused: http://localhost:11434`

**Diagnosis:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check if LM Studio is running
curl http://localhost:1234/v1/models
```

**Solutions:**

**Ollama Not Running:**
```bash
# Start Ollama
ollama serve

# Pull a model
ollama pull llama3
```

**LM Studio Not Running:**
1. Open LM Studio application
2. Load a model
3. Start the local server (default port: 1234)
4. Verify endpoint in config matches server port

**Wrong Port:**
```yaml
# Ollama default
endpoint: "http://localhost:11434/v1"

# LM Studio default
endpoint: "http://localhost:1234/v1"
```

### Model Not Found

**Error:** `InvalidRequestError: The model 'gpt-5' does not exist`

**Solution:**
```yaml
# Use valid model names
evaluator:
  provider: "openai"
  model: "gpt-4o"  # Valid OpenAI model
  
# For local models, use exact name from Ollama/LM Studio
evaluator:
  provider: "openai"
  endpoint: "http://localhost:11434/v1"
  model: "llama3"  # Must match: ollama list
```

### Provider Authentication Errors

**Error:** `AuthenticationError: Incorrect API key provided`

**Solution:**
1. Verify API key is correct: `echo $OPENAI_API_KEY`
2. Check for trailing spaces: `export OPENAI_API_KEY=$(echo $OPENAI_API_KEY | tr -d '[:space:]')`
3. Regenerate API key from provider dashboard

---

## Runtime Errors

### Agent Timeout Errors

**Error:** `TimeoutError: Agent did not respond within 30 seconds`

**Solution:**
```yaml
# Increase timeout in config
agent:
  timeout: 120  # seconds
  
# Or programmatically
agent = MyAgent(timeout=120)
```

### Memory Issues with Large Tests

**Error:** `MemoryError: Unable to allocate array`

**Solutions:**

**Reduce Batch Size:**
```yaml
attack:
  max_attempts: 10  # Reduce from 50
  batch_size: 5     # Process in smaller batches
```

**Run Tests Incrementally:**
```python
# Run one engine at a time
results = {}
results['attack'] = indo.run_attack_tests(agent)
results['truth'] = indo.run_truth_tests(agent)
results['governance'] = indo.run_governance_tests(agent)
```

**Disable Visualization:**
```yaml
reporting:
  generate_visualizations: false
  generate_embeddings: false
```

### Rate Limiting (OpenAI, Anthropic)

**Error:** `RateLimitError: Rate limit exceeded`

**Solutions:**

**Add Delays:**
```yaml
evaluator:
  rate_limit_delay: 1.0  # seconds between requests
  max_retries: 5
  retry_delay: 2.0
```

**Use Local LLM for High-Volume Testing:**
```yaml
evaluator:
  provider: "openai"
  endpoint: "http://localhost:11434/v1"  # Ollama
  model: "llama3"
  api_key: "ollama"
```

**Batch Requests:**
```python
# Process in smaller batches
indo.run_full_suite(agent, batch_size=10, delay=1.0)
```

### JSON Parsing Failures

**Error:** `JSONDecodeError: Expecting value: line 1 column 1`

**Common Causes:**
1. LLM returned non-JSON format
2. Network response was HTML error page
3. Empty response from agent

**Solutions:**
```python
# Enable debug logging to see raw responses
import logging
logging.basicConfig(level=logging.DEBUG)

# Add response validation
from agent_indoctrination.core.agent import AgentInterface

class MyAgent(AgentInterface):
    def send_message(self, message: str) -> str:
        response = self.llm.generate(message)
        if not response or not isinstance(response, str):
            raise ValueError(f"Invalid response: {response}")
        return response
```

### Embedding Generation Failures

**Error:** `RuntimeError: Failed to generate embeddings`

**Solution:**
```bash
# Install sentence-transformers
pip install sentence-transformers

# Or disable embeddings
```

```yaml
truth:
  enable_embeddings: false
  enable_semantic_similarity: false
```

---

## Testing Failures

### Agent Not Responding Correctly

**Issue:** Agent returns same response for all queries

**Diagnosis:**
```python
# Test agent directly
agent = MyAgent()
print(agent.send_message("Hello"))
print(agent.send_message("What is 2+2?"))
```

**Solutions:**
1. Verify agent is stateless (not caching responses)
2. Check if agent is properly initialized
3. Ensure agent calls LLM for each request

### Unexpected Test Results

**Issue:** Tests passing/failing unexpectedly

**Debug Steps:**
```python
# Enable verbose output
indo = Indoctrinator(config_path="config.yaml", log_level="DEBUG")

# Run single test engine
results = indo.orchestrator.attack_engine.run(agent)
print(results)

# Check thresholds
print(indo.config.attack.max_attempts)
print(indo.config.governance.frameworks)
```

### Report Generation Errors

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'report.pdf'`

**Solution:**
```python
# Ensure output directory exists
import os
os.makedirs("reports", exist_ok=True)

# Generate with absolute path
indo.generate_report(results, output_path="./reports/report.pdf")
```

### PDF Generation Issues

**Error:** `OSError: cannot load library 'gobject-2.0-0'`

**Solution (Linux):**
```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
sudo apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0
```

**Solution (macOS):**
```bash
brew install cairo pango gdk-pixbuf libffi
```

**Fallback - Use Markdown/JSON Instead:**
```python
# Generate markdown instead
indo.generate_report(results, format="markdown", output_path="report.md")
```

### Visualization Errors

**Error:** `ImportError: No module named 'plotly'`

**Solution:**
```bash
pip install plotly kaleido
```

---

## Performance Issues

### Slow Test Execution

**Causes & Solutions:**

**1. Too Many Attack Attempts:**
```yaml
attack:
  max_attempts: 10  # Reduce from 50
```

**2. Slow LLM Provider:**
```yaml
# Use faster model
evaluator:
  model: "gpt-3.5-turbo"  # Instead of gpt-4o
```

**3. Enable Parallel Execution:**
```python
indo.run_full_suite(agent, parallel=True, workers=4)
```

### High Memory Usage

**Solutions:**

**1. Disable Visualization:**
```yaml
reporting:
  generate_visualizations: false
```

**2. Stream Results:**
```python
# Process results incrementally
for engine_name, engine_results in indo.run_suite_streaming(agent):
    process_results(engine_results)
```

**3. Clear Cache:**
```python
# Clear embedding cache
import shutil
shutil.rmtree(".cache/embeddings", ignore_errors=True)
```

### Timeout During Adaptive Attacks

**Error:** `TimeoutError: Adaptive attack exceeded maximum time`

**Solution:**
```yaml
attack:
  adaptive:
    max_iterations: 3      # Reduce from 5
    timeout_per_iteration: 30  # seconds
    early_stopping: true
```

### Token Limit Exceeded

**Error:** `InvalidRequestError: This model's maximum context length is 8192 tokens`

**Solutions:**

**1. Truncate Long Prompts:**
```yaml
attack:
  max_prompt_length: 4000  # tokens
```

**2. Use Model with Larger Context:**
```yaml
evaluator:
  model: "gpt-4-turbo-preview"  # 128k context
```

**3. Chunk Long Tests:**
```python
# Split test cases into chunks
for chunk in chunks(test_cases, size=10):
    results = indo.run_tests(agent, test_cases=chunk)
```

---

## Common Error Messages

### `AttributeError: 'NoneType' object has no attribute 'send_message'`

**Cause:** Agent not properly initialized

**Solution:**
```python
# Ensure agent inherits from AgentInterface
from agent_indoctrination.core import AgentInterface

class MyAgent(AgentInterface):
    def send_message(self, message: str) -> str:
        return self.llm.generate(message)

# Initialize before use
agent = MyAgent()
results = indo.run_full_suite(agent)
```

### `ValueError: Config file not found: config.yaml`

**Solution:**
```bash
# Check current directory
ls config.yaml

# Use absolute path
indo = Indoctrinator(config_path="/absolute/path/to/config.yaml")

# Or create default config
indoctrinate init --output config.yaml
```

### `KeyError: 'evaluator'`

**Cause:** Missing required config section

**Solution:**
```yaml
# Add required evaluator config
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"
```

### `TypeError: run_full_suite() got an unexpected keyword argument`

**Cause:** Using outdated API

**Solution:**
```bash
# Update to latest version
pip install --upgrade indoctrine-ai

# Check version
python -c "import agent_indoctrination; print(agent_indoctrination.__version__)"
```

---

## Exit Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 0 | Success | - |
| 1 | General error | Check logs for details |
| 2 | Configuration error | Validate config.yaml |
| 3 | Agent error | Test agent independently |
| 4 | Network error | Check internet/endpoints |
| 5 | Authentication error | Verify API keys |
| 6 | Timeout | Increase timeout values |
| 7 | Resource error | Reduce batch size/memory usage |

---

## Log Interpretation

### Understanding Log Levels

**DEBUG:** Detailed diagnostic information
```
DEBUG:agent_indoctrination.attack:Running prompt injection test 1/50
```

**INFO:** Confirmation that things are working
```
INFO:agent_indoctrination:Attack engine completed: robustness_score=100.0
```

**WARNING:** Something unexpected but recoverable
```
WARNING:agent_indoctrination.truth:Embedding generation failed, using keyword matching
```

**ERROR:** Something failed
```
ERROR:agent_indoctrination.governance:EU AI Act check failed: Article 9 violation
```

**CRITICAL:** Severe error, testing cannot continue
```
CRITICAL:agent_indoctrination:Agent crashed: ConnectionError
```

---

## Getting Help

If you're still experiencing issues:

1. **Search GitHub Issues:** https://github.com/16246541-corp/indoctrine.ai/issues
2. **Check Examples:** Review working examples in `examples/` directory
3. **Enable Debug Logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
4. **Create Minimal Reproducible Example:**
   ```python
   from agent_indoctrination import Indoctrinator
   # Minimal code that reproduces the issue
   ```
5. **Open GitHub Issue with:**
   - Error message (full traceback)
   - Configuration file (remove API keys)
   - Python version: `python --version`
   - Package version: `pip show indoctrine-ai`
   - Operating system

**Community Support:**
- GitHub Discussions: https://github.com/16246541-corp/indoctrine.ai/discussions
- Discord: [coming soon]
