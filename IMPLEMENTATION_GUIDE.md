# LangGraph MCP Agent Project - Complete Implementation Guide

## 📋 Overview

This project demonstrates a complete implementation of:
- **LangGraph**: State-based workflow with nodes and edges
- **MCP Server**: Model Context Protocol server with tool integration
- **Intelligent Agent**: Orchestrates graph workflows and tool usage
- **Testing**: Comprehensive test suite

## 🏗️ Architecture

### Components

1. **Graph Layer** (`src/graph/`)
   - **state.py**: Defines the graph state structure
   - **nodes.py**: Implements processing nodes
   - **edges.py**: Defines routing logic
   - **workflow.py**: Assembles and executes the graph

2. **MCP Server** (`src/mcp_server/`)
   - **server.py**: FastAPI-based MCP server
   - **tools.py**: Tool implementations and registry

3. **Agent** (`src/agent/`)
   - **agent.py**: Intelligent agent orchestrating workflows
   - **mcp_client.py**: HTTP client for MCP server communication

## 🚀 Quick Start

### 1. Setup

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
```

### 3. Start MCP Server

In terminal 1:
```bash
python3 main.py --server
```

The server will start at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 4. Run Agent

In terminal 2:

```bash
# Interactive mode
python3 main.py --interactive

# Single message
python3 main.py --message "Process this text"

# Test graph only
python3 main.py --test-graph "Test input"

# Run examples
python3 examples.py
```

## 📊 Graph Workflow

The LangGraph workflow consists of:

```
START → input_node → processing_node → decision_node → output_node → END
                                              ↓
                                         error_node → END
```

### Node Functions

- **input_node**: Validates and prepares input
- **processing_node**: Transforms input data
- **decision_node**: Makes routing decisions based on state
- **output_node**: Generates final output
- **error_node**: Handles errors gracefully

### State Management

```python
GraphState = {
    "input": str,           # Original input
    "messages": List[str],  # Processing history
    "processed_data": str,  # Transformed data
    "decision": str,        # Routing decision
    "output": str,          # Final output
    "iteration_count": int  # Track iterations
}
```

## 🛠️ MCP Tools

Available tools from MCP server:

### 1. get_current_time()
Returns current date, time, and timestamp.

```python
agent.use_tool("get_current_time")
# Returns: {"time": "14:30:45", "date": "2026-03-12", "timestamp": "..."}
```

### 2. calculate(operation, a, b)
Performs basic arithmetic operations.

```python
agent.use_tool("calculate", {
    "operation": "add",  # add, subtract, multiply, divide
    "a": 10,
    "b": 5
})
# Returns: {"operation": "add", "a": 10, "b": 5, "result": 15}
```

### 3. analyze_text(text)
Analyzes text statistics.

```python
agent.use_tool("analyze_text", {"text": "Hello World"})
# Returns: {
#   "character_count": 11,
#   "word_count": 2,
#   "sentence_count": 0,
#   "average_word_length": 5.5,
#   "unique_words": 2
# }
```

### 4. format_data(data, format_type)
Formats data in various formats.

```python
agent.use_tool("format_data", {
    "data": {"key": "value"},
    "format_type": "pretty"  # json, pretty, compact
})
```

## 🤖 Agent Usage

### Programmatic Usage

```python
from src.agent.agent import Agent

# Create agent instance
with Agent() as agent:
    # Run with message
    result = agent.run("Process this text")
    print(result['output'])
    
    # Use specific tool
    time = agent.use_tool("get_current_time")
    
    # Interactive mode
    agent.run_interactive()
```

### Interactive Commands

When in interactive mode:
- Type any message to process
- `tools` - List available tools
- `history` - Show conversation history
- `exit` or `quit` - Exit interactive mode

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python3 tests/test_graph.py

# Test specific component
python3 -c "from src.graph.workflow import run_graph; print(run_graph('test'))"
```

### Test Coverage

- ✅ Simple input processing
- ✅ Complex input handling
- ✅ State management
- ✅ Decision routing
- ✅ Error handling

## 📁 Project Structure

```
langgraph-mcp-project/
├── src/
│   ├── __init__.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py           # Main agent implementation
│   │   └── mcp_client.py      # MCP HTTP client
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py           # State definition
│   │   ├── nodes.py           # Node implementations
│   │   ├── edges.py           # Edge routing logic
│   │   └── workflow.py        # Graph builder
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py          # FastAPI server
│       └── tools.py           # Tool implementations
├── tests/
│   ├── __init__.py
│   └── test_graph.py          # Test suite
├── main.py                    # Main entry point
├── examples.py                # Example usage
├── requirements.txt           # Dependencies
├── setup.sh                   # Setup script
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

## 🔧 API Endpoints

### MCP Server Endpoints

- `GET /` - Server info
- `GET /health` - Health check
- `GET /tools` - List all tools
- `POST /call` - Call a tool
- `GET /tool/{tool_name}` - Get tool info

### Example API Calls

```bash
# List tools
curl http://localhost:8000/tools

# Call a tool
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_current_time", "parameters": {}}'

# Health check
curl http://localhost:8000/health
```

## 🎯 Use Cases

1. **Text Processing Pipeline**
   - Input validation → Processing → Decision making → Output

2. **Tool Integration**
   - Use MCP tools for calculations, text analysis, formatting

3. **Interactive Chat**
   - Multi-turn conversations with state management

4. **Workflow Automation**
   - Custom node implementations for specific tasks

## 📝 Adding Custom Tools

Add new tools to `src/mcp_server/tools.py`:

```python
@staticmethod
def my_custom_tool(param1: str, param2: int) -> Dict[str, Any]:
    """
    My custom tool description
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Dictionary with results
    """
    return {
        "result": f"{param1} processed {param2} times"
    }

# Add to TOOL_REGISTRY
TOOL_REGISTRY["my_custom_tool"] = {
    "name": "my_custom_tool",
    "description": "My custom tool description",
    "parameters": {
        "param1": {"type": "string", "description": "..."},
        "param2": {"type": "number", "description": "..."}
    },
    "function": MCPTools.my_custom_tool
}
```

## 📈 Extending the Graph

Add custom nodes to `src/graph/nodes.py`:

```python
def custom_node(state: GraphState) -> Dict[str, Any]:
    """Custom processing node"""
    # Your logic here
    return {
        "custom_data": "processed",
        "messages": state.get("messages", []) + ["Custom step"]
    }
```

Update `src/graph/workflow.py`:

```python
workflow.add_node("custom_node", custom_node)
workflow.add_edge("processing_node", "custom_node")
workflow.add_edge("custom_node", "decision_node")
```

## 🐛 Troubleshooting

### MCP Server Not Starting

```bash
# Check if port is in use
lsof -i :8000

# Try different port
MCP_SERVER_PORT=8001 python3 main.py --server
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Permission Errors

```bash
# Make scripts executable
chmod +x setup.sh
```

## 📚 Dependencies

- **langgraph** >= 0.2.0 - Graph-based workflow framework
- **langchain** >= 0.1.0 - LLM framework
- **langchain-openai** >= 0.0.5 - OpenAI integration
- **mcp** >= 0.9.0 - Model Context Protocol
- **pydantic** >= 2.0.0 - Data validation
- **python-dotenv** >= 1.0.0 - Environment variables
- **uvicorn** >= 0.27.0 - ASGI server
- **fastapi** >= 0.109.0 - Web framework
- **httpx** >= 0.26.0 - HTTP client

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 💡 Tips

1. **Start MCP server first** before running agent
2. **Use virtual environment** to isolate dependencies
3. **Check logs** in server terminal for debugging
4. **Test individual components** before full integration
5. **Add error handling** in custom nodes

## 🎓 Learning Path

1. ✅ Understand basic graph workflow
2. ✅ Learn node and edge concepts
3. ✅ Explore MCP server tools
4. ✅ Use agent for orchestration
5. 🔄 Add custom tools and nodes
6. 🔄 Build complex workflows

---

**Happy Building! 🚀**
