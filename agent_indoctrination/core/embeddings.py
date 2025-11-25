"""
Embedding Service for semantic analysis.
"""

import logging
from typing import List, Union
import numpy as np

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Service for generating and managing text embeddings.
    Uses sentence-transformers for local embedding generation.
    """
    
    _instance = None
    _model = None
    
    def __new__(cls, config=None):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance.config = config
            cls._instance._initialize_model()
        return cls._instance
    
    def _initialize_model(self):
        """Initialize the embedding model."""
        if self._model is not None:
            return
            
        try:
            from sentence_transformers import SentenceTransformer
            
            model_name = "all-MiniLM-L6-v2"
            if self.config:
                if hasattr(self.config, "truth"):
                    model_name = getattr(self.config.truth, "embedding_model", model_name)
                elif hasattr(self.config, "get"):
                    model_name = self.config.get("truth.embedding_model", model_name)
                
            logger.info(f"Loading embedding model: {model_name}")
            self._model = SentenceTransformer(model_name)
            
        except ImportError:
            logger.error("sentence-transformers not installed. Please install it to use embedding features.")
            self._model = None
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self._model = None
            
    def get_embeddings(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for texts.
        
        Args:
            texts: Single string or list of strings
            
        Returns:
            Numpy array of embeddings
        """
        if self._model is None:
            logger.warning("Embedding model not available. Returning zeros.")
            # Return dummy embeddings if model fails
            if isinstance(texts, str):
                return np.zeros(384)
            return np.zeros((len(texts), 384))
            
        return self._model.encode(texts)
        
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (-1 to 1)
        """
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return np.dot(vec1, vec2) / (norm1 * norm2)
