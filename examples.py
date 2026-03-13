"""
Example script demonstrating the agent capabilities
"""
from src.agent.agent import Agent


def main():
    """Run example demonstrations"""
    
    print("\n" + "="*70)
    print("🎯 Agent Examples")
    print("="*70 + "\n")
    
    # Create agent instance
    with Agent() as agent:
        
        # Example 1: Simple message
        print("\n📝 Example 1: Simple Message")
        print("-" * 70)
        result1 = agent.run("Process this simple text")
        
        # Example 2: Longer message
        print("\n📝 Example 2: Longer Message")
        print("-" * 70)
        result2 = agent.run(
            "This is a longer message that should trigger the complex decision path"
        )
        
        # Example 3: Using specific tools
        print("\n📝 Example 3: Direct Tool Usage")
        print("-" * 70)
        
        # Get current time
        time_result = agent.use_tool("get_current_time")
        
        # Analyze text
        text_result = agent.use_tool(
            "analyze_text",
            {"text": "The quick brown fox jumps over the lazy dog"}
        )
        
        # Perform calculation
        calc_result = agent.use_tool(
            "calculate",
            {"operation": "add", "a": 42, "b": 58}
        )
        
        print("\n" + "="*70)
        print("✅ Examples Complete")
        print("="*70 + "\n")


if __name__ == "__main__":
    main()
