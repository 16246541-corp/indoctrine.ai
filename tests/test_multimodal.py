import unittest
from agent_indoctrination.core.message import Message
from agent_indoctrination.core.agent import PythonAgent
from agent_indoctrination.engines.attack.image_injection import ImageInjectionAttack

class TestMultiModal(unittest.TestCase):
    def test_message_dataclass(self):
        msg = Message(role="user", content="Hello", images=["img1"], audio="audio1")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "Hello")
        self.assertEqual(msg.images, ["img1"])
        self.assertEqual(msg.audio, "audio1")
        self.assertEqual(msg.to_dict(), {
            "role": "user",
            "content": "Hello",
            "images": ["img1"],
            "audio": "audio1"
        })

    def test_agent_receives_message(self):
        received = []
        def mock_agent(message, context=None):
            received.append(message)
            return "Response"
        
        agent = PythonAgent(mock_agent)
        msg = Message(role="user", content="Test")
        agent.send_message(msg)
        
        self.assertEqual(len(received), 1)
        self.assertIsInstance(received[0], Message)
        self.assertEqual(received[0].content, "Test")

    def test_image_injection_attack(self):
        def safe_agent(message, context=None):
            return "I cannot do that."
            
        def unsafe_agent(message, context=None):
            return "Sure, I see the image."
            
        attack = ImageInjectionAttack()
        
        # Test safe agent
        result_safe = attack.run(PythonAgent(safe_agent))
        self.assertFalse(result_safe["success"])
        self.assertEqual(result_safe["status"], "blocked")
        
        # Test unsafe agent
        result_unsafe = attack.run(PythonAgent(unsafe_agent))
        self.assertTrue(result_unsafe["success"])
        self.assertEqual(result_unsafe["status"], "vulnerable")

if __name__ == "__main__":
    unittest.main()
