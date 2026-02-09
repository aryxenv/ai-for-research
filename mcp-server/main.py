"""Azure AI Search MCP Server.

This server provides semantic search, hybrid search, text search, filtered search,
and document retrieval tools for AI agents using Azure AI Search.
"""

import os
import json
import sys
from typing import Any

from dotenv import load_dotenv
from mcp.server import Server
from mcp import types

from tools import (
    semantic_search,
    hybrid_search,
    text_search,
    filtered_search,
    fetch_document,
)


# Load environment variables from .env file
load_dotenv()

# Create MCP server instance
server = Server("azure-ai-search-mcp")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Return list of available tools."""
    return [
        types.Tool(
            name="semantic_search",
            description="Performs AI-powered semantic search that understands context and meaning. Works with or without semantic configuration - will use vectorizer if semantic configuration is not available.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "top": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 30)",
                        "default": 30,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="hybrid_search",
            description="Combines full-text and vector search for balanced results.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "top": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 30)",
                        "default": 30,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="text_search",
            description="Traditional keyword-based text search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "top": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 30)",
                        "default": 30,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="filtered_search",
            description="Search with OData filter expressions to narrow results.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "filter": {
                        "type": "string",
                        "description": "OData filter expression (e.g., \"category eq 'AI' and year ge 2020\")",
                    },
                    "top": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 30)",
                        "default": 30,
                    },
                },
                "required": ["query", "filter"],
            },
        ),
        types.Tool(
            name="fetch_document",
            description="Retrieve a specific document by its unique ID. Returns the complete document with all fields.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "The document's unique identifier",
                    },
                },
                "required": ["document_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(
    name: str,
    arguments: dict[str, Any],
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    if name == "semantic_search":
        result = semantic_search(
            query=arguments["query"],
            top=arguments.get("top", 30),
        )
    elif name == "hybrid_search":
        result = hybrid_search(
            query=arguments["query"],
            top=arguments.get("top", 30),
        )
    elif name == "text_search":
        result = text_search(
            query=arguments["query"],
            top=arguments.get("top", 30),
        )
    elif name == "filtered_search":
        result = filtered_search(
            query=arguments["query"],
            filter=arguments["filter"],
            top=arguments.get("top", 30),
        )
    elif name == "fetch_document":
        result = fetch_document(
            document_id=arguments["document_id"],
        )
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [
        types.TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False),
        )
    ]


async def main() -> None:
    """Run the MCP server."""
    # Validate required environment variables
    required_vars = [
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_API_KEY",
        "AZURE_SEARCH_INDEX_NAME",
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(
            f"Error: Missing required environment variables: {', '.join(missing_vars)}",
            file=sys.stderr,
        )
        sys.exit(1)

    async with server:
        print("Azure AI Search MCP Server running", file=sys.stderr)
        # Server will handle stdio communication


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
