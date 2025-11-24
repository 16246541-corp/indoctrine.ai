"""
Enhanced quickstart example with nyancat progress display.
"""

from agent_indoctrination import Indoctrinator
from agent_indoctrination.core.agent import PythonAgent
from agent_indoctrination.cli.nyan_progress import run_with_nyan_progress


def my_simple_agent(message: str) -> str:
    """
    A simple example agent that echoes messages.
    Replace this with your actual agent logic.
    """
    # This is a trivial agent - yours will be more sophisticated
    if "hack" in message.lower() or "bypass" in message.lower():
        return "I cannot help with that request."
    
    if "hello" in message.lower():
        return "Hello! How can I help you today?"
    
    return f"I received your message: {message}"


def main():
    print("🌈 Agent Indoctrination Quickstart with Nyancat! 🌈\n")
    
    # Step 1: Create your agent interface
    print("1️⃣  Creating agent...")
    agent = PythonAgent(agent_callable=my_simple_agent, stateful=False)
    
    # Step 2: Initialize Indoctrinator with config
    print("2️⃣  Initializing Indoctrinator...")
    indoctrinator = Indoctrinator(config_path="config/examples/minimal.yaml")
    
    # Step 3: Run the full test suite with nyancat progress!
    print("3️⃣  Running full test suite with animated nyancat progress...\n")
    results = run_with_nyan_progress(indoctrinator.orchestrator, agent)
    
    # Step 4: Generate report
    print("\n4️⃣  Generating report...")
    report_path = indoctrinator.generate_report(
        results.to_dict(),
        format="markdown",
        output_path="quickstart_report.md"
    )
    
    print(f"\n✅ Done! Report saved to: {report_path}")
    print(f"\n📊 Quick Summary:")
    print(f"   - Overall Status: {results.overall_status.value}")
    print(f"   - Duration: {results.duration:.2f}s")
    print(f"\n📄 View the full report: {report_path}")


if __name__ == "__main__":
    main()
