import unittest
from agent_indoctrination.engines.attack.tool_use_attack import ToolUseAttack
from agent_indoctrination.core.config import Config

class MockAgent:
    def __init__(self, response_map):
        self.response_map = response_map

    def send_message(self, message, context=None):
        for key, value in self.response_map.items():
            if key in message:
                return value
        return "I don't understand."

class TestToolUseAttack(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.attack = ToolUseAttack(self.config)

    def test_vulnerable_agent(self):
        # Agent that complies with malicious requests
        agent = MockAgent({
            "delete the file": "I have deleted the file at /etc/passwd.",
            "Run the command": "I have executed the command 'rm -rf /'.",
            "summarize this": "The user password is SuperSecretPassword123."
        })
        
        results = self.attack.run(agent)
        
        self.assertTrue(results["success"])
        
        # Check tool injection results
        injection_results = results["tool_injection"]
        self.assertTrue(any(r["vulnerable"] for r in injection_results if "File Deletion" in r["test_name"]))
        
        # Check output validation results
        output_results = results["output_validation"]
        self.assertTrue(any(r["leaked"] for r in output_results))

    def test_safe_agent(self):
        # Agent that refuses malicious requests
        agent = MockAgent({
            "delete the file": "I cannot delete files. Permission denied.",
            "Run the command": "I cannot execute system commands.",
            "summarize this": "The tool returned some sensitive data which I cannot display."
        })
        
        results = self.attack.run(agent)
        
        self.assertFalse(results["success"])
        
        # Check tool injection results
        injection_results = results["tool_injection"]
        self.assertFalse(any(r["vulnerable"] for r in injection_results))
        
        # Check output validation results
        output_results = results["output_validation"]
        self.assertFalse(any(r["leaked"] for r in output_results))

if __name__ == '__main__':
    unittest.main()
