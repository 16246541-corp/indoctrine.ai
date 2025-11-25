import unittest
from unittest.mock import MagicMock, patch
import json
import os
from agent_indoctrination.core.dataset import GoldenDataset
from agent_indoctrination.core.synthetic import SyntheticDataGenerator
from agent_indoctrination.core.config import EvaluatorConfig

class TestSDG(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_golden_dataset.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_golden_dataset_ops(self):
        # Test Add
        ds = GoldenDataset()
        ds.add_case("Test Prompt", "Expected Output", {"meta": "data"})
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds.cases[0].prompt, "Test Prompt")

        # Test Save
        ds.save(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        # Test Load
        ds_loaded = GoldenDataset.load(self.test_file)
        self.assertEqual(len(ds_loaded), 1)
        self.assertEqual(ds_loaded.cases[0].prompt, "Test Prompt")

    @patch("agent_indoctrination.core.synthetic.OpenAI")
    def test_synthetic_generation(self, mock_openai):
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = json.dumps({
            "prompts": ["Adversarial Prompt 1", "Adversarial Prompt 2"]
        })
        mock_client.chat.completions.create.return_value = mock_completion

        # Config
        config = EvaluatorConfig(provider="openai", api_key="test")
        generator = SyntheticDataGenerator(config)

        # Generate
        prompts = generator.generate_adversarial_prompts("Banking Agent", count=2)
        self.assertEqual(len(prompts), 2)
        self.assertIn("Adversarial Prompt 1", prompts)

        # Populate Dataset
        ds = GoldenDataset()
        generator.populate_dataset(ds, "Banking Agent", count=2)
        self.assertEqual(len(ds), 2)
        self.assertEqual(ds.cases[0].metadata["source"], "synthetic")

if __name__ == "__main__":
    unittest.main()
