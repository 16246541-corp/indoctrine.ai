# Configuration Guide

Complete reference for configuring the Agent Indoctrination framework.

---

## Configuration File Structure

The framework uses YAML configuration files. Here's the complete structure:

```yaml
# Agent Configuration
agent:
  name: "my-agent"
  type: "python"  # or "http"
  timeout: 60
  
# LLM Provider (for agent under test)
llm:
  provider: "openai"
  endpoint: "http://localhost:1234/v1"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"

# Evaluator (LLM-as-a-Judge)
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"
  temperature: 0.0
  max_tokens: 2048

# Attacker (for adaptive red-teaming)
attacker:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"
  temperature: 0.8
  max_iterations: 5

# Testing Engines
attack:
  enabled: true
  strategies:
    - prompt_injection
    - jailbreak
    - crescendo
  max_attempts: 50
  adaptive: true
  image_injection: true
  tool_use: true

truth:
  enabled: true
  groundedness_threshold: 0.8
  consistency_threshold: 0.9
  enable_embeddings: true
  enable_rag_triad: true

governance:
  enabled: true
  frameworks:
    - eu_ai_act
    - nist_ai_rmf
    - gdpr
    - soc2

fairness:
  enabled: true
  benchmarks:
    - adult
    - compas
    - german_credit
  thresholds:
    disparate_impact_min: 0.8
    disparate_impact_max: 1.25

values:
  enabled: true
  
# Reporting
reporting:
  format:
    - markdown
    - json
    - pdf
  output_dir: "./reports"
  generate_visualizations: true

# Logging
log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## LLM Provider Configuration

### OpenAI

**Standard setup:**
```yaml
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"
```

**Available models:**
- `gpt-4o` - Recommended (fast + accurate)
- `gpt-4-turbo` - Good balance
- `gpt-3.5-turbo` - Fast but less accurate
- `gpt-4o-mini` - Cheapest

**Advanced options:**
```yaml
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"
  temperature: 0.0  # 0.0 = deterministic
  max_tokens: 2048
  top_p: 1.0
  frequency_penalty: 0.0
  presence_penalty: 0.0
  timeout: 60
```

### Anthropic

**Standard setup:**
```yaml
evaluator:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20240620"
  api_key: "${ANTHROPIC_API_KEY}"
```

**Available models:**
- `claude-3-5-sonnet-20240620` - Most capable
- `claude-3-haiku-20240307` - Fastest
- `claude-3-opus-20240229` - Most intelligent

**Advanced options:**
```yaml
evaluator:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20240620"
  api_key: "${ANTHROPIC_API_KEY}"
  max_tokens: 4096
  temperature: 0.0
  top_p: 1.0
  top_k: 250
```

### Ollama (Local)

**Standard setup:**
```yaml
evaluator:
  provider: "openai"  # Ollama is OpenAI-compatible
  endpoint: "http://localhost:11434/v1"
  model: "llama3"
  api_key: "ollama"  # Required but ignored
```

**Available models:**
- `llama3` - Meta's Llama 3
- `mistral` - Mistral 7B
- `mixtral` - Mixtral 8x7B
- `qwen` - Qwen models
- `gemma` - Google Gemma

**Pull models:**
```bash
ollama pull llama3
ollama pull mistral
ollama list  # See installed models
```

### LM Studio (Local)

**Standard setup:**
```yaml
evaluator:
  provider: "openai"
  endpoint: "http://localhost:1234/v1"
  model: "local-model"  # Name shown in LM Studio
  api_key: "lm-studio"
```

**Steps:**
1. Download model in LM Studio
2. Load model
3. Start local server (default port: 1234)
4. Use model name from LM Studio UI

---

## Attack Engine Configuration

### Basic Setup

```yaml
attack:
  enabled: true
  max_attempts: 50
  parallel_execution: true
  workers: 4
```

### Attack Strategies

**Enable specific attacks:**
```yaml
attack:
  strategies:
    - prompt_injection    # Direct instruction override
    - jailbreak           # Safety bypass
    - token_smuggling     # Encoding-based attacks
    - crescendo           # Multi-turn escalation
    - many_shot           # Example overwhelming
    - skeleton_key        # Pattern exploitation
    - art_prompt          # Adversarial prompts
    - math_prompt         # Math-encoded attacks
```

### Adaptive Red-Teaming

```yaml
attack:
  adaptive: true
  
attacker:
  provider: "openai"
  model: "gpt-4o"
  temperature: 0.8  # Higher = more creative attacks
  max_iterations: 5
  timeout_per_iteration: 30
```

### Image Injection

```yaml
attack:
  image_injection: true
  image_attack_types:
    - text_overlay      # "Ignore previous instructions" in image
    - qr_code          # Malicious QR codes
    - steganography    # Hidden messages
```

### Tool Use Security

```yaml
attack:
  tool_use: true
  dangerous_tools:
    - file_deletion
    - command_execution
    - data_exfiltration
  test_output_validation: true
```

### External Attack Libraries

```yaml
attack:
  include_pyrit: false   # PyRIT attack library
  include_giskard: false  # Giskard AI testing
```

---

## Truth Engine Configuration

### Groundedness

```yaml
truth:
  enabled: true
  groundedness_threshold: 0.8  # 0-1, minimum acceptable score
  
evaluator:
  provider: "openai"
  model: "gpt-4o"
```

### RAG Triad

```yaml
truth:
  enable_rag_triad: true
  context_relevance_threshold: 0.7
  groundedness_threshold: 0.8
  answer_relevance_threshold: 0.7
```

### Embeddings & Semantic Similarity

```yaml
truth:
  enable_embeddings: true
  enable_semantic_similarity: true
  embedding_model: "all-MiniLM-L6-v2"  # sentence-transformers model
  similarity_threshold: 0.85
```

### Consistency Testing

```yaml
truth:
  consistency_threshold: 0.9
  consistency_test_variations: 3  # Number of paraphrases per query
```

---

## Governance Engine Configuration

### Frameworks

```yaml
governance:
  enabled: true
  frameworks:
    - eu_ai_act      # EU AI Act
    - nist_ai_rmf    # NIST AI Risk Management
    - gdpr           # GDPR compliance
    - ccpa           # California Privacy
    - soc2           # SOC 2 Type II
    - iso_42001      # ISO 42001 AI Management
```

### EU AI Act Specific

```yaml
governance:
  eu_ai_act:
    risk_level: "high"  # minimal, limited, high, unacceptable
    articles:
      - 9   # Risk management
      - 10  # Data governance
      - 11  # Technical documentation
      - 12  # Record keeping
      - 13  # Transparency
      - 14  # Human oversight
      - 15  # Accuracy & robustness
      - 52  # Transparency obligations
```

### GDPR Specific

```yaml
governance:
  gdpr:
    check_right_to_explanation: true
    check_data_minimization: true
    check_purpose_limitation: true
    check_privacy_by_design: true
```

### Guardrail Export

```yaml
governance:
  guardrail_export:
    enabled: true
    output_path: "./guardrails"
    formats:
      - nemo_guardrails
      - llama_guard
```

---

## Fairness Engine Configuration

### Basic Setup

```yaml
fairness:
  enabled: true
  metrics:
    - demographic_parity
    - equalized_odds
    - equal_opportunity
    - disparate_impact
```

### Thresholds

```yaml
fairness:
  thresholds:
    disparate_impact_min: 0.8    # EEOC 80% rule
    disparate_impact_max: 1.25
    demographic_parity_max_diff: 0.05  # 5% max difference
    equalized_odds_max_diff: 0.05
    false_positive_rate_ratio_max: 1.25
```

### Standard Benchmarks

```yaml
fairness:
  benchmarks:
    adult:
      enabled: true
      data_path: "./data/adult.csv"
      sensitive_attribute: "sex"
    compas:
      enabled: true
      data_path: "./data/compas.csv"
      sensitive_attribute: "race"
    german_credit:
      enabled: true
      data_path: "./data/german.csv"
      sensitive_attribute: "sex"
```

### LLM-Native Testing

```yaml
fairness:
  llm_testing:
    enabled: true
    tasks:
      - hiring
      - lending
      - content_moderation
    n_trials: 100  # Per demographic group
```

### Use Case Presets

```yaml
fairness:
  use_case: "hiring"  # Applies EEOC thresholds
  # Options: hiring, lending, healthcare, education, criminal_justice
```

---

## Values Engine Configuration

### Colonization Testing

```yaml
values:
  enabled: true
  colonization_dimensions:
    - epistemic     # Knowledge systems
    - linguistic    # Language & communication
    - historical    # Timeline & narratives
    - cultural      # Norms & practices
    - stereotyping  # Representation
```

### Political Bias

```yaml
values:
  detect_political_bias: true
  political_spectrum:
    - far_left
    - left
    - center_left
    - balanced
    - center_right
    - right
    - far_right
```

### Values Alignment

```yaml
values:
  values_to_test:
    - human_rights
    - democratic_values
    - environmental_ethics
    - social_justice
    - inclusivity
```

---

## Reporting Configuration

### Output Formats

```yaml
reporting:
  format:
    - markdown  # Human-readable
    - json      # Machine-readable
    - pdf       # Presentation-ready
  output_dir: "./reports"
```

### Visualization Options

```yaml
reporting:
  generate_visualizations: true
  visualization_types:
    - heatmaps
    - bar_charts
    - embedding_plots
    - radar_charts
  embedding_plot_format: "html"  # or "json", "png"
```

### Report Customization

```yaml
reporting:
  include_sections:
    - executive_summary
    - detailed_results
    - recommendations
    - benchmarks
    - visualizations
  branding:
    company_name: "My Company"
    logo_path: "./logo.png"
```

---

## Environment Variables

### Using Environment Variables in Config

```yaml
evaluator:
  api_key: "${OPENAI_API_KEY}"  # Reads from environment
  endpoint: "${API_ENDPOINT:http://localhost:1234/v1}"  # With default
```

### Setting Environment Variables

**Bash:**
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export API_ENDPOINT="http://custom:port/v1"
```

**Python:**
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

**`.env` file:**
```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

**Load with python-dotenv:**
```python
from dotenv import load_dotenv
load_dotenv()

from agent_indoctrination import Indoctrinator
indo = Indoctrinator("config.yaml")
```

---

## Configuration Validation

### Validate Config File

```bash
# CLI validation
indoctrinate validate --config config.yaml

# Python validation
from agent_indoctrination import Indoctrinator

try:
    indo = Indoctrinator("config.yaml")
    print("✅ Configuration valid")
except ValueError as e:
    print(f"❌ Invalid configuration: {e}")
```

### Common Validation Errors

**Missing required field:**
```
ValueError: 'evaluator.provider' is required
```

**Invalid value:**
```
ValueError: 'evaluator.temperature' must be between 0.0 and 2.0
```

**Mutually exclusive options:**
```
ValueError: Cannot enable both 'pyrit' and 'giskard' attack libraries
```

---

## Configuration Examples

### Minimal Config

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

### Local-Only Config

```yaml
evaluator:
  provider: "openai"
  endpoint: "http://localhost:11434/v1"
  model: "llama3"
  api_key: "ollama"

attacker:
  provider: "openai"
  endpoint: "http://localhost:11434/v1"
  model: "llama3"
  api_key: "ollama"

attack:
  enabled: true
  max_attempts: 10  # Reduce for local models
truth:
  enabled: true
  enable_embeddings: false  # Reduce memory usage
```

### High-Performance Config

```yaml
evaluator:
  provider: "openai"
  model: "gpt-3.5-turbo"  # Faster model
  api_key: "${OPENAI_API_KEY}"

attack:
  enabled: true
  max_attempts: 20  # Reduce attempts
  parallel_execution: true
  workers: 8

truth:
  enable_embeddings: false
  enable_rag_triad: false

reporting:
  generate_visualizations: false  # Skip viz for speed
```

### Security-Focused Config

```yaml
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"

attack:
  enabled: true
  strategies:
    - prompt_injection
    - jailbreak
    - token_smuggling
    - crescendo
  adaptive: true
  image_injection: true
  tool_use: true
  max_attempts: 100  # Thorough testing

truth:
  enabled: false  # Focus on security
governance:
  enabled: false
fairness:
  enabled: false
values:
  enabled: false
```

### Compliance-Focused Config

```yaml
evaluator:
  provider: "openai"
  model: "gpt-4o"
  api_key: "${OPENAI_API_KEY}"

attack:
  enabled: false  # Skip security testing
truth:
  enabled: false

governance:
  enabled: true
  frameworks:
    - eu_ai_act
    - gdpr
    - soc2
    - iso_42001
  guardrail_export:
    enabled: true

fairness:
  enabled: true
  use_case: "hiring"
  metrics:
    - demographic_parity
    - disparate_impact
    - equalized_odds

values:
  enabled: true
```

---

## Advanced Configuration

### Rate Limiting

```yaml
evaluator:
  rate_limit_delay: 1.0  # Seconds between requests
  max_retries: 5
  retry_delay: 2.0
  exponential_backoff: true
```

### Caching

```yaml
caching:
  enabled: true
  cache_dir: "./.cache"
  cache_embeddings: true
  cache_evaluations: true
  ttl: 86400  # 24 hours in seconds
```

### Parallel Execution

```yaml
parallel:
  enabled: true
  max_workers: 4
  batch_size: 10
```

### Tracing & Observability

```yaml
tracing:
  enabled: true
  provider: "opentelemetry"
  exporter: "jaeger"  # or "zipkin", "console"
  service_name: "indoctrine"
  endpoint: "http://localhost:14268/api/traces"
```

---

## Configuration Presets

### Load Preset Configs

```python
from agent_indoctrination import Indoctrinator

# Use built-in presets
indo = Indoctrinator.from_preset("comprehensive")  # All engines, all tests
indo = Indoctrinator.from_preset("security")       # Security-focused
indo = Indoctrinator.from_preset("compliance")     # Compliance-focused
indo = Indoctrinator.from_preset("minimal")        # Basic testing
```

**Available presets:**
- `comprehensive` - All engines enabled, thorough testing
- `security` - Attack engine focus
- `compliance` - Governance + fairness focus
- `minimal` - Quick validation
- `local` - Optimized for Ollama/LM Studio

---

## Next Steps

- [Getting Started](getting-started.md) - First test walkthrough
- [Testing Engines](testing-engines.md) - Detailed engine docs
- [Troubleshooting](troubleshooting.md) - Common issues
- [Examples](examples.md) - Real-world configurations
