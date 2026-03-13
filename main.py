"""
Main entry point for the LangGraph MCP Agent project
"""
import sys
import argparse
from src.agent.agent import Agent
from src.mcp_server.server import start_server


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="LangGraph MCP Agent Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run agent with a message
  python main.py --message "Hello, world!"
  
  # Run interactive agent
  python main.py --interactive
  
  # Start MCP server
  python main.py --server
  
  # Test graph only
  python main.py --test-graph "Test input"
        """
    )
    
    parser.add_argument(
        "--message", "-m",
        type=str,
        help="Process a single message with the agent"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run agent in interactive mode"
    )
    
    parser.add_argument(
        "--server", "-s",
        action="store_true",
        help="Start the MCP server"
    )
    
    parser.add_argument(
        "--test-graph", "-t",
        type=str,
        help="Test the LangGraph workflow with input"
    )
    
    parser.add_argument(
        "--no-tools",
        action="store_true",
        help="Run agent without demonstrating tool usage"
    )
    
    args = parser.parse_args()
    
    # Start MCP server
    if args.server:
        print("🚀 Starting MCP Server...")
        start_server()
        return
    
    # Test graph only
    if args.test_graph:
        from src.graph.workflow import run_graph
        print("🧪 Testing LangGraph workflow...")
        result = run_graph(args.test_graph)
        print(f"\nFinal Output: {result.get('output')}")
        return
    
    # Run agent with message
    if args.message:
        print("🤖 Running Agent with message...")
        with Agent() as agent:
            result = agent.run(args.message, use_tools=not args.no_tools)
            print(f"\n{'='*70}")
            print("📊 Final Result Summary")
            print(f"{'='*70}")
            print(f"Input: {result['input']}")
            print(f"Output: {result['output']}")
            print(f"{'='*70}\n")
        return
    
    # Run interactive mode
    if args.interactive:
        with Agent() as agent:
            agent.run_interactive()
        return
    
    # Default: Show help and run a demo
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n" + "="*70)
        print("🎬 Running Demo")
        print("="*70 + "\n")
        
        demo_message = "Hello from LangGraph MCP Agent!"
        print(f"Demo message: '{demo_message}'\n")
        
        with Agent() as agent:
            result = agent.run(demo_message)
            print(f"\n{'='*70}")
            print("📊 Demo Complete")
            print(f"{'='*70}")
            print(f"Output: {result['output']}")
            print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
