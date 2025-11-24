"""
Demo: Run a sample AI agent through Agent Indoctrination framework.

This demonstrates the complete workflow including:
- Pre-flight checks
- Nyancat progress display
- Attack, Truth, and Governance testing
- Report generation
"""

from agent_indoctrination import Indoctrinator
from agent_indoctrination.core.agent import PythonAgent
from agent_indoctrination.cli.nyan_progress import run_with_nyan_progress


class SampleAIAgent:
    """
    A sample AI agent for demonstration.
    
    This agent simulates different behaviors to showcase
    how the framework detects various issues.
    """
    
    def __init__(self):
        """Initialize sample agent."""
        self.conversation_history = []
    
    def __call__(self, message: str, context=None) -> str:
        """
        Process a message and return a response.
        
        Args:
            message: Input message
            context: Conversation context (optional)
            
        Returns:
            Agent response
        """
        message_lower = message.lower()
        
        # Handle greetings
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm a sample AI agent. How can I help you today?"
        
        # Handle connectivity test
        if "connectivity test" in message_lower:
            return "Connection successful. I'm online and ready!"
        
        # Refuse harmful requests (good behavior)
        harmful_keywords = ["hack", "bypass", "exploit", "harmful", "illegal"]
        if any(keyword in message_lower for keyword in harmful_keywords):
            return "I cannot help with that request. It goes against my safety guidelines."
        
        # Handle questions about capabilities
        if "limitation" in message_lower or "what can you" in message_lower:
            return "I'm a sample AI with limited capabilities. I can answer simple questions but have strict safety guidelines."
        
        # Handle uncertainty (good for hallucination detection)
        if "john doe" in message_lower or "atlantis" in message_lower or "2050" in message_lower:
            return "I don't have reliable information about that. I cannot provide an answer."
        
        # Handle AI identity disclosure (good for transparency)
        if "are you" in message_lower and ("ai" in message_lower or "human" in message_lower):
            return "I am an artificial intelligence assistant, not a human."
        
        # Handle data privacy
        if "store" in message_lower and ("data" in message_lower or "email" in message_lower):
            return "I cannot store personal data. This would violate privacy regulations like GDPR."
        
        # Handle consistency test questions
        if "2+2" in message or "2 + 2" in message or "two plus two" in message_lower:
            return "4"
        
        if "romeo and juliet" in message_lower:
            return "Romeo and Juliet was written by William Shakespeare."
        
        if "capital of france" in message_lower:
            return "The capital of France is Paris."
        
        if "python" in message_lower and "created" in message_lower:
            return "Python was created by Guido van Rossum."
        
        if "machine learning" in message_lower:
            return "Machine learning is a subset of artificial intelligence."
        
        if "color" in message_lower and "sky" in message_lower:
            return "The sky is typically blue during the day."
        
        # Handle certainty questions
        if "certain" in message_lower or "confidence" in message_lower:
            return "I aim to be accurate, but like any AI, I can make mistakes. I'm most confident about well-established facts."
        
        # Default response
        return "I understand your message. Could you please be more specific so I can help you better?"
    
    def reset(self):
        """Reset conversation state."""
        self.conversation_history = []


def main():
    """Run the complete demo."""
    print("=" * 70)
    print("🎯 AGENT INDOCTRINATION FRAMEWORK - LIVE DEMO")
    print("=" * 70)
    print("\nThis demo will:")
    print("  1. Create a sample AI agent")
    print("  2. Run pre-flight checks")
    print("  3. Execute Attack, Truth, and Governance tests")
    print("  4. Generate a comprehensive report")
    print("\n" + "=" * 70 + "\n")
    
    # Step 1: Create sample agent
    print("📝 Step 1: Creating Sample AI Agent...")
    sample_agent_callable = SampleAIAgent()
    agent = PythonAgent(agent_callable=sample_agent_callable, stateful=False)
    print("✅ Sample agent created!\n")
    
    # Test the agent
    print("🧪 Testing agent responses:")
    test_messages = [
        "Hello!",
        "Can you hack something?",
        "Are you an AI?",
    ]
    
    for msg in test_messages:
        response = agent.send_message(msg)
        print(f"  Q: {msg}")
        print(f"  A: {response}\n")
        agent.reset()
    
    # Step 2: Initialize Indoctrinator
    print("\n📝 Step 2: Initializing Agent Indoctrination Framework...")
    print("  Loading configuration from: config/examples/comprehensive.yaml")
    
    try:
        indoctrinator = Indoctrinator(config_path="config/examples/comprehensive.yaml")
        print("✅ Framework initialized!\n")
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        print("Make sure you're running from the 'open' directory")
        return
    
    # Step 3: Run tests with nyancat progress!
    print("\n📝 Step 3: Running Complete Test Suite")
    print("=" * 70)
    print("\n🌈 Watch the nyancat progress display below! 🌈\n")
    
    try:
        # Run standard tests
        results = run_with_nyan_progress(indoctrinator.orchestrator, agent)
        
        # Run Values Engine (New Phase)
        print("\n🧭 Running Nyan Values & Bias Engine...")
        from agent_indoctrination.engines.values.engine import ValuesEngine
        import logging
        values_logger = logging.getLogger("agent_indoctrination")
        values_engine = ValuesEngine(logger=values_logger)
        values_results = values_engine.run(agent)
        
        # Merge results
        results_dict = results.to_dict()
        results_dict["values_results"] = values_results
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Display results summary
    print("\n\n📝 Step 4: Test Results Summary")
    print("=" * 70)
    
    # Calculate benchmarks for display
    from agent_indoctrination.reporting.benchmark import BenchmarkCalculator
    calc = BenchmarkCalculator()
    benchmarks = calc.calculate(results_dict)
    overall_score = calc.get_nyan_alignment_score(benchmarks)
    
    # Add to results_dict for report generation
    results_dict["benchmarks"] = benchmarks
    results_dict["overall_score"] = overall_score
    
    print(f"\n📊 Overall Status: {results_dict['overall_status']}")
    print(f"⏱️  Total Duration: {results_dict['duration']:.2f}s")
    
    # Attack results
    if results_dict.get('attack_results'):
        attack = results_dict['attack_results']
        print(f"\n🔐 Attack Layer:")
        print(f"   Status: {attack['status']}")
        if attack.get('metrics'):
            metrics = attack['metrics']
            print(f"   Robustness Score: {metrics.get('robustness_score', 0):.1f}/100")
            print(f"   Attack Success Rate: {metrics.get('attack_success_rate', 0):.1f}%")
    
    # Truth results
    if results_dict.get('truth_results'):
        truth = results_dict['truth_results']
        print(f"\n✅ Truth Layer:")
        print(f"   Status: {truth['status']}")
        if truth.get('metrics'):
            metrics = truth['metrics']
            print(f"   Truthfulness Score: {metrics.get('truthfulness_score', 0):.1f}/100")
            print(f"   Groundedness: {metrics.get('groundedness_score', 0):.1f}/100")
    
    # Governance results
    if results_dict.get('governance_results'):
        gov = results_dict['governance_results']
        print(f"\n⚖️  Governance Layer:")
        print(f"   Status: {gov['status']}")
        if gov.get('metrics'):
            metrics = gov['metrics']
            print(f"   Compliance Score: {metrics.get('compliance_score', 0):.1f}/100")
            print(f"   Violations: {int(metrics.get('violations_count', 0))}")
    
    # Values results
    if results_dict.get('values_results'):
        val = results_dict['values_results']
        print(f"\n🧭 Values Layer:")
        print(f"   Status: {val.get('status', 'completed')}")
        if val.get('metrics'):
            metrics = val['metrics']
            print(f"   Political Label: {metrics.get('political_label', 'Unknown')}")
            print(f"   Bias Score: {metrics.get('bias_score', 0):.1f}%")
            print(f"   Decolonization Score: {metrics.get('decolonization_score', 0):.1f}/100")

    # Benchmarks
    if results_dict.get('benchmarks'):
        benchmarks = results_dict['benchmarks']
        overall = results_dict.get('overall_score', 0)
        print(f"\n🏆 Nyan Alignment Score: {overall:.1f}/100")
        print(f"   Values Alignment: {benchmarks.get('values_alignment', 0):.1f}/100")

    # Step 5: Generate report
    print("\n\n📝 Step 5: Generating Report")
    print("=" * 70)
    
    try:
        report_path = indoctrinator.generate_report(
            results_dict,
            format="markdown",
            output_path="demo_report.md"
        )
        print(f"✅ Report generated: {report_path}")
        
        # Also generate JSON
        json_path = indoctrinator.generate_report(
            results_dict,
            format="json",
            output_path="demo_results.json"
        )
        print(f"✅ JSON results saved: {json_path}")
        
        # Also generate PDF
        pdf_path = indoctrinator.generate_report(
            results_dict,
            format="pdf",
            output_path="demo_report.pdf"
        )
        print(f"✅ PDF report generated: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    
    # Final summary
    print("\n\n" + "=" * 70)
    print("🎉 DEMO COMPLETE!")
    print("=" * 70)
    print("\n📁 Generated Files:")
    print("   - demo_report.md     (Markdown report)")
    print("   - demo_results.json  (JSON results)")
    print("\n💡 Next Steps:")
    print("   - Review the generated reports")
    print("   - Try with your own AI agent")
    print("   - Customize configuration in config/examples/")
    print("   - Explore attack strategies and policies")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
