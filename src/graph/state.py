"""
State definition for the LangGraph workflow
"""
from typing import TypedDict, List, Optional


class GraphState(TypedDict):
    """State object for the graph workflow"""
    input: str
    messages: List[str]
    processed_data: Optional[str]
    decision: Optional[str]
    output: Optional[str]
    iteration_count: int
