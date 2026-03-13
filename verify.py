#!/usr/bin/env python3
"""
Quick verification script to test all components
"""
import sys
import os
import httpx

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work"""
    print("🔍 Testing imports...")
    try:
        from src.graph.workflow import run_graph
        from src.agent.agent import Agent
        from src.mcp_server.tools import TOOL_REGISTRY
        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_graph():
    """Test graph execution"""
    print("\n🔍 Testing graph...")
    try:
        from src.graph.workflow import run_graph
        result = run_graph("verify")
        assert result["output"] is not None
        print(f"  ✅ Graph working: {result['decision']}")
        return True
    except Exception as e:
        print(f"  ❌ Graph failed: {e}")
        return False

def test_mcp_server():
    """Test MCP server"""
    print("\n🔍 Testing MCP server...")
    try:
        response = httpx.get("http://localhost:8000/health", timeout=2.0)
        if response.status_code == 200:
            print("  ✅ MCP server is running")
            
            # Test tools endpoint
            tools = httpx.get("http://localhost:8000/tools", timeout=2.0)
            tool_count = len(tools.json()["tools"])
            print(f"  ✅ Found {tool_count} tools")
            return True
        else:
            print(f"  ❌ Server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠️  MCP server not running: {e}")
        print("     Start with: python3 main.py --server")
        return False

def test_agent():
    """Test agent initialization"""
    print("\n🔍 Testing agent...")
    try:
        from src.agent.agent import Agent
        with Agent() as agent:
            print("  ✅ Agent initialized")
            return True
    except Exception as e:
        print(f"  ❌ Agent failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("\n" + "="*70)
    print("🧪 LangGraph MCP Project - Verification")
    print("="*70)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Graph", test_graph()))
    results.append(("MCP Server", test_mcp_server()))
    results.append(("Agent", test_agent()))
    
    print("\n" + "="*70)
    print("📊 Verification Results")
    print("="*70)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
    
    all_critical_passed = results[0][1] and results[1][1] and results[3][1]
    
    print("="*70)
    if all_critical_passed:
        print("🎉 All critical components verified!")
        if not results[2][1]:
            print("⚠️  Note: Start MCP server for full functionality")
        print("="*70 + "\n")
        return 0
    else:
        print("❌ Some components failed verification")
        print("="*70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
