"""
LangGraph workflow builder
"""
from langgraph.graph import StateGraph, END
from .state import GraphState
from .nodes import input_node, processing_node, decision_node, output_node, error_node
from .edges import route_after_decision


def create_graph():
    """
    Create and configure the LangGraph workflow
    
    Returns:
        Compiled graph ready for execution
    """
    # Initialize the graph with our state
    workflow = StateGraph(GraphState)
    
    # Add nodes to the graph
    workflow.add_node("input_node", input_node)
    workflow.add_node("processing_node", processing_node)
    workflow.add_node("decision_node", decision_node)
    workflow.add_node("output_node", output_node)
    workflow.add_node("error_node", error_node)
    
    # Set the entry point
    workflow.set_entry_point("input_node")
    
    # Add edges (connections between nodes)
    workflow.add_edge("input_node", "processing_node")
    workflow.add_edge("processing_node", "decision_node")
    
    # Add conditional edge based on decision
    workflow.add_conditional_edges(
        "decision_node",
        route_after_decision,
        {
            "output_node": "output_node",
            "error_node": "error_node"
        }
    )
    
    # Both output and error nodes lead to END
    workflow.add_edge("output_node", END)
    workflow.add_edge("error_node", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_graph(user_input: str):
    """
    Execute the graph with given input
    
    Args:
        user_input: Input string to process
        
    Returns:
        Final state after graph execution
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting LangGraph Workflow")
    print(f"{'='*60}\n")
    
    # Create the graph
    app = create_graph()
    
    # Initialize state
    initial_state = GraphState(
        input=user_input,
        messages=[],
        processed_data=None,
        decision=None,
        output=None,
        iteration_count=0
    )
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    print(f"\n{'='*60}")
    print(f"✅ Workflow Complete")
    print(f"{'='*60}\n")
    
    return final_state
