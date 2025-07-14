#!/usr/bin/env python3
"""
Red Hat Search MCP Server

A Model Context Protocol (MCP) server that provides access to Red Hat's ecosystem catalog
using the REST search API. Includes optional Prometheus metrics for monitoring tool usage 
and performance.
"""

import logging

from mcp.server import FastMCP

from config import MCP_TRANSPORT
from metrics import start_metrics_thread, set_active_connections
from tools import register_tools
from database import search_service

# Get logger
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the MCP server"""
    # Initialize FastMCP server
    mcp = FastMCP("redhat-search-mcp")
    
    # Register all tools
    register_tools(mcp)
    
    # Start metrics server in background thread if enabled
    start_metrics_thread()
    
    # Run the MCP server
    try:
        logger.info("Starting Red Hat Search MCP Server")
        mcp.run(transport=MCP_TRANSPORT)
    except KeyboardInterrupt:
        logger.info("Shutting down MCP server...")
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        raise
    finally:
        # Clean up resources
        import asyncio
        asyncio.run(search_service.cleanup())
        
        # Clean up metrics
        set_active_connections(0)
        logger.info("MCP server shutdown complete")

if __name__ == "__main__":
    main() 