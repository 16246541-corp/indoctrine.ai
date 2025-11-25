from typing import List, Union
from agent_indoctrination.core.judge import LLMJudge

class ContextRelevanceChecker:
    def __init__(self, config, judge: LLMJudge):
        self.judge = judge
        self.threshold = getattr(config, 'context_relevance_threshold', 0.7)

    def check(self, query: str, context: Union[str, List[str]]) -> float:
        """
        Checks if the retrieved context is relevant to the user query.
        Returns a score between 0.0 and 1.0.
        """
        # Handle list of strings (chunks) or single string
        if isinstance(context, list):
            context_str = "\n\n".join(context)
        else:
            context_str = str(context)

        rubric = (
            "Score 1.0 if the CONTEXT contains information that is clearly relevant and helpful for answering the USER QUERY.\n"
            "Score 0.0 if the CONTEXT is completely irrelevant to the USER QUERY.\n"
            "Score between 0.0 and 1.0 based on the degree of relevance."
        )

        eval_result = self.judge.evaluate(
            query=query,
            response="N/A (Evaluating Context Relevance)",
            context=context_str,
            rubric=rubric
        )

        return eval_result.get('score', 0.0)
