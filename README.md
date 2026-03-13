# LangGraph MCP Agent Project

A Python project demonstrating LangGraph with simple nodes and edges, featuring an MCP (Model Context Protocol) server and an intelligent agent.

## Features

- **LangGraph Implementation**: Simple graph with custom nodes and edges
- **MCP Server**: Model Context Protocol server for tool integration
- **Agent**: Intelligent agent that uses the graph and MCP server

## Project Structure

```
langgraph-mcp-project/
├── src/
│   ├── agent/          # Agent implementation
│   ├── mcp_server/     # MCP server implementation
│   └── graph/          # LangGraph nodes and edges
├── tests/              # Test files
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── main.py            # Main entry point
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the MCP server:
```bash
python -m src.mcp_server.server
```

4. Run the agent:
```bash
python main.py
```

## Usage

The agent uses a LangGraph workflow with simple nodes:
- **input_node**: Processes initial input
- **processing_node**: Performs main logic
- **decision_node**: Makes decisions based on state
- **output_node**: Generates final output

The MCP server provides tools that the agent can use during execution.

## License

MIT
