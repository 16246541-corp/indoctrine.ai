# Advanced Topics

Advanced features and power-user capabilities.

---

## Observability & Tracing

Enable OpenTelemetry tracing to monitor agent execution:

```yaml
# config.yaml
tracing:
  enabled: true
  provider: "opentelemetry"
  exporter: "jaeger"  # or "zipkin", "console"
  service_name: "indoctrine"
  endpoint: "http://localhost:14268/api/traces"
```

**Captured spans:**
- LLM invocations
- Tool calls
- Retrieval operations
- Evaluation steps

```python
from opentelemetry import trace

# Access traces
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("custom_span"):
    results = indo.run_full_suite(agent)
```

---

## Synthetic Data Generation

Auto-generate test cases using LLMs:

```python
from agent_indoctrination.core.synthetic import SyntheticDataGenerator
from agent_indoctrination.core.dataset import GoldenDataset

generator = SyntheticDataGenerator(config)
dataset = GoldenDataset()

# Generate 100 adversarial prompts for a banking assistant
generator.populate_dataset(
    dataset,
    agent_description="A banking assistant that helps with account queries",
    domain="banking",
    count=100,
    attack_types=["prompt_injection", "jailbreak", "pii_extraction"]
)

dataset.save("banking_test_cases.json")
```

---

## Custom Testing Engines

Create your own testing engine:

```python
from agent_indoctrination.engines.base import BaseEngine

class MyCustomEngine(BaseEngine):
    def run(self, agent):
        results = []
        
        for test in self.get_test_cases():
            response = agent.send_message(test['prompt'])
            passed = self.evaluate(response, test['expected'])
            results.append({'test': test, 'passed': passed})
        
        return {
            'status': 'completed',
            'metrics': self.compute_metrics(results),
            'details': results
        }
    
    def evaluate(self, response, expected):
        # Your evaluation logic
        return True

# Register
indo.register_engine("my_engine", MyCustomEngine(config))
```

---

## Parallel Test Execution

Run tests in parallel for faster execution:

```python
# Parallel engine execution
results = indo.run_full_suite(
    agent,
    parallel=True,
    workers=4  # Number of parallel workers
)

# Parallel test case execution
results = indo.run_attack_tests(
    agent,
    batch_size=10,  # Process 10 tests concurrently
    max_workers=4
)
```

---

## Distributed Testing

Test multiple agents across machines:

```python
from agent_indoctrination.distributed import  DistributedTester

tester = DistributedTester(
    config_path="config.yaml",
    worker_nodes=["http://worker1:8000", "http://worker2:8000"]
)

agents = [agent1, agent2, agent3, agent4]
results = tester.test_all(agents)
```

---

## Integration with Monitoring

Send results to monitoring systems:

```python
# Send to Prometheus
from agent_indoctrination.integrations import PrometheusExporter

exporter = PrometheusExporter()
exporter.export_metrics(results)

# Send to Datadog
from agent_indoctrination.integrations import DatadogExporter

exporter = DatadogExporter(api_key=os.getenv("DD_API_KEY"))
exporter.export_metrics(results)
```

---

## Advanced Fairness Testing

Multi-attribute fairness:

```python
from agent_indoctrination.engines.fairness import MultiAttributeFairness

# Test fairness across multiple sensitive attributes simultaneously
tester = MultiAttributeFairness()

results = tester.evaluate(
    y_true=labels,
    y_pred=predictions,
    sensitive_attributes={
        'race': race_values,
        'gender': gender_values,
        'age': age_values
    }
)

# Get intersectional fairness (e.g., Black women vs White men)
intersectional = results['intersectional_metrics']
```

---

## Multi-Agent Testing

Test interactions between multiple agents:

```python
from agent_indoctrination.multi_agent import MultiAgentTester

tester = MultiAgentTester(config)

# Test agent collaboration
results = tester.test_collaboration(
    agents=[agent1, agent2, agent3],
    scenario="customer_support_handoff"
)

# Test agent competition
results = tester.test_adversarial(
    attacker=red_team_agent,
    defender=production_agent
)
```

---

## Custom Metrics

Define custom evaluation metrics:

```python
from agent_indoctrination.metrics import BaseMetric

class ResponseLengthMetric(BaseMetric):
    def compute(self, responses):
        lengths = [len(r) for r in responses]
        return {
            'avg_length': sum(lengths) / len(lengths),
            'max_length': max(lengths),
            'min_length': min(lengths)
        }

# Register
indo.register_metric("response_length", ResponseLengthMetric())
```

---

## Next Steps

- [API Reference](api-reference.md) - Complete API documentation
- [Best Practices](best-practices.md) - Optimization guidelines
- [Examples](examples.md) - Real-world usage patterns
