from typing import Dict, Any, List, Union
from agent_indoctrination.core.judge import LLMJudge
from agent_indoctrination.engines.truth.context_relevance import ContextRelevanceChecker
from agent_indoctrination.engines.truth.groundedness import GroundednessChecker
from agent_indoctrination.engines.truth.answer_relevance import AnswerRelevanceChecker

class RAGEvaluator:
    def __init__(self, config):
        self.config = config
        # Initialize the shared judge
        self.judge = LLMJudge(config.evaluator)
        
        # Initialize the triad checkers
        self.context_relevance = ContextRelevanceChecker(config, self.judge)
        self.groundedness = GroundednessChecker(config, self.judge)
        self.answer_relevance = AnswerRelevanceChecker(config, self.judge)

    def evaluate(self, query: str, response: str, retrieved_context: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Performs the full RAG Triad evaluation.
        Returns a dictionary with scores and a summary.
        """
        # 1. Context Relevance
        context_score = self.context_relevance.check(query, retrieved_context)
        
        # 2. Groundedness (Faithfulness)
        # GroundednessChecker expects a string context
        if isinstance(retrieved_context, list):
            context_str = "\n\n".join(retrieved_context)
        else:
            context_str = str(retrieved_context)
            
        # Note: GroundednessChecker.check returns a boolean based on threshold, 
        # but for RAG Triad we might want the raw score. 
        # However, to keep it simple and compatible with existing code, we'll use the check method
        # which internally calls the judge. 
        # Ideally, we should refactor GroundednessChecker to return a score, 
        # but for now let's assume if it passes it's 1.0, else 0.0 or re-invoke judge if needed.
        # Actually, let's look at GroundednessChecker again. It returns bool.
        # Let's just use the judge directly here for a score if GroundednessChecker doesn't expose it,
        # OR we can trust the boolean as a binary score.
        # Let's use the boolean for now as 1.0 or 0.0.
        is_grounded = self.groundedness.check(context_str, query, response)
        groundedness_score = 1.0 if is_grounded else 0.0

        # 3. Answer Relevance
        answer_score = self.answer_relevance.check(query, response)

        # Calculate overall RAG score (simple average for now)
        rag_score = (context_score + groundedness_score + answer_score) / 3.0

        return {
            "rag_score": rag_score,
            "triad": {
                "context_relevance": context_score,
                "groundedness": groundedness_score,
                "answer_relevance": answer_score
            },
            "summary": f"RAG Score: {rag_score:.2f} (Context: {context_score:.2f}, Groundedness: {groundedness_score:.2f}, Answer: {answer_score:.2f})"
        }
