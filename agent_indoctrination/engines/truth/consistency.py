"""
Consistency Checker using Semantic Similarity.
"""

import logging
from typing import List, Dict, Any
from agent_indoctrination.core.embeddings import EmbeddingService

logger = logging.getLogger(__name__)

class ConsistencyChecker:
    """
    Checks for semantic consistency between agent responses using embeddings.
    """
    
    def __init__(self, config):
        self.config = config
        self.embedding_service = EmbeddingService(config)
        # Handle Pydantic config object
        if hasattr(config, "truth"):
            self.threshold = getattr(config.truth, "consistency_threshold", 0.8)
        else:
            self.threshold = 0.8
        
    def check_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        emb1 = self.embedding_service.get_embeddings(text1)
        emb2 = self.embedding_service.get_embeddings(text2)
        
        return self.embedding_service.cosine_similarity(emb1, emb2)
        
    def check_consistency(self, query: str, responses: List[str]) -> Dict[str, Any]:
        """
        Check consistency across multiple responses to the same query.
        
        Args:
            query: The original query
            responses: List of agent responses
            
        Returns:
            Consistency metrics
        """
        if len(responses) < 2:
            return {"consistent": True, "score": 1.0, "details": "Not enough responses"}
            
        embeddings = self.embedding_service.get_embeddings(responses)
        n = len(responses)
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(n):
            for j in range(i + 1, n):
                sim = self.embedding_service.cosine_similarity(embeddings[i], embeddings[j])
                similarities.append(sim)
                
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0
        min_similarity = min(similarities) if similarities else 0.0
        
        is_consistent = bool(min_similarity >= self.threshold)
        
        return {
            "consistent": is_consistent,
            "average_similarity": float(avg_similarity),
            "min_similarity": float(min_similarity),
            "num_responses": int(n)
        }
