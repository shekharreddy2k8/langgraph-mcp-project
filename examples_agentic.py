"""
Example demonstrating the Agentic Agent that intelligently chooses tools
"""
from src.agent.agentic_agent import AgenticAgent


def main():
    """Run agentic agent demonstrations"""
    
    print("\n" + "="*70)
    print("🎯 Agentic Agent Examples")
    print("="*70)
    print("The agent will intelligently choose which tools to use!\n")
    
    # Create agentic agent instance
    with AgenticAgent() as agent:
        
        # Example 1: Time-related query
        print("\n📝 Example 1: Time Query")
        print("-" * 70)
        result1 = agent.run("What time is it right now?")
        print(f"\nResponse: {result1['output']}")
        
        # Example 2: Math calculation
        print("\n📝 Example 2: Math Calculation")
        print("-" * 70)
        result2 = agent.run("Can you add 42 and 58 for me?")
        print(f"\nResponse: {result2['output']}")
        
        # Example 3: Text analysis
        print("\n📝 Example 3: Text Analysis")
        print("-" * 70)
        result3 = agent.run("Analyze this text: The quick brown fox jumps over the lazy dog")
        print(f"\nResponse: {result3['output']}")
        
        # Example 4: Multiple tools
        print("\n📝 Example 4: Multiple Tools")
        print("-" * 70)
        result4 = agent.run("What's the time and can you multiply 7 times 8?")
        print(f"\nResponse: {result4['output']}")
        
        # Example 5: No tools needed
        print("\n📝 Example 5: No Tools Needed")
        print("-" * 70)
        result5 = agent.run("Hello, how are you?")
        print(f"\nResponse: {result5['output']}")
        
        # Example 6: Complex query
        print("\n📝 Example 6: Complex Query")
        print("-" * 70)
        result6 = agent.run("I need to know what 125 divided by 5 equals, and also tell me the current date")
        print(f"\nResponse: {result6['output']}")
        
        print("\n" + "="*70)
        print("✅ Agentic Examples Complete")
        print("="*70 + "\n")


if __name__ == "__main__":
    main()
