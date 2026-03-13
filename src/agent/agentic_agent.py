"""
Agentic Agent - Intelligently chooses tools based on user input
"""
import os
import json
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from ..graph.workflow import run_graph
from .mcp_client import MCPClient

# Load environment variables
load_dotenv()


class AgenticAgent:
    """
    Intelligent agent that autonomously decides which tools to use based on user input
    """
    
    def __init__(self, mcp_server_url: str = None, use_llm: bool = True):
        """
        Initialize the agentic agent
        
        Args:
            mcp_server_url: URL of the MCP server (optional)
            use_llm: Whether to use LLM for tool selection (requires OpenAI API key)
        """
        self.mcp_client = MCPClient(mcp_server_url)
        self.conversation_history: List[Dict[str, str]] = []
        self.use_llm = use_llm
        self.llm_client = None
        
        # Initialize LLM if available
        if use_llm:
            try:
                from openai import OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key and api_key != "your_openai_api_key_here":
                    self.llm_client = OpenAI(api_key=api_key)
                    print("\n🤖 Agentic Agent Initialized (with LLM)")
                else:
                    print("\n🤖 Agentic Agent Initialized (rule-based mode)")
                    print("⚠️  OPENAI_API_KEY not set - using rule-based tool selection")
                    self.use_llm = False
            except ImportError:
                print("\n🤖 Agentic Agent Initialized (rule-based mode)")
                print("⚠️  OpenAI not installed - using rule-based tool selection")
                print("   Install with: pip install openai")
                self.use_llm = False
        else:
            print("\n🤖 Agentic Agent Initialized (rule-based mode)")
        
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
    
    def _get_tool_descriptions(self) -> str:
        """Get formatted tool descriptions for LLM"""
        tools = self.mcp_client.list_tools()
        descriptions = []
        for tool in tools:
            params = tool.get('parameters', {})
            param_str = json.dumps(params) if params else "no parameters"
            descriptions.append(f"- {tool['name']}: {tool['description']}\n  Parameters: {param_str}")
        return "\n".join(descriptions)
    
    def _select_tools_with_llm(self, user_input: str) -> List[Dict[str, Any]]:
        """
        Use LLM to decide which tools to call
        
        Args:
            user_input: User's message
            
        Returns:
            List of tool calls with parameters
        """
        if not self.llm_client:
            return self._select_tools_with_rules(user_input)
        
        tools_desc = self._get_tool_descriptions()
        
        system_prompt = f"""You are an intelligent agent that decides which tools to use based on user requests.

Available tools:
{tools_desc}

Analyze the user's request and decide which tools to call. Return a JSON array of tool calls.
Each tool call should have:
- "tool_name": the name of the tool
- "parameters": object with required parameters (empty object if no parameters needed)
- "reasoning": brief explanation of why this tool is needed

If no tools are needed, return an empty array.

Example response:
[
  {{
    "tool_name": "get_current_time",
    "parameters": {{}},
    "reasoning": "User asked about the current time"
  }},
  {{
    "tool_name": "calculate",
    "parameters": {{"operation": "add", "a": 5, "b": 3}},
    "reasoning": "User wants to add 5 and 3"
  }}
]

Return ONLY the JSON array, no other text."""

        try:
            print("\n🧠 Using LLM to select tools...")
            response = self.llm_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.1
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse JSON response
            if result.startswith("```json"):
                result = result[7:-3].strip()
            elif result.startswith("```"):
                result = result[3:-3].strip()
            
            tool_calls = json.loads(result)
            
            if tool_calls:
                print(f"   Selected {len(tool_calls)} tool(s)")
                for tc in tool_calls:
                    print(f"   - {tc['tool_name']}: {tc['reasoning']}")
            else:
                print("   No tools selected")
            
            return tool_calls
            
        except Exception as e:
            print(f"⚠️  LLM tool selection failed: {e}")
            print("   Falling back to rule-based selection")
            return self._select_tools_with_rules(user_input)
    
    def _select_tools_with_rules(self, user_input: str) -> List[Dict[str, Any]]:
        """
        Rule-based tool selection (fallback when LLM is not available)
        
        Args:
            user_input: User's message
            
        Returns:
            List of tool calls with parameters
        """
        print("\n🔍 Using rule-based tool selection...")
        input_lower = user_input.lower()
        tool_calls = []
        
        # Time-related keywords
        if any(word in input_lower for word in ['time', 'date', 'when', 'clock', 'today']):
            tool_calls.append({
                "tool_name": "get_current_time",
                "parameters": {},
                "reasoning": "User mentioned time/date keywords"
            })
        
        # Math-related keywords
        math_ops = {
            'add': ['add', 'plus', 'sum', '+'],
            'subtract': ['subtract', 'minus', 'difference', '-'],
            'multiply': ['multiply', 'times', 'product', '*', 'x'],
            'divide': ['divide', 'divided by', '/', '÷']
        }
        
        for operation, keywords in math_ops.items():
            if any(kw in input_lower for kw in keywords):
                # Try to extract numbers
                import re
                numbers = re.findall(r'\d+\.?\d*', user_input)
                if len(numbers) >= 2:
                    tool_calls.append({
                        "tool_name": "calculate",
                        "parameters": {
                            "operation": operation,
                            "a": float(numbers[0]),
                            "b": float(numbers[1])
                        },
                        "reasoning": f"User wants to {operation} numbers"
                    })
                break
        
        # Text analysis keywords
        if any(word in input_lower for word in ['analyze', 'count', 'words', 'characters', 'statistics', 'stats']):
            # Extract text to analyze (could be improved)
            tool_calls.append({
                "tool_name": "analyze_text",
                "parameters": {"text": user_input},
                "reasoning": "User wants text analysis"
            })
        
        # Format keywords
        if any(word in input_lower for word in ['format', 'json', 'pretty']):
            # This would need data to format
            pass
        
        if tool_calls:
            print(f"   Selected {len(tool_calls)} tool(s):")
            for tc in tool_calls:
                print(f"   - {tc['tool_name']}: {tc['reasoning']}")
        else:
            print("   No tools selected")
        
        return tool_calls
    
    def _execute_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute selected tool calls
        
        Args:
            tool_calls: List of tool calls to execute
            
        Returns:
            Dictionary of tool results
        """
        if not tool_calls:
            return {}
        
        print(f"\n{'─'*70}")
        print("🛠️  Executing Selected Tools")
        print(f"{'─'*70}\n")
        
        results = {}
        for tool_call in tool_calls:
            tool_name = tool_call["tool_name"]
            parameters = tool_call.get("parameters", {})
            
            print(f"🔧 Using tool: {tool_name}")
            if parameters:
                print(f"   Parameters: {parameters}")
            print(f"   Reason: {tool_call.get('reasoning', 'N/A')}")
            
            result = self.mcp_client.call_tool(tool_name, parameters)
            results[tool_name] = result
            print(f"   Result: {result}\n")
        
        return results
    
    def _generate_response_with_llm(self, user_input: str, graph_result: Dict, tool_results: Dict) -> str:
        """
        Generate natural language response using LLM
        
        Args:
            user_input: Original user input
            graph_result: Result from graph workflow
            tool_results: Results from tool execution
            
        Returns:
            Natural language response
        """
        if not self.llm_client:
            # Simple response without LLM
            response_parts = [f"Graph output: {graph_result.get('output', 'N/A')}"]
            if tool_results:
                response_parts.append(f"Tool results: {json.dumps(tool_results, indent=2)}")
            return "\n".join(response_parts)
        
        try:
            context = {
                "graph_output": graph_result.get('output'),
                "tool_results": tool_results
            }
            
            system_prompt = """You are a helpful AI assistant. Generate a natural, conversational response based on the workflow results and tool outputs provided. Be concise and friendly."""
            
            user_prompt = f"""User asked: {user_input}

Workflow result: {graph_result.get('output')}

Tool results:
{json.dumps(tool_results, indent=2)}

Please provide a helpful response to the user."""
            
            response = self.llm_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️  Response generation failed: {e}")
            return f"Graph: {graph_result.get('output')}\nTools: {json.dumps(tool_results)}"
    
    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Main agentic execution - intelligently selects and uses tools
        
        Args:
            user_input: User's input
            
        Returns:
            Complete execution result
        """
        print(f"\n{'='*70}")
        print(f"🎯 Agentic Agent Execution Started")
        print(f"{'='*70}")
        print(f"Input: {user_input}\n")
        
        # Store in conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Step 1: Process with LangGraph
        print(f"🔄 Processing with LangGraph workflow...")
        graph_result = run_graph(user_input)
        
        # Step 2: Intelligently select tools
        tool_calls = (self._select_tools_with_llm(user_input) 
                     if self.use_llm 
                     else self._select_tools_with_rules(user_input))
        
        # Step 3: Execute selected tools
        tool_results = self._execute_tool_calls(tool_calls)
        
        # Step 4: Generate response
        if self.use_llm and self.llm_client:
            final_output = self._generate_response_with_llm(user_input, graph_result, tool_results)
        else:
            final_output = graph_result.get("output", "No output generated")
            if tool_results:
                final_output += f"\n\nTool results: {json.dumps(tool_results, indent=2)}"
        
        # Compile final result
        final_result = {
            "input": user_input,
            "graph_result": graph_result,
            "tool_calls": tool_calls,
            "tool_results": tool_results,
            "output": final_output
        }
        
        # Store agent response in history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_output
        })
        
        print(f"\n{'='*70}")
        print(f"✅ Agentic Agent Execution Complete")
        print(f"{'='*70}\n")
        
        return final_result
    
    def run_interactive(self):
        """
        Run agent in interactive mode
        """
        print("\n" + "="*70)
        print("🤖 Interactive Agentic Agent Mode")
        print("="*70)
        print("I'll intelligently choose which tools to use based on your input!")
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
                
                # Process with agentic agent
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
        print("\n🔌 Agentic Agent closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
