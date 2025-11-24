from typing import Optional
from pydantic import BaseModel, Field

class EvaluatorConfig(BaseModel):
    provider: str = "openai"  # openai, anthropic, or local
    model: str = "gpt-4o"     # or "claude-3-5-sonnet", "llama3", etc.
    api_key: Optional[str] = None
    endpoint: Optional[str] = None  # Crucial for Local LLMs (Ollama/LM Studio)
    temperature: float = 0.0

class Config(BaseModel):
    evaluator: EvaluatorConfig = Field(default_factory=EvaluatorConfig)
    groundedness_threshold: float = 0.7
    
    class Config:
        extra = "ignore"
