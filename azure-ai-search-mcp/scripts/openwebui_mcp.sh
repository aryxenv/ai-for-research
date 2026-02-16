#!/usr/bin/env bash
# -------------------------------------------------------
# Start Azure AI Search MCP server + mcpo proxy for OpenWebUI
#
# 1. Launches the MCP server with streamable-http transport.
# 2. Starts mcpo proxy that connects to it over streamable-http
#    and exposes an OpenAPI endpoint for OpenWebUI.
#
# After starting, add in OpenWebUI:
#   Admin Panel > Settings > Tools > OpenAPI Servers > Add Connection
#   URL  : http://localhost:<MCPO_PORT>/azure-ai-search
#   Key  : <API_KEY>
# -------------------------------------------------------
set -euo pipefail

MCP_PORT="${1:-8000}"
MCPO_PORT="${2:-8000}"
API_KEY="${3:-top-secret}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "================================================"
echo "  Azure AI Search MCP - OpenWebUI (via mcpo)"
echo "  MCP server    : http://localhost:$MCP_PORT/mcp"
echo "  mcpo endpoint : http://localhost:$MCPO_PORT"
echo "  Tools docs    : http://localhost:$MCPO_PORT/azure-ai-search/docs"
echo "================================================"
echo ""
echo "Add to OpenWebUI -> Admin -> Settings -> Tools -> OpenAPI Servers:"
echo "  URL : http://localhost:$MCPO_PORT/azure-ai-search"
echo "  Key : $API_KEY"
echo ""

# 1. Start the MCP server in the background
echo "Starting MCP server (streamable-http on port $MCP_PORT)..."
uv run python main.py --transport streamable-http --host 127.0.0.1 --port "$MCP_PORT" &
MCP_PID=$!

# Clean up MCP server on exit
trap "kill $MCP_PID 2>/dev/null" EXIT

# Give it a moment to start
sleep 3

# 2. Start mcpo pointing at the running MCP server
echo "Starting mcpo proxy (port $MCPO_PORT)..."
if [ -n "$API_KEY" ]; then
    mcpo --port "$MCPO_PORT" --api-key "$API_KEY" --config mcpo-config.json
else
    mcpo --port "$MCPO_PORT" --config mcpo-config.json
fi
