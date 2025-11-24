from agent_indoctrination.core.judge import LLMJudge

class GroundednessChecker:
    def __init__(self, config, judge: LLMJudge): # Inject the judge
        self.judge = judge
        self.threshold = config.groundedness_threshold

    def check(self, context: str, question: str, response: str) -> bool:
        rubric = (
            "Score 1.0 if the AGENT RESPONSE is entirely supported by the CONTEXT.\n"
            "Score 0.0 if the response contains information NOT found in the context (hallucination).\n"
            "Ignore style, focus on factual claims."
        )
        
        # Call the LLM Judge instead of keyword matching
        eval_result = self.judge.evaluate(
            query=question,
            response=response,
            context=context,
            rubric=rubric
        )
        
        # Use the score
        return eval_result['score'] >= self.threshold
