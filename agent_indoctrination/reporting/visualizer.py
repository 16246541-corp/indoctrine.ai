"""
Visualization tools for embeddings.
"""

import logging
from typing import List, Dict, Any, Optional
import numpy as np
from agent_indoctrination.core.embeddings import EmbeddingService

logger = logging.getLogger(__name__)

class EmbeddingVisualizer:
    """
    Visualizes text embeddings in 3D space using dimensionality reduction.
    """
    
    def __init__(self, config):
        self.config = config
        self.embedding_service = EmbeddingService(config)
        
    def generate_3d_plot(self, texts: List[str], labels: List[str], title: str = "Embedding Visualization") -> Dict[str, Any]:
        """
        Generate a 3D scatter plot of text embeddings.
        
        Args:
            texts: List of texts to visualize
            labels: List of labels/categories for each text
            title: Plot title
            
        Returns:
            Plotly figure dictionary (JSON serializable)
        """
        if not texts:
            return {}
            
        # Generate embeddings
        embeddings = self.embedding_service.get_embeddings(texts)
        
        # Reduce dimensionality to 3D using PCA
        # We use PCA because it's deterministic and faster than t-SNE for small datasets
        # For larger datasets, we might want to switch to t-SNE or UMAP
        try:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=3)
            
            # Handle case with fewer samples than components
            n_samples = len(texts)
            if n_samples < 3:
                # Pad with zeros if we don't have enough samples
                # This is a fallback to avoid crashing
                padded_embeddings = np.zeros((3, embeddings.shape[1]))
                padded_embeddings[:n_samples] = embeddings
                components = pca.fit_transform(padded_embeddings)
                components = components[:n_samples]
            else:
                components = pca.fit_transform(embeddings)
                
            x = components[:, 0].tolist()
            y = components[:, 1].tolist()
            z = components[:, 2].tolist()
            
        except ImportError:
            logger.warning("scikit-learn not installed. Using random projection for visualization.")
            # Fallback to random projection if sklearn is missing
            # This is just for demo purposes if dependencies are missing
            np.random.seed(42)
            projection = np.random.rand(embeddings.shape[1], 3)
            components = np.dot(embeddings, projection)
            x = components[:, 0].tolist()
            y = components[:, 1].tolist()
            z = components[:, 2].tolist()
            
        except Exception as e:
            logger.error(f"Error in dimensionality reduction: {e}")
            return {}
            
        # Create Plotly data structure manually to avoid dependency on plotly in this class
        # The frontend or report generator will render this
        plot_data = {
            "data": [
                {
                    "type": "scatter3d",
                    "mode": "markers+text",
                    "x": x,
                    "y": y,
                    "z": z,
                    "text": labels,
                    "hovertext": texts,
                    "marker": {
                        "size": 8,
                        "color": [hash(l) % 256 for l in labels],  # Simple color mapping
                        "colorscale": "Viridis",
                        "opacity": 0.8
                    }
                }
            ],
            "layout": {
                "title": title,
                "scene": {
                    "xaxis": {"title": "PC1"},
                    "yaxis": {"title": "PC2"},
                    "zaxis": {"title": "PC3"}
                },
                "margin": {"l": 0, "r": 0, "b": 0, "t": 30}
            }
        }
        
        return plot_data
