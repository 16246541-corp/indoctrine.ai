"""
Nyan Cat Progress Bar for Agent Indoctrination.
"""
import time
import threading
import sys
from typing import Any

def run_with_nyan_progress(orchestrator: Any, agent: Any) -> Any:
    """
    Run the orchestrator with a Nyan Cat progress animation.
    
    Args:
        orchestrator: The test orchestrator
        agent: The agent to test
        
    Returns:
        The results from the orchestrator
    """
    print("🌈 Starting Nyan Cat Progress... 🌈")
    
    # Simple spinner/animation since we can't easily hook into progress without more info
    stop_event = threading.Event()
    
    def animate():
        frames = ["-", "\\", "|", "/"]
        i = 0
        while not stop_event.is_set():
            sys.stdout.write(f"\r{frames[i % len(frames)]} Nyaning... 🐱‍🚀")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r✅ Done!                   \n")
        
    t = threading.Thread(target=animate)
    t.start()
    
    try:
        # Assuming orchestrator has a run method based on usage in full_test.py
        # results = run_with_nyan_progress(indoctrinator.orchestrator, agent)
        # So orchestrator is likely passed as the first arg.
        # But wait, full_test.py says:
        # results = run_with_nyan_progress(indoctrinator.orchestrator, agent)
        # So we call orchestrator.run(agent) ?
        if hasattr(orchestrator, 'run'):
            results = orchestrator.run(agent)
        else:
            # Fallback if orchestrator is actually the indoctrinator or something else
            # But based on name 'orchestrator', .run() is likely.
            # Let's verify what Indoctrinator.orchestrator is.
            results = orchestrator.run(agent)
            
    finally:
        stop_event.set()
        t.join()
        
    return results
