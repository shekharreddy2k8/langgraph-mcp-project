"""
MCP Server Tools - Tool definitions for the MCP server
"""
from typing import Any, Dict
from datetime import datetime
import json


class MCPTools:
    """Collection of tools exposed by the MCP server"""
    
    @staticmethod
    def get_current_time() -> Dict[str, Any]:
        """
        Get the current time
        
        Returns:
            Dictionary with current time information
        """
        now = datetime.now()
        return {
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "timestamp": now.isoformat()
        }
    
    @staticmethod
    def calculate(operation: str, a: float, b: float) -> Dict[str, Any]:
        """
        Perform basic calculations
        
        Args:
            operation: Operation to perform (add, subtract, multiply, divide)
            a: First number
            b: Second number
            
        Returns:
            Dictionary with calculation result
        """
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero"
        }
        
        if operation not in operations:
            return {"error": f"Unknown operation: {operation}"}
        
        try:
            result = operations[operation](a, b)
            return {
                "operation": operation,
                "a": a,
                "b": b,
                "result": result
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def analyze_text(text: str) -> Dict[str, Any]:
        """
        Analyze text and return statistics
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with text analysis results
        """
        words = text.split()
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": text.count('.') + text.count('!') + text.count('?'),
            "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "unique_words": len(set(word.lower() for word in words))
        }
    
    @staticmethod
    def format_data(data: Dict[str, Any], format_type: str = "json") -> str:
        """
        Format data in different formats
        
        Args:
            data: Data to format
            format_type: Output format (json, pretty, compact)
            
        Returns:
            Formatted string
        """
        if format_type == "json":
            return json.dumps(data)
        elif format_type == "pretty":
            return json.dumps(data, indent=2, sort_keys=True)
        elif format_type == "compact":
            return json.dumps(data, separators=(',', ':'))
        else:
            return str(data)


# Tool registry for MCP server
TOOL_REGISTRY = {
    "get_current_time": {
        "name": "get_current_time",
        "description": "Get the current date and time",
        "parameters": {},
        "function": MCPTools.get_current_time
    },
    "calculate": {
        "name": "calculate",
        "description": "Perform basic mathematical calculations",
        "parameters": {
            "operation": {"type": "string", "description": "Operation: add, subtract, multiply, divide"},
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "function": MCPTools.calculate
    },
    "analyze_text": {
        "name": "analyze_text",
        "description": "Analyze text and return statistics",
        "parameters": {
            "text": {"type": "string", "description": "Text to analyze"}
        },
        "function": MCPTools.analyze_text
    },
    "format_data": {
        "name": "format_data",
        "description": "Format data in different formats",
        "parameters": {
            "data": {"type": "object", "description": "Data to format"},
            "format_type": {"type": "string", "description": "Format type: json, pretty, compact"}
        },
        "function": MCPTools.format_data
    }
}
