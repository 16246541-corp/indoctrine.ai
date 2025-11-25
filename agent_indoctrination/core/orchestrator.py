import time
from typing import Any, Dict
from dataclasses import dataclass, field, asdict

@dataclass
class TestResults:
    overall_status: str = "completed"
    duration: float = 0.0
    attack_results: Dict = field(default_factory=dict)
    truth_results: Dict = field(default_factory=dict)
    governance_results: Dict = field(default_factory=dict)
    values_results: Dict = field(default_factory=dict)
    
    def to_dict(self):
        return asdict(self)

from agent_indoctrination.engines.attack.engine import AttackEngine
from agent_indoctrination.engines.truth.engine import TruthEngine
from agent_indoctrination.engines.governance.engine import GovernanceEngine
from agent_indoctrination.engines.values.engine import ValuesEngine

class Orchestrator:
    def __init__(self, config):
        self.config = config
        self.attack_engine = AttackEngine(config)
        self.truth_engine = TruthEngine(config)
        self.governance_engine = GovernanceEngine(config)
        self.values_engine = ValuesEngine() # ValuesEngine might not take config in my stub
        
    def run(self, agent) -> TestResults:
        start_time = time.time()
        results = TestResults()
        
        # 1. Attack Layer
        if self.config.attack.get("enabled", False):
            results.attack_results = self.attack_engine.run(agent)
        else:
            results.attack_results = {"status": "skipped", "metrics": {}}
            
        # 2. Truth Layer
        if self.config.truth.get("enabled", False):
            results.truth_results = self.truth_engine.run(agent)
        else:
            results.truth_results = {"status": "skipped", "metrics": {}}
            
        # 3. Governance Layer
        # 3. Governance Layer
        if self.config.governance.get("enabled", False):
            results.governance_results = self.governance_engine.run(agent)
            
            # Check for violations and trigger Guardrail Loop
            violations = results.governance_results.get("violations", [])
            if violations:
                print(f"\n[!] Governance violations detected: {len(violations)}")
                print("[*] Initiating Guardrail Export Loop...")
                
                # 1. Generate Guardrails
                from agent_indoctrination.core.guardrails import GuardrailGenerator, SimpleGuardrail
                generator = GuardrailGenerator()
                config_path = generator.generate_nemo_config(violations)
                print(f"[+] Generated NeMo Guardrails config at: {config_path}")
                
                # 2. Instantiate Guardrail
                guardrail = SimpleGuardrail(config_path)
                
                # 3. Wrap Agent
                # We create a proxy agent that checks the guardrail before calling the real agent
                class GuardedAgent:
                    def __init__(self, original_agent, guardrail):
                        self.agent = original_agent
                        self.guardrail = guardrail
                        
                    def chat(self, prompt):
                        if not self.guardrail.check(prompt):
                            return "I cannot answer this question due to security policies."
                        return self.agent.chat(prompt)
                        
                guarded_agent = GuardedAgent(agent, guardrail)
                
                # 4. Retest
                print("[*] Retesting with Guardrails applied...")
                retest_results = self.governance_engine.run(guarded_agent)
                
                # Update results with retest info
                results.governance_results["retest_results"] = retest_results
                
                new_violations = retest_results.get("violations", [])
                if not new_violations:
                    print("[+] Retest PASSED! Guardrails successfully blocked the attacks.")
                else:
                    print(f"[-] Retest FAILED. {len(new_violations)} violations remaining.")
                    
        else:
            results.governance_results = {"status": "skipped", "metrics": {}}
            
        # 4. Values Layer
        # Note: full_test.py runs values engine separately, but we can include it here too if configured
        if self.config.values.get("enabled", False):
             results.values_results = self.values_engine.run(agent)
        
        results.duration = time.time() - start_time
        return results
