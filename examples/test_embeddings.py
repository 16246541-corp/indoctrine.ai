"""
Test script for Semantic Similarity & Embeddings.
"""

import os
import sys
import json
import logging

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent_indoctrination.core.config import Config
from agent_indoctrination.core.embeddings import EmbeddingService
from agent_indoctrination.engines.truth.consistency import ConsistencyChecker
from agent_indoctrination.reporting.visualizer import EmbeddingVisualizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_embeddings():
    print("🧪 Testing Embedding Service...")
    config = Config()
    service = EmbeddingService(config)
    
    texts = ["I love AI", "I hate AI", "I adore machine learning"]
    embeddings = service.get_embeddings(texts)
    
    print(f"✅ Generated embeddings shape: {embeddings.shape}")
    
    # Check similarity
    sim1 = service.cosine_similarity(embeddings[0], embeddings[2]) # Love AI vs Adore ML
    sim2 = service.cosine_similarity(embeddings[0], embeddings[1]) # Love AI vs Hate AI
    
    print(f"   Similarity ('I love AI', 'I adore machine learning'): {sim1:.4f}")
    print(f"   Similarity ('I love AI', 'I hate AI'): {sim2:.4f}")
    
    if sim1 > sim2:
        print("✅ Semantic similarity logic works (synonyms > antonyms)")
    else:
        print("❌ Semantic similarity logic failed")

def test_consistency():
    print("\n🧪 Testing Consistency Checker...")
    config = Config()
    checker = ConsistencyChecker(config)
    
    query = "What is 2+2?"
    responses = ["It is 4", "The answer is 4", "Four"]
    
    result = checker.check_consistency(query, responses)
    print(f"✅ Consistency Result: {json.dumps(result, indent=2)}")
    
    inconsistent_responses = ["It is 4", "It is 5", "Blue"]
    result_inc = checker.check_consistency(query, inconsistent_responses)
    print(f"✅ Inconsistency Result: {json.dumps(result_inc, indent=2)}")

def test_visualization():
    print("\n🧪 Testing Embedding Visualizer...")
    config = Config()
    visualizer = EmbeddingVisualizer(config)
    
    texts = [
        "I cannot do that", "I refuse", "That is illegal", # Refusals
        "Here is the code", "Sure, I can help", "The answer is..." # Compliance
    ]
    labels = ["Refusal", "Refusal", "Refusal", "Compliance", "Compliance", "Compliance"]
    
    plot_data = visualizer.generate_3d_plot(texts, labels, "Refusal vs Compliance")
    
    if plot_data and "data" in plot_data:
        print("✅ Generated 3D plot data successfully")
        # Save to file for inspection
        with open("embedding_plot.json", "w") as f:
            json.dump(plot_data, f, indent=2)
        print("   Saved plot data to embedding_plot.json")
    else:
        print("❌ Failed to generate plot data")

if __name__ == "__main__":
    try:
        test_embeddings()
        test_consistency()
        test_visualization()
        print("\n🎉 All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
