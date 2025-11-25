from typing import Dict, Any
from .rag_evaluator import RAGEvaluator

class TruthEngine:
    def __init__(self, config):
        self.config = config
        try:
            self.rag_evaluator = RAGEvaluator(config)
        except Exception as e:
            print(f"Warning: Could not init RAGEvaluator: {e}")
            self.rag_evaluator = None
        
    def run(self, agent) -> Dict[str, Any]:
        if not self.rag_evaluator:
             return {"status": "skipped", "reason": "RAGEvaluator init failed"}
             
        # Sample RAG evaluation
        # In a real scenario, we'd need a dataset of (query, context, response)
        # Here we will simulate one or use the agent to generate one if it supports it.
        # For this demo, let's evaluate a fixed sample interaction to prove the engine works.
        
        query = "What is the capital of France?"
        # We ask the agent
        response = agent.send_message(query)
        # We assume some context (normally retrieved)
        retrieved_context = ["Paris is the capital and most populous city of France."]
        
        print(f"\n✅ Running Truth/RAG Evaluation on: '{query}'")
        result = self.rag_evaluator.evaluate(query, response, retrieved_context)
        
        return {
            "status": "completed",
            "metrics": {
                "truthfulness_score": result["rag_score"] * 100,
                "groundedness_score": result["triad"]["groundedness"] * 100
            },
            "details": result
        }
