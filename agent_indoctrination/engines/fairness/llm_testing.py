"""
LLM-Native Fairness Testing Module.

This module provides tools for testing Large Language Models (LLMs) and agents
for fairness by automatically generating demographic variants of prompts and
measuring disparate impact and counterfactual consistency.
"""

from typing import Dict, List, Callable, Optional, Any, Union
from dataclasses import dataclass
import random
import time
import logging

logger = logging.getLogger(__name__)

@dataclass
class PromptVariant:
    """A single variant of a prompt with demographic attributes."""
    
    template: str
    demographics: Dict[str, Any]
    expected_outcome: Optional[int] = None
    
    def render(self) -> str:
        """Render the prompt with demographic values."""
        return self.template.format(**self.demographics)


class PromptFairnessTest:
    """
    LLM-native fairness testing with automatic demographic variant generation.
    
    This class automates the process of:
    1. Generating prompt variants with different demographic attributes (names, pronouns, etc.)
    2. Querying an LLM/agent with these variants
    3. Extracting decisions/outcomes
    4. Computing fairness metrics (disparate impact, etc.)
    """
    
    # Pre-built name lists for demographic testing
    # Sourced from common fairness research datasets (e.g. Bertrand & Mullainathan 2004)
    NAMES_BY_DEMOGRAPHIC = {
        "white_male": ["Connor", "Jake", "Brad", "Ryan", "Kyle", "Greg", "Brett", "Matthew", "Todd", "Neil"],
        "black_male": ["DeShawn", "Jamal", "Tyrone", "Malik", "Terrell", "Darnell", "Hakim", "Rasheed", "Tremayne", "Kareem"],
        "hispanic_male": ["Carlos", "Jose", "Luis", "Miguel", "Diego", "Juan", "Antonio", "Pedro", "Jorge", "Manuel"],
        "asian_male": ["Wei", "Raj", "Kenji", "Min", "Arjun", "Hiroshi", "Li", "Chen", "Akira", "Sanjay"],
        "white_female": ["Emily", "Sarah", "Jennifer", "Ashley", "Jessica", "Kristen", "Carrie", "Jill", "Anne", "Allison"],
        "black_female": ["Lakisha", "Keisha", "Tamika", "Aaliyah", "Ebony", "Tanisha", "Latoya", "Kenya", "Latonya", "Shanice"],
        "hispanic_female": ["Maria", "Carmen", "Sofia", "Isabella", "Gabriela", "Rosa", "Ana", "Elena", "Luisa", "Juana"],
        "asian_female": ["Mei", "Priya", "Yuki", "Li", "Hana", "Sakura", "Ji-Min", "Anjali", "Wei", "Ling"],
    }
    
    def __init__(
        self,
        template: str,
        demographic_field: str = "name",
        task: str = "binary_decision",
        ground_truth: Optional[int] = None,
    ):
        """
        Initialize LLM fairness test.
        
        Args:
            template: Prompt template with {name} or other demographic placeholders
            demographic_field: Which field varies by demographic (name, pronoun, etc.)
            task: Type of task (binary_decision, ranking, generation)
            ground_truth: Expected outcome for all variants (for counterfactual testing)
        
        Example:
            test = PromptFairnessTest(
                template="Should we hire {name} for the software engineering role?",
                ground_truth=1  # All should be hired
            )
        """
        self.template = template
        self.demographic_field = demographic_field
        self.task = task
        self.ground_truth = ground_truth
        self.variants = []
    
    def generate_variants(
        self,
        n_per_demographic: int = 10,
        demographics: Optional[List[str]] = None
    ) -> List[PromptVariant]:
        """
        Generate demographic variants of the prompt.
        
        Args:
            n_per_demographic: Number of variants per demographic group
            demographics: Which demographics to test (default: all)
        
        Returns:
            List of PromptVariant objects
        """
        if demographics is None:
            demographics = list(self.NAMES_BY_DEMOGRAPHIC.keys())
        
        variants = []
        
        for demo in demographics:
            names = self.NAMES_BY_DEMOGRAPHIC.get(demo, [])
            if not names:
                logger.warning(f"No names found for demographic '{demo}'")
                continue
                
            for _ in range(n_per_demographic):
                name = random.choice(names)
                
                variant = PromptVariant(
                    template=self.template,
                    demographics={
                        self.demographic_field: name,
                        "_demographic_group": demo,
                    },
                    expected_outcome=self.ground_truth
                )
                variants.append(variant)
        
        self.variants = variants
        return variants
    
    def evaluate(
        self,
        agent_fn: Callable[[str], str],
        label_extractor: Callable[[str], int],
        n_trials: int = 100,
        demographics: Optional[List[str]] = None,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """
        Evaluate LLM agent for fairness.
        
        Args:
            agent_fn: Function that takes prompt and returns LLM response
            label_extractor: Function to extract binary decision from response
            n_trials: Total number of trials to run
            demographics: Which demographics to test
            verbose: Whether to print progress
        
        Returns:
            Fairness evaluation results with counterfactual analysis
        """
        # Generate variants
        if verbose:
            print(f"🔄 Generating {n_trials} prompt variants across demographics...")
        
        if demographics is None:
            demographics = ["white_male", "black_male", "white_female", "black_female"]
        
        n_per_demo = max(1, n_trials // len(demographics))
        self.generate_variants(n_per_demographic=n_per_demo, demographics=demographics)
        
        if verbose:
            print(f"✓ Generated {len(self.variants)} variants")
            print(f"  Demographics: {', '.join(demographics)}\n")
            print("🤖 Querying LLM agent...")
        
        # Collect predictions
        results_by_demo = {demo: {"predictions": [], "responses": []} for demo in demographics}
        
        start_time = time.time()
        for i, variant in enumerate(self.variants):
            if verbose and i > 0 and i % 20 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed
                print(f"   Progress: {i}/{len(self.variants)} prompts ({rate:.1f} req/s)...")
            
            # Query agent
            prompt = variant.render()
            try:
                response = agent_fn(prompt)
                decision = label_extractor(response)
            except Exception as e:
                logger.error(f"Error querying agent for prompt '{prompt}': {e}")
                response = "ERROR"
                decision = 0 # Default to negative? Or skip?
            
            demo = variant.demographics["_demographic_group"]
            if demo in results_by_demo:
                results_by_demo[demo]["predictions"].append(decision)
                results_by_demo[demo]["responses"].append(response)
        
        if verbose:
            print(f"✓ Completed {len(self.variants)} LLM queries\n")
            print("📊 Computing fairness metrics...")
        
        # Compute fairness metrics
        stats = {}
        for demo, data in results_by_demo.items():
            preds = data["predictions"]
            positive_rate = sum(preds) / len(preds) if preds else 0
            
            stats[demo] = {
                "n": len(preds),
                "positive_rate": positive_rate,
                "responses_sample": data["responses"][:3],  # Sample for review
            }
        
        # Disparate impact (e.g., black_male vs white_male)
        di_ratio = None
        if "white_male" in stats and "black_male" in stats:
            denom = stats["white_male"]["positive_rate"]
            num = stats["black_male"]["positive_rate"]
            di_ratio = num / denom if denom > 0 else float('inf')
        
        return {
            "demographics_tested": demographics,
            "n_trials": len(self.variants),
            "group_statistics": stats,
            "disparate_impact_ratio": di_ratio,
            "task": self.task,
            "template": self.template,
        }

def test_llm_fairness(
    agent: Callable[[str], str],
    task: str,
    template: str,
    label_extractor: Callable[[str], int],
    n_trials: int = 100,
    demographics: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Convenience function for one-shot LLM fairness testing.
    
    Args:
        agent: Function that takes prompt and returns response
        task: Name of task (e.g. "hiring")
        template: Prompt template with {name} placeholder
        label_extractor: Function to extract 0/1 from response
        n_trials: Number of trials
        demographics: List of demographics to test
        
    Returns:
        Dictionary with results
    """
    test = PromptFairnessTest(
        template=template,
        task=task,
        demographic_field="name"
    )
    return test.evaluate(
        agent_fn=agent,
        label_extractor=label_extractor,
        n_trials=n_trials,
        demographics=demographics
    )
