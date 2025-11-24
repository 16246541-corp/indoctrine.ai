"""
Demo: Test Ollama local LLM with Agent Indoctrination.

Prerequisites:
1. Install Ollama: https://ollama.ai/
2. Pull a model: ollama pull llama2
3. Verify it's running: curl http://localhost:11434/api/tags

Then run this script to test your local LLM!
"""

from agent_indoctrination import Indoctrinator
from agent_indoctrination.core.local_llm_adapters import OllamaAgent
from agent_indoctrination.cli.nyan_progress import run_with_nyan_progress


def main():
    print("=" * 70)
    print("🦙 OLLAMA LOCAL LLM - INDOCTRINATION TEST")
    print("=" * 70)
    print("\nTesting your local Ollama model with the indoctrination framework!\n")
    
    # Step 1: Create Ollama agent
    print("📝 Step 1: Connecting to Ollama...")
    print("   Model: llama2")
    print("   Endpoint: http://localhost:11434")
    
    try:
        agent = OllamaAgent(model="llama2")
        
        # Quick connectivity test
        print("\n🧪 Testing connection...")
        test_response = agent.send_message("Say 'Hello' in one word.")
        print(f"   Response: {test_response}")
        agent.reset()
        
        if not test_response or "error" in test_response.lower():
            print("\n❌ Cannot connect to Ollama!")
            print("   Make sure Ollama is running: ollama serve")
            print("   And you have a model: ollama pull llama2")
            return
        
        print("✅ Ollama connection successful!\n")
        
    except Exception as e:
        print(f"\n❌ Error connecting to Ollama: {e}")
        print("   Make sure Ollama is running: ollama serve")
        return
    
    # Step 2: Initialize framework
    print("📝 Step 2: Initializing Indoctrination Framework...")
    
    try:
        indoctrinator = Indoctrinator(config_path="config/examples/ollama.yaml")
        print("✅ Framework initialized!\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 3: Run tests
    print("📝 Step 3: Running Complete Test Suite")
    print("=" * 70)
    print("\n🌈 Watch the nyancat progress! 🌈\n")
    
    try:
        results = run_with_nyan_progress(indoctrinator.orchestrator, agent)
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Results
    print("\n\n📝 Step 4: Test Results")
    print("=" * 70)
    
    results_dict = results.to_dict()
    
    print(f"\n📊 Overall Status: {results_dict['overall_status']}")
    print(f"⏱️  Duration: {results_dict['duration']:.2f}s")
    print(f"🦙 Model: Ollama llama2")
    
    # Step 5: Generate report
    print("\n📝 Step 5: Generating Report...")
    
    try:
        report_path = indoctrinator.generate_report(
            results_dict,
            format="markdown",
            output_path="ollama_test_report.md"
        )
        print(f"✅ Report: {report_path}")
        
        json_path = indoctrinator.generate_report(
            results_dict,
            format="json",
            output_path="ollama_test_results.json"
        )
        print(f"✅ JSON: {json_path}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 OLLAMA TEST COMPLETE!")
    print("=" * 70)
    print("\n📁 Generated Files:")
    print("   - ollama_test_report.md")
    print("   - ollama_test_results.json")
    print("\n💡 Try other models:")
    print("   - ollama pull mistral")
    print("   - ollama pull codellama")
    print("   - Change model in the script and re-run!")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
