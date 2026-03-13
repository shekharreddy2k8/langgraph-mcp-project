"""
Edge definitions and routing logic for the LangGraph workflow
"""
from typing import Literal
from .state import GraphState


def route_after_decision(state: GraphState) -> Literal["output_node", "error_node"]:
    """
    Route to the next node based on decision
    
    Args:
        state: Current graph state
        
    Returns:
        Name of the next node to execute
    """
    decision = state.get("decision", "")
    
    # Route based on decision
    if decision in ["simple", "complex"]:
        return "output_node"
    else:
        return "error_node"


def should_continue(state: GraphState) -> Literal["continue", "end"]:
    """
    Determine if workflow should continue or end
    
    Args:
        state: Current graph state
        
    Returns:
        'continue' or 'end'
    """
    # Check if we have output
    if state.get("output"):
        return "end"
    return "continue"
