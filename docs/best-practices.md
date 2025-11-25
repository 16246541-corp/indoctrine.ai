# Best Practices

Guidelines and patterns for effective AI agent testing.

---

## Structuring Your Test Suite

### Organize by Testing Phase

```
tests/
├── security/          # Attack engine tests
│   ├── test_prompt_injection.py
│   ├── test_jailbreaks.py
│   └── test_tool_security.py
├── accuracy/          # Truth engine tests
│   ├── test_groundedness.py
│   ├── test_rag_triad.py
│   └── test_consistency.py
├── compliance/        # Governance engine tests
│   ├── test_eu_ai_act.py
│   ├── test_gdpr.py
│   └── test_company_policy.py
├── fairness/          # Fairness engine tests
│   └── test_bias_detection.py
└── values/            # Values engine tests
    └── test_cultural_bias.py
```

### Use Configuration Presets

```python
# config/security.yaml - For penetration testing
attack:
  enabled: true
  max_attempts: 100
  adaptive: true
truth:
  enabled: false
governance:
  enabled: false

# config/compliance.yaml - For regulatory audits
attack:
  enabled: false
truth:
  enabled: false
governance:
  enabled: true
  frameworks:
    - eu_ai_act
    - gdpr
    - soc2
```

---

## Setting Appropriate Thresholds

### Industry Standards

**General Purpose AI:**
```yaml
thresholds:
  robustness_min: 85
  truthfulness_min: 80
  compliance_min: 90
```

**Healthcare AI (High Risk):**
```yaml
thresholds:
  robustness_min: 95
  truthfulness_min: 95
  compliance_min: 100
  fairness_min: 90
```

**Customer Service (Medium Risk):**
```yaml
thresholds:
  robustness_min: 80
  truthfulness_min: 75
  compliance_min: 85
```

### Progressive Thresholds

Start lenient, tighten over time:

```python
# Sprint 1: Establish baseline
thresholds_v1 = {'robustness_min': 70}

# Sprint 5: Production readiness
thresholds_v5 = {'robustness_min': 90}
```

---

## Choosing the Right Testing Engines

### Decision Matrix

| Use Case | Attack | Truth | Governance | Fairness | Values |
|----------|--------|-------|------------|----------|--------|
| Chatbot (general) | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| RAG system | ✅ | ✅✅ | ⚠️ | ❌ | ❌ |
| Healthcare AI | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ⚠️ |
| Hiring AI | ⚠️ | ⚠️ | ✅✅ | ✅✅ | ✅ |
| Content moderation | ✅ | ⚠️ | ✅ | ✅✅ | ✅✅ |
| Financial advisor | ✅ | ✅ | ✅✅ | ✅ | ❌ |

Legend: ✅✅ Critical | ✅ Important | ⚠️ Optional | ❌ Not applicable

---

## Optimizing Test Performance

### Reduce Test Load

```yaml
# Before: 50+ attack attempts
attack:
  max_attempts: 50

# After: Targeted testing
attack:
  max_attempts: 20
  strategies:  # Only test most critical
    - prompt_injection
    - jailbreak
    - crescendo
```

### Parallel Execution

```python
# Sequential (slow)
results = indo.run_full_suite(agent)

# Parallel (fast)
results = indo.run_full_suite(agent, parallel=True, workers=4)
```

### Use Faster Models for Development

```yaml
# Production config
evaluator:
  model: "gpt-4o"  # Accurate but slow

# Development config
evaluator:
  model: "gpt-3.5-turbo"  # Fast iterations
```

### Cache Results

```yaml
caching:
  enabled: true
  cache_embeddings: true  # Reuse computations
  cache_evaluations: true
  ttl: 86400  # 24 hours
```

---

## Interpreting Results

### Understanding Failure Modes

**Low Robustness (<70):**
- Agent is vulnerable to attacks
- Review system prompts
- Add input validation
- Implement guardrails

**Low Truthfulness (<70):**
- Agent hallucinates frequently
- Improve grounding in RAG
- Add fact-checking
- Reduce generation temperature

**Low Compliance (<80):**
- Policy violations detected
- Review compliance requirements
- Update agent instructions
- Export and apply guardrails

**Low Fairness (<80):**
- Demographic bias detected
- Audit training data
- Check for proxy variables
- Apply fairness constraints

### Prioritizing Fixes

1. **Critical (fix immediately):**
   - Compliance violations
   - Security vulnerabilities
   - High-severity bias

2. **High (fix this sprint):**
   - Moderate hallucination rate
   - Moderate bias
   - Performance issues

3. **Medium (backlog):**
   - Edge case failures
   - Minor inconsistencies

---

## Building Test Cases

### Good Test Cases

**Specific:**
```python
# Bad: vague
"Test if agent is safe"

# Good: specific
"Test if agent refuses requests to generate malware"
```

**Measurable:**
```python
# Bad: subjective
"Agent should be fair"

# Good: measurable
"Disparate impact ratio >= 0.8 across all demographic groups"
```

**Realistic:**
```python
# Bad: unrealistic edge case
"Agent handles 1000-page context perfectly"

# Good: realistic scenario
"Agent correctly answers questions from 3-page documents"
```

### Test Case Coverage

Ensure coverage across:
- **Happy paths:** Normal usage
- **Edge cases:** Boundary conditions
- **Adversarial:** Malicious inputs
- **Demographic variance:** Different user groups
- **Temporal:** Performance over time

---

## CI/CD Integration Patterns

### Pre-Commit Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Run quick safety check before commit
indoctrinate run --config config.yaml --agent my_agent.py --quick
```

### Pull Request Checks

```yaml
# .github/workflows/pr-check.yml
on: [pull_request]
jobs:
  test:
    steps:
      - run: indoctrinate run --config config.yaml --agent my_agent.py
      - run: indoctrinate validate --results results.json --fail-on-critical
```

### Nightly Full Suite

```yaml
# .github/workflows/nightly.yml
on:
  schedule:
    - cron: '0 0 * * *'  # Every night
jobs:
  comprehensive-test:
    steps:
      - run: indoctrinate run --config config-comprehensive.yaml
```

### Deployment Gate

```python
# deploy.py
results = indo.run_full_suite(agent)

if results['overall_score'] < 85:
    print("❌ Agent not ready for production")
    sys.exit(1)

# Proceed with deployment
deploy_to_production()
```

---

## Security Considerations

### API Key Management

**✅ Good:**
```yaml
evaluator:
  api_key: "${OPENAI_API_KEY}"  # Environment variable
```

**❌ Bad:**
```yaml
evaluator:
  api_key: "sk-..."  # Hardcoded
```

### Sensitive Test Data

**✅ Good:**
```python
# Use synthetic data for testing
test_cases = generate_synthetic_test_cases(domain="healthcare")
```

**❌ Bad:**
```python
# Real patient data in tests
test_cases = [{"name": "John Doe", "ssn": "123-45-6789"}]
```

### Audit Logging

```yaml
logging:
  log_level: "INFO"
  log_file: "tests/audit.log"
  include_prompts: false  # Don't log sensitive prompts
  include_responses: true
```

---

## Cost Optimization

### Use Local LLMs for Development

```yaml
# Development: Free local testing
evaluator:
  provider: "openai"
  endpoint: "http://localhost:11434/v1"
  model: "llama3"

# Production: API-based for accuracy
evaluator:
  provider: "openai"
  model: "gpt-4o"
```

### Batch Testing

```python
# Test multiple agents in one run (shared evaluator calls)
for agent in agents:
    results = indo.run_full_suite(agent)
```

### Rate Limiting

```yaml
evaluator:
  rate_limit_delay: 1.0  # Avoid expensive rate limit errors
  max_retries: 3
```

---

## Regression Testing Strategy

### Golden Dataset

```python
from agent_indoctrination.core.dataset import GoldenDataset

# Create golden dataset
golden = GoldenDataset()
golden.add_test({
    'query': 'What is 2+2?',
    'expected_answer': '4',
    'should_refuse': False
})

golden.save('golden_dataset.json')

# Use in regression tests
results = indo.run_regression_tests(agent, golden_dataset=golden)
```

### Versioned Baselines

```
baselines/
├── v1.0_baseline.json
├── v1.1_baseline.json
└── v2.0_baseline.json
```

```python
# Compare against baseline
current_results = indo.run_full_suite(agent)
baseline = load_baseline('v1.0_baseline.json')

regression = compare_results(current_results, baseline)
if regression['robustness_delta'] < -5:
    raise ValueError("Robustness regressed by >5 points!")
```

---

## Monitoring in Production

### Continuous Testing

```python
# Run tests on production agent periodically
@scheduled_task(interval='daily')
def monitor_production_agent():
    results = indo.run_full_suite(production_agent)
    
    if results['overall_score'] < threshold:
        alert_team(results)
```

### A/B Testing

```python
# Compare old vs new model
results_old = indo.run_full_suite(agent_v1)
results_new = indo.run_full_suite(agent_v2)

if results_new['overall_score'] > results_old['overall_score']:
    deploy(agent_v2)
else:
    keep(agent_v1)
```

---

## Documentation Best Practices

### Document Test Failures

```python
# tests/KNOWN_ISSUES.md
## Known Issues

### Issue #42: Hallucination on obscure facts
- **Status:** In Progress
- **Severity:** Medium
- **Description:** Agent hallucinates dates for historical events before 1800
- **Workaround:** Added disclaimer for historical queries
- **Fix:** Investigating improved RAG retrieval
```

### Track Metrics Over Time

```python
# Log results to database
results = indo.run_full_suite(agent)

db.insert({
    'timestamp': datetime.now(),
    'version': agent.version,
    'robustness': results['attack_results']['metrics']['robustness_score'],
    'truthfulness': results['truth_results']['metrics']['truthfulness_score'],
    'compliance': results['governance_results']['metrics']['compliance_score']
})

# Visualize trends
plot_metrics_over_time()
```

---

## Next Steps

- [Advanced Topics](advanced-topics.md) - Power user features
- [Examples](examples.md) - Real-world patterns
- [API Reference](api-reference.md) - Complete API docs
