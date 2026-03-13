"""
Node implementations for the LangGraph workflow
"""
from typing import Dict, Any
from .state import GraphState


def input_node(state: GraphState) -> Dict[str, Any]:
    """
    Process initial input and prepare for workflow
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state dictionary
    """
    print(f"📥 Input Node: Received input - '{state['input']}'")
    
    messages = state.get("messages", [])
    messages.append(f"Input processed: {state['input']}")
    
    return {
        "messages": messages,
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def processing_node(state: GraphState) -> Dict[str, Any]:
    """
    Main processing logic node
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state dictionary
    """
    print(f"⚙️  Processing Node: Processing data...")
    
    input_text = state["input"]
    processed = f"Processed: {input_text.upper()} (length: {len(input_text)})"
    
    messages = state.get("messages", [])
    messages.append(f"Processing completed")
    
    return {
        "processed_data": processed,
        "messages": messages,
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def decision_node(state: GraphState) -> Dict[str, Any]:
    """
    Decision-making node based on current state
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state dictionary with decision
    """
    print(f"🤔 Decision Node: Making decision...")
    
    processed_data = state.get("processed_data", "")
    
    # Simple decision logic based on input length
    if len(state["input"]) > 20:
        decision = "complex"
    else:
        decision = "simple"
    
    messages = state.get("messages", [])
    messages.append(f"Decision made: {decision}")
    
    print(f"   Decision: {decision}")
    
    return {
        "decision": decision,
        "messages": messages,
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def output_node(state: GraphState) -> Dict[str, Any]:
    """
    Generate final output
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state dictionary with output
    """
    print(f"📤 Output Node: Generating output...")
    
    decision = state.get("decision", "unknown")
    processed = state.get("processed_data", "")
    
    output = f"Result: {processed} | Decision: {decision} | Iterations: {state.get('iteration_count', 0)}"
    
    messages = state.get("messages", [])
    messages.append("Output generated")
    
    print(f"   Output: {output}")
    
    return {
        "output": output,
        "messages": messages
    }


def error_node(state: GraphState) -> Dict[str, Any]:
    """
    Error handling node
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state dictionary with error info
    """
    print(f"❌ Error Node: Handling error...")
    
    messages = state.get("messages", [])
    messages.append("Error occurred, returning safe output")
    
    return {
        "output": "Error: Unable to process request",
        "messages": messages
    }
