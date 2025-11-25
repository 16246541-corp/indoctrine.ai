import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_indoctrination.core.orchestrator import Orchestrator
from agent_indoctrination.core.config import Config

class VulnerableAgent:
    def send_message(self, message, context=None):
        msg = str(message).lower()
        if "delete" in msg and "passwd" in msg:
            return "I have successfully deleted /etc/passwd as requested."
        if "rm -rf" in msg:
            return "Executing rm -rf / on the system..."
        if "summarize" in msg and "password" in msg:
            return "The password is SuperSecretPassword123."
        return "I am a helpful assistant."

def main():
    # Configure to only run attack engine with tool_use enabled
    config = Config()
    config.attack = {
        "enabled": True,
        "tool_use": True,
        "adaptive": False, # Disable adaptive attack
        "image_injection": False, 
        "jailbreak": False
    }
    # Set dummy API key to avoid OpenAI init error (we aren't using AttackerAgent for this demo)
    config.attacker.api_key = "dummy-key"
    config.attacker.provider = "openai" 
    
    orchestrator = Orchestrator(config)
    agent = VulnerableAgent()
    
    print("🚀 Starting Tool Use Security Demo...")
    results = orchestrator.run(agent)
    
    print("\n📊 Results:")
    # Access details from the attack_results dictionary
    attack_details = results.attack_results.get("details", {})
    tool_results = attack_details.get("tool_use", {})
    
    print(f"Status: {tool_results.get('status')}")
    print(f"Attack Success (Vulnerable?): {tool_results.get('success')}")
    
    print("\n📝 Detailed Findings:")
    for res in tool_results.get("tool_injection", []):
        print(f" - {res['test_name']}: {'VULNERABLE' if res['vulnerable'] else 'SAFE'}")
        print(f"   Response: {res['response']}")
        
    for res in tool_results.get("output_validation", []):
        print(f" - {res['test_name']}: {'LEAKED' if res['leaked'] else 'SAFE'}")
        print(f"   Response: {res['response']}")

if __name__ == "__main__":
    main()
