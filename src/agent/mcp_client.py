"""
MCP Client for interacting with the MCP server
"""
import os
import httpx
from typing import Any, Dict, List, Optional


class MCPClient:
    """Client for interacting with MCP server"""
    
    def __init__(self, base_url: str = None):
        """
        Initialize MCP client
        
        Args:
            base_url: Base URL of the MCP server
        """
        host = os.getenv("MCP_SERVER_HOST", "localhost")
        port = os.getenv("MCP_SERVER_PORT", "8000")
        self.base_url = base_url or f"http://{host}:{port}"
        self.client = httpx.Client(timeout=30.0)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools from MCP server
        
        Returns:
            List of tool information
        """
        try:
            response = self.client.get(f"{self.base_url}/tools")
            response.raise_for_status()
            return response.json()["tools"]
        except Exception as e:
            print(f"Error listing tools: {e}")
            return []
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Call a tool on the MCP server
        
        Args:
            tool_name: Name of the tool to call
            parameters: Parameters for the tool
            
        Returns:
            Tool execution result
        """
        try:
            payload = {
                "tool_name": tool_name,
                "parameters": parameters or {}
            }
            
            response = self.client.post(f"{self.base_url}/call", json=payload)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                return result.get("result", {})
            else:
                print(f"Tool error: {result.get('error')}")
                return {"error": result.get("error")}
                
        except Exception as e:
            print(f"Error calling tool '{tool_name}': {e}")
            return {"error": str(e)}
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific tool
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool information or None if not found
        """
        try:
            response = self.client.get(f"{self.base_url}/tool/{tool_name}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting tool info: {e}")
            return None
    
    def health_check(self) -> bool:
        """
        Check if MCP server is healthy
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json().get("status") == "healthy"
        except Exception:
            return False
    
    def close(self):
        """Close the HTTP client"""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
