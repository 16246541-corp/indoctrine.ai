"""
Demo: Test LM Studio local LLM with Agent Indoctrination.

Prerequisites:
1. Install LM Studio: https://lmstudio.ai/
2. Load a model in LM Studio
3. Start the local server (usually on port 1234)
4. Verify: curl http://localhost:1234/v1/models

Then run this script!
"""

from agent_indoctrination import Indoctrinator
from agent_indoctrination.core.local_llm_adapters import LMStudioAgent
from agent_indoctrination.cli.nyan_progress import run_with_nyan_progress


def main():
    print("=" * 70)
    print("🎨 LM STUDIO LOCAL LLM - INDOCTRINATION TEST")
    print("=" * 70)
    print("\nTesting your LM Studio model with the indoctrination framework!\n")
    
    # Step 1: Create LM Studio agent
    print("📝 Step 1: Connecting to LM Studio...")
    print("   Endpoint: http://localhost:1234")
    
    try:
        agent = LMStudioAgent()
        
        # Quick connectivity test
        print("\n🧪 Testing connection...")
        test_response = agent.send_message("Say 'Hello' in one word.")
        print(f"   Response: {test_response}")
        agent.reset()
        
        if not test_response or "error" in test_response.lower():
            print("\n❌ Cannot connect to LM Studio!")
            print("   1. Open LM Studio")
            print("   2. Load a model")
            print("   3. Click 'Start Server' in the Local Server tab")
            return
        
        print("✅ LM Studio connection successful!\n")
        
    except Exception as e:
        print(f"\n❌ Error connecting to LM Studio: {e}")
        print("   Make sure LM Studio server is running on port 1234")
        return
    
    # Step 2: Initialize framework
    print("📝 Step 2: Initializing Indoctrination Framework...")
    
    try:
        indoctrinator = Indoctrinator(config_path="config/examples/lmstudio.yaml")
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
    print(f"🎨 Server: LM Studio")
    
    # Step 5: Generate report
    print("\n📝 Step 5: Generating Report...")
    
    try:
        report_path = indoctrinator.generate_report(
            results_dict,
            format="markdown",
            output_path="lmstudio_test_report.md"
        )
        print(f"✅ Report: {report_path}")
        
        json_path = indoctrinator.generate_report(
            results_dict,
            format="json",
            output_path="lmstudio_test_results.json"
        )
        print(f"✅ JSON: {json_path}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 LM STUDIO TEST COMPLETE!")
    print("=" * 70)
    print("\n📁 Generated Files:")
    print("   - lmstudio_test_report.md")
    print("   - lmstudio_test_results.json")
    print("\n💡 Tips:")
    print("   - Try different models in LM Studio")
    print("   - Adjust temperature and parameters")
    print("   - Compare results across models")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
