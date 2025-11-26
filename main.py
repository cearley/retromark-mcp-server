#!/usr/bin/env python3
"""
Retromark - Universal MCP Server for Bookmark Management

Main entry point supporting two modes:
- MCP mode: Runs as an MCP server for AI assistants (Claude, Continue.dev, Amazon Q, etc.)
- CLI mode: Standalone command-line bookmark management interface
"""

import os
import sys
import argparse

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_mcp_server():
    """Start the MCP server for AI-assisted bookmark management.

    The server can be used with any MCP-compatible client including:
    - Claude Desktop
    - Claude Code
    - Continue.dev (VS Code/JetBrains)
    - Amazon Q CLI
    """
    from src.server import app
    print("Starting Retromark MCP Server...")
    app.run()

def start_cli():
    """Start the command-line interface."""
    from src.url_manager import main as url_manager_main
    url_manager_main()

def main():
    """Main entry point for the Retromark MCP Server."""
    parser = argparse.ArgumentParser(description="Retromark - Universal MCP Server for Bookmark Management")
    parser.add_argument("--mode", choices=["cli", "mcp"], default="cli",
                        help="Mode to run: 'mcp' for MCP server (Claude/Continue.dev/Amazon Q), 'cli' for standalone CLI")
    
    args = parser.parse_args()
    
    if args.mode == "mcp":
        start_mcp_server()
    else:
        start_cli()

if __name__ == "__main__":
    main()
