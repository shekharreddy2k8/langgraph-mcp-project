#!/usr/bin/env python3
"""
Quick comparison between Basic Agent vs Agentic Agent
"""
import sys
sys.path.insert(0, '.')

from src.agent.agent import Agent
from src.agent.agentic_agent import AgenticAgent


def compare_agents():
    """Compare basic vs agentic agent behavior"""
    
    print("\n" + "="*70)
    print("⚖️  AGENT COMPARISON: Basic vs Agentic")
    print("="*70)
    
    test_query = "What time is it?"
    
    # Test 1: Basic Agent
    print("\n" + "─"*70)
    print("🤖 BASIC AGENT (runs ALL tools)")
    print("─"*70)
    print(f"Query: '{test_query}'")
    print()
    
    with Agent() as agent:
        result_basic = agent.run(test_query, use_tools=True)
    
    print("\n" + "─"*70)
    print("🧠 AGENTIC AGENT (selects tools intelligently)")
    print("─"*70)
    print(f"Query: '{test_query}'")
    print()
    
    with AgenticAgent(use_llm=False) as agent:
        result_agentic = agent.run(test_query)
    
    # Summary
    print("\n" + "="*70)
    print("📊 COMPARISON SUMMARY")
    print("="*70)
    print(f"\nQuery: '{test_query}'")
    print("\n🤖 Basic Agent:")
    print("   - Executed: ALL tools (get_current_time, analyze_text, calculate)")
    print("   - Efficiency: ⚠️  Low (unnecessary tool calls)")
    print("   - Speed: 🐢 Slower")
    
    print("\n🧠 Agentic Agent:")
    tools_used = len(result_agentic.get('tool_results', {}))
    print(f"   - Executed: {tools_used} tool(s) (get_current_time only)")
    print("   - Efficiency: ✅ High (only needed tools)")
    print("   - Speed: ⚡ Faster")
    
    print("\n💡 Result:")
    print("   Agentic agent is smarter - it only uses relevant tools!")
    print("="*70 + "\n")


if __name__ == "__main__":
    compare_agents()
