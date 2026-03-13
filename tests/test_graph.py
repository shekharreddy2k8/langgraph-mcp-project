"""
Test suite for the project
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.graph.workflow import run_graph
from src.graph.state import GraphState


def test_graph_simple_input():
    """Test graph with simple input"""
    print("\n🧪 Test 1: Simple Input")
    print("-" * 60)
    
    result = run_graph("test")
    
    assert result["input"] == "test", f"Expected input 'test', got {result['input']}"
    assert result["output"] is not None, "Output should not be None"
    assert result["decision"] == "simple", f"Expected decision 'simple', got {result['decision']}"
    assert "TEST" in result["processed_data"], f"Expected 'TEST' in processed_data, got {result['processed_data']}"
    
    print("✅ Test 1 passed")


def test_graph_complex_input():
    """Test graph with complex input"""
    print("\n🧪 Test 2: Complex Input")
    print("-" * 60)
    
    result = run_graph("This is a much longer test input that should be complex")
    
    assert result["decision"] == "complex"
    assert result["output"] is not None
    
    print("✅ Test 2 passed")


def test_graph_state():
    """Test graph state management"""
    print("\n🧪 Test 3: State Management")
    print("-" * 60)
    
    result = run_graph("state test")
    
    assert isinstance(result["messages"], list)
    assert len(result["messages"]) > 0
    assert result["iteration_count"] > 0
    
    print("✅ Test 3 passed")


def run_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 Running Tests")
    print("="*70)
    
    try:
        test_graph_simple_input()
        test_graph_complex_input()
        test_graph_state()
        
        print("\n" + "="*70)
        print("✅ All Tests Passed!")
        print("="*70 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during testing: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
