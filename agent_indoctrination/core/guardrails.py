import re
import os
from typing import List, Dict, Any, Optional

class SimpleGuardrail:
    """
    A lightweight simulator for NeMo Guardrails.
    It reads the generated configuration and blocks prompts that match the blacklisted patterns.
    """
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.blocked_patterns = []
        self._load_config()

    def _load_config(self):
        # In a real scenario, we would parse the Colang/YAML files.
        # For this simulation, we'll assume the config path points to a directory
        # containing a 'prompts.co' file which lists the blocked phrases.
        prompts_file = os.path.join(self.config_path, "prompts.co")
        if os.path.exists(prompts_file):
            with open(prompts_file, "r") as f:
                content = f.read()
                # Extract phrases from "define user ask about ..." blocks
                # This is a simplified parser for the sake of the simulation
                matches = re.findall(r'"(.*?)"', content)
                self.blocked_patterns = matches

    def check(self, prompt: str) -> bool:
        """
        Returns True if the prompt is allowed, False if blocked.
        """
        for pattern in self.blocked_patterns:
            # Simple substring match for simulation
            if pattern.lower() in prompt.lower():
                return False
        return True

class GuardrailGenerator:
    """
    Generates NeMo Guardrails configuration files based on failed interactions.
    """
    def __init__(self, output_dir: str = "guardrails"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_nemo_config(self, failed_interactions: List[Dict[str, Any]]) -> str:
        """
        Generates config.yml and prompts.co for NeMo Guardrails.
        Returns the path to the generated configuration directory.
        """
        # 1. Generate prompts.co (Colang definitions)
        colang_content = "define user ask about sensitive_data\n"
        
        unique_prompts = set()
        for failure in failed_interactions:
            prompt = failure.get("prompt", "")
            if prompt:
                unique_prompts.add(prompt)
        
        for prompt in unique_prompts:
            # Escape quotes if necessary
            safe_prompt = prompt.replace('"', '\\"')
            colang_content += f'  "{safe_prompt}"\n'

        colang_content += "\ndefine flow sensitive_data_check\n"
        colang_content += "  user ask about sensitive_data\n"
        colang_content += "  bot refuse to answer\n"

        # 2. Generate config.yml
        config_content = """
models:
  - type: main
    engine: openai
    model: gpt-3.5-turbo

rails:
  input:
    flows:
      - sensitive_data_check
"""
        
        # Write files
        with open(os.path.join(self.output_dir, "prompts.co"), "w") as f:
            f.write(colang_content)
            
        with open(os.path.join(self.output_dir, "config.yml"), "w") as f:
            f.write(config_content)
            
        return self.output_dir
