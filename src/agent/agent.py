"""
Agent implementation that uses LangGraph and MCP Server
"""
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from ..graph.workflow import run_graph
from .mcp_client import MCPClient


# Load environment variables
load_dotenv()


class Agent:
    """
    Intelligent agent that orchestrates LangGraph workflow and MCP tools
    """
    
    def __init__(self, mcp_server_url: str = None):
        """
        Initialize the agent
        
        Args:
            mcp_server_url: URL of the MCP server (optional)
        """
        self.mcp_client = MCPClient(mcp_server_url)
        self.conversation_history: List[Dict[str, str]] = []
        
        print("\n🤖 Agent Initialized")
        self._check_mcp_server()
    
    def _check_mcp_server(self):
        """Check if MCP server is available"""
        if self.mcp_client.health_check():
            print("✅ MCP Server is connected and healthy")
            tools = self.mcp_client.list_tools()
            print(f"📦 Available tools: {len(tools)}")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description']}")
        else:
            print("⚠️  MCP Server is not available. Tools will not be accessible.")
            print("   Start the server with: python -m src.mcp_server.server")
    
    def process_with_graph(self, user_input: str) -> Dict[str, Any]:
        """
        Process input using LangGraph workflow
        
        Args:
            user_input: User's input text
            
        Returns:
            Final state from graph execution
        """
        print(f"\n🔄 Processing with LangGraph workflow...")
        result = run_graph(user_input)
        return result
    
    def use_tool(self, tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use an MCP tool
        
        Args:
            tool_name: Name of the tool to use
            parameters: Tool parameters
            
        Returns:
            Tool execution result
        """
        print(f"\n🔧 Using tool: {tool_name}")
        if parameters:
            print(f"   Parameters: {parameters}")
        
        result = self.mcp_client.call_tool(tool_name, parameters)
        print(f"   Result: {result}")
        
        return result
    
    def run(self, user_input: str, use_tools: bool = True) -> Dict[str, Any]:
        """
        Main agent execution method
        
        Args:
            user_input: User's input
            use_tools: Whether to demonstrate tool usage
            
        Returns:
            Complete execution result
        """
        print(f"\n{'='*70}")
        print(f"🎯 Agent Execution Started")
        print(f"{'='*70}")
        print(f"Input: {user_input}\n")
        
        # Store in conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Step 1: Process with LangGraph
        graph_result = self.process_with_graph(user_input)
        
        # Step 2: Use MCP tools (optional demonstration)
        tool_results = {}
        if use_tools:
            print(f"\n{'─'*70}")
            print("🛠️  Demonstrating MCP Tool Usage")
            print(f"{'─'*70}\n")
            
            # Example tool calls
            tool_results["time"] = self.use_tool("get_current_time")
            
            tool_results["text_analysis"] = self.use_tool(
                "analyze_text",
                {"text": user_input}
            )
            
            if len(user_input.split()) > 0:
                word_count = len(user_input.split())
                tool_results["calculation"] = self.use_tool(
                    "calculate",
                    {"operation": "multiply", "a": word_count, "b": 2}
                )
        
        # Compile final result
        final_result = {
            "input": user_input,
            "graph_result": graph_result,
            "tool_results": tool_results,
            "output": graph_result.get("output", "No output generated")
        }
        
        # Store agent response in history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_result["output"]
        })
        
        print(f"\n{'='*70}")
        print(f"✅ Agent Execution Complete")
        print(f"{'='*70}\n")
        
        return final_result
    
    def run_interactive(self):
        """
        Run agent in interactive mode
        """
        print("\n" + "="*70)
        print("🤖 Interactive Agent Mode")
        print("="*70)
        print("Type 'exit' or 'quit' to stop")
        print("Type 'tools' to list available tools")
        print("Type 'history' to see conversation history")
        print("="*70 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'tools':
                    tools = self.mcp_client.list_tools()
                    print("\n📦 Available Tools:")
                    for tool in tools:
                        print(f"\n  • {tool['name']}")
                        print(f"    {tool['description']}")
                    print()
                    continue
                
                if user_input.lower() == 'history':
                    print("\n📜 Conversation History:")
                    for idx, msg in enumerate(self.conversation_history, 1):
                        role = msg['role'].title()
                        content = msg['content']
                        print(f"\n  {idx}. {role}: {content}")
                    print()
                    continue
                
                # Process with agent
                result = self.run(user_input)
                print(f"\nAgent: {result['output']}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    def close(self):
        """Clean up resources"""
        self.mcp_client.close()
        print("\n🔌 Agent closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
