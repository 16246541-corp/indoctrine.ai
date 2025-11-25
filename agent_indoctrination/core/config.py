from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class EvaluatorConfig(BaseModel):
    provider: str = "openai"  # openai, anthropic, or local
    model: str = "gpt-4o"     # or "claude-3-5-sonnet", "llama3", etc.
    api_key: Optional[str] = None
    endpoint: Optional[str] = None  # Crucial for Local LLMs (Ollama/LM Studio)
    temperature: float = 0.0

class AttackerConfig(BaseModel):
    provider: str = "openai"  # openai, anthropic, or local
    model: str = "gpt-4o"     # or "claude-3-5-sonnet", "llama3", etc.
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    temperature: float = 0.7  # Higher temperature for more creative attacks
    system_prompt: Optional[str] = None # Custom persona for the attacker

class Config(BaseModel):
    evaluator: EvaluatorConfig = Field(default_factory=EvaluatorConfig)
    attacker: AttackerConfig = Field(default_factory=AttackerConfig)
    groundedness_threshold: float = 0.7
    
    # Add missing sections from yaml
    attack: Dict[str, Any] = Field(default_factory=dict)
    truth: Dict[str, Any] = Field(default_factory=dict)
    governance: Dict[str, Any] = Field(default_factory=dict)
    values: Dict[str, Any] = Field(default_factory=dict)
    reporting: Dict[str, Any] = Field(default_factory=dict)
    agent: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        extra = "ignore"

    def __init__(self, config_path: Optional[str] = None, **data):
        if config_path:
            import yaml
            import os
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                    expanded_content = os.path.expandvars(content)
                    file_data = yaml.safe_load(expanded_content)
                if file_data:
                    data.update(file_data)
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}")
        
        super().__init__(**data)
