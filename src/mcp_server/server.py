"""
MCP Server Implementation using FastAPI
"""
import os
import json
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from .tools import TOOL_REGISTRY


# Request/Response Models
class ToolCallRequest(BaseModel):
    """Request model for tool calls"""
    tool_name: str
    parameters: Dict[str, Any] = {}


class ToolCallResponse(BaseModel):
    """Response model for tool calls"""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None


class ToolListResponse(BaseModel):
    """Response model for tool listing"""
    tools: List[Dict[str, Any]]


# Initialize FastAPI app
app = FastAPI(
    title="MCP Server",
    description="Model Context Protocol Server with Tools",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "MCP Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "/tools": "List all available tools",
            "/call": "Call a tool with parameters"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/tools", response_model=ToolListResponse)
async def list_tools():
    """
    List all available tools
    
    Returns:
        List of tools with their metadata
    """
    tools = []
    for tool_name, tool_info in TOOL_REGISTRY.items():
        tools.append({
            "name": tool_info["name"],
            "description": tool_info["description"],
            "parameters": tool_info["parameters"]
        })
    
    return ToolListResponse(tools=tools)


@app.post("/call", response_model=ToolCallResponse)
async def call_tool(request: ToolCallRequest):
    """
    Call a tool with specified parameters
    
    Args:
        request: Tool call request with tool name and parameters
        
    Returns:
        Tool execution result
    """
    tool_name = request.tool_name
    parameters = request.parameters
    
    # Check if tool exists
    if tool_name not in TOOL_REGISTRY:
        raise HTTPException(
            status_code=404,
            detail=f"Tool '{tool_name}' not found"
        )
    
    # Get tool function
    tool = TOOL_REGISTRY[tool_name]
    tool_function = tool["function"]
    
    # Execute tool
    try:
        if parameters:
            result = tool_function(**parameters)
        else:
            result = tool_function()
        
        return ToolCallResponse(
            success=True,
            result=result
        )
    except Exception as e:
        return ToolCallResponse(
            success=False,
            error=str(e)
        )


@app.get("/tool/{tool_name}")
async def get_tool_info(tool_name: str):
    """
    Get information about a specific tool
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Tool metadata
    """
    if tool_name not in TOOL_REGISTRY:
        raise HTTPException(
            status_code=404,
            detail=f"Tool '{tool_name}' not found"
        )
    
    tool = TOOL_REGISTRY[tool_name]
    return {
        "name": tool["name"],
        "description": tool["description"],
        "parameters": tool["parameters"]
    }


def start_server(host: str = None, port: int = None):
    """
    Start the MCP server
    
    Args:
        host: Host to bind to (default: from env or localhost)
        port: Port to bind to (default: from env or 8000)
    """
    host = host or os.getenv("MCP_SERVER_HOST", "localhost")
    port = port or int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting MCP Server")
    print(f"{'='*60}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"URL: http://{host}:{port}")
    print(f"Docs: http://{host}:{port}/docs")
    print(f"{'='*60}\n")
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
