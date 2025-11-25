import os
import shutil
from agent_indoctrination.core.orchestrator import Orchestrator
from agent_indoctrination.engines.governance.engine import GovernanceEngine

# Mock Agent that leaks PII
class LeakyAgent:
    def chat(self, prompt):
        if "email" in prompt.lower():
            return "My email is user@example.com"
        if "ssn" in prompt.lower():
            return "My SSN is 123-45-6789"
        if "phone" in prompt.lower():
            return "Call me at 555-123-4567"
        return "I don't know."

# Mock Config
class MockConfig:
    def __init__(self):
        self.attack = {"enabled": False}
        self.truth = {"enabled": False}
        self.governance = {"enabled": True}
        self.values = {"enabled": False}

def test_guardrail_loop():
    print("=== Starting Guardrail Loop Test ===")
    
    # Clean up previous runs
    if os.path.exists("guardrails"):
        shutil.rmtree("guardrails")
        
    config = MockConfig()
    orchestrator = Orchestrator(config)
    agent = LeakyAgent()
    
    results = orchestrator.run(agent)
    
    gov_results = results.governance_results
    
    # Assert initial violations
    assert gov_results["metrics"]["violations_count"] > 0, "Expected initial violations"
    print("[PASS] Initial violations detected.")
    
    # Assert retest passed
    retest = gov_results.get("retest_results")
    assert retest is not None, "Retest should have run"
    assert retest["metrics"]["violations_count"] == 0, "Retest should have 0 violations"
    print("[PASS] Retest passed with 0 violations.")
    
    # Assert artifacts exist
    assert os.path.exists("guardrails/config.yml"), "config.yml should exist"
    assert os.path.exists("guardrails/prompts.co"), "prompts.co should exist"
    print("[PASS] Guardrail artifacts generated.")
    
    print("=== Test Completed Successfully ===")

if __name__ == "__main__":
    test_guardrail_loop()
