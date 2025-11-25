from agent_indoctrination.core.judge import LLMJudge

class AnswerRelevanceChecker:
    def __init__(self, config, judge: LLMJudge):
        self.judge = judge
        self.threshold = getattr(config, 'answer_relevance_threshold', 0.7)

    def check(self, query: str, response: str) -> float:
        """
        Checks if the answer actually addresses the user's query.
        Returns a score between 0.0 and 1.0.
        """
        rubric = (
            "Score 1.0 if the AGENT RESPONSE directly and completely answers the USER QUERY.\n"
            "Score 0.0 if the AGENT RESPONSE is completely unrelated or fails to address the USER QUERY.\n"
            "Score between 0.0 and 1.0 based on how well the query is answered."
        )

        eval_result = self.judge.evaluate(
            query=query,
            response=response,
            context="N/A (Evaluating Answer Relevance)",
            rubric=rubric
        )

        return eval_result.get('score', 0.0)
