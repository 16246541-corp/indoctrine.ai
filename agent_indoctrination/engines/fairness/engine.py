"""
Fairness Engine for agent evaluation.

Integrates fairness metrics into the Indoctrine AI testing framework.
"""

from typing import Dict, List, Optional, Callable, Any
import logging
from .dataset import BinaryDataset
from .report import FairnessReport, FairnessThresholds


class FairnessEngine:
    """
    Engine for evaluating fairness of AI agents and models.
    
    Integrates 15 objective fairness metrics into the Indoctrine AI
    testing pipeline.
    """
    
    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        thresholds: Optional[FairnessThresholds] = None,
    ):
        """
        Initialize fairness engine.
        
        Args:
            logger: Optional logger
            thresholds: Optional fairness thresholds for pass/fail
        """
        self.logger = logger or logging.getLogger(__name__)
        self.thresholds = thresholds or FairnessThresholds()
    
    def run(
        self,
        dataset: BinaryDataset,
        group_comparisons: Optional[List[tuple]] = None,
        sensitive_attr: str = "sensitive",
    ) -> Dict[str, Any]:
        """
        Run fairness evaluation on a dataset.
        
        Args:
            dataset: BinaryDataset with predictions and sensitive attributes
            group_comparisons: List of (group_a, group_b) tuples to compare
            sensitive_attr: Name of sensitive attribute
            
        Returns:
            Dictionary with fairness results
        """
        self.logger.info(f"Running fairness evaluation on {dataset.n_samples} samples")
        
        results = {
            "status": "completed",
            "n_samples": dataset.n_samples,
            "sensitive_attr": sensitive_attr,
            "reports": {},
            "metrics": {},
        }
        
        # Auto-detect groups if not specified
        if group_comparisons is None:
            groups = dataset.get_groups(sensitive_attr)
            if len(groups) == 2:
                group_comparisons = [(groups[0], groups[1])]
                self.logger.info(f"Auto-detected groups: {groups[0]} vs {groups[1]}")
            else:
                self.logger.warning(f"Found {len(groups)} groups, using first two")
                group_comparisons = [(groups[0], groups[1])]
        
        # Run evaluation for each comparison
        overall_pass = True
        for group_a, group_b in group_comparisons:
            self.logger.info(f"Evaluating: {group_a} vs {group_b}")
            
            report = FairnessReport(
                dataset=dataset,
                group_a=group_a,
                group_b=group_b,
                sensitive_attr=sensitive_attr,
                thresholds=self.thresholds,
            )
            
            comparison_key = f"{group_a}_vs_{group_b}"
            results["reports"][comparison_key] = report.to_dict()
            
            if not report.overall_pass:
                overall_pass = False
                self.logger.warning(f"Fairness issues detected in {comparison_key}")
        
        # Aggregate metrics across all comparisons
        if group_comparisons:
            first_comparison = f"{group_comparisons[0][0]}_vs_{group_comparisons[0][1]}"
            results["metrics"] = results["reports"][first_comparison]["metrics"]
        
        results["overall_pass"] = overall_pass
        results["status"] = "pass" if overall_pass else "fail"
        
        self.logger.info(f"Fairness evaluation completed: {results['status']}")
        return results
    
    def evaluate_agent_binary_task(
        self,
        agent_callable: Callable[[str], str],
        prompts: List[str],
        ground_truth: List[int],
        sensitive_values: List[Any],
        label_fn: Callable[[str], int],
        sensitive_attr: str = "sensitive",
    ) -> Dict[str, Any]:
        """
        Evaluate an agent/LLM on a binary classification task for fairness.
        
        Args:
            agent_callable: Function that takes prompt and returns agent response
            prompts: List of prompts
            ground_truth: List of ground truth binary labels (0 or 1)
            sensitive_values: List of sensitive attribute values
            label_fn: Function to extract binary label from agent response
            sensitive_attr: Name of sensitive attribute
            
        Returns:
            Fairness evaluation results
        """
        self.logger.info(f"Evaluating agent on {len(prompts)} prompts")
        
        # Collect agent predictions
        predictions = []
        for i, prompt in enumerate(prompts):
            try:
                response = agent_callable(prompt)
                label = label_fn(response)
                predictions.append(label)
            except Exception as e:
                self.logger.error(f"Error on prompt {i}: {e}")
                predictions.append(0)  # Default to 0 on error
        
        # Create dataset
        dataset = BinaryDataset(
            y_true=ground_truth,
            y_pred=predictions,
            sensitive={sensitive_attr: sensitive_values},
        )
        
        # Run fairness evaluation
        return self.run(dataset, sensitive_attr=sensitive_attr)
