#!/usr/bin/env bash
# -------------------------------------------------------
# Start mcpo proxy for OpenWebUI, connecting to the cloud MCP server
#
# Starts mcpo proxy that connects to the cloud-hosted MCP server
# (configured in mcpo-config.json) and exposes an OpenAPI endpoint
# for OpenWebUI.
#
# After starting, add in OpenWebUI:
#   Admin Panel > Settings > Tools > OpenAPI Servers > Add Connection
#   URL  : http://localhost:<MCPO_PORT>/azure-ai-search
#   Key  : <API_KEY>
# -------------------------------------------------------
set -euo pipefail

MCPO_PORT="${1:-8001}"
API_KEY="${2:-top-secret}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "================================================"
echo "  Azure AI Search MCP - OpenWebUI (via mcpo)"
echo "  mcpo endpoint : http://localhost:$MCPO_PORT"
echo "  Tools docs    : http://localhost:$MCPO_PORT/azure-ai-search/docs"
echo "================================================"
echo ""
echo "Add to OpenWebUI -> Admin -> Settings -> Tools -> OpenAPI Servers:"
echo "  URL : http://localhost:$MCPO_PORT/azure-ai-search"
echo "  Key : $API_KEY"
echo ""

echo "Starting mcpo proxy (port $MCPO_PORT)..."
if [ -n "$API_KEY" ]; then
    mcpo --port "$MCPO_PORT" --api-key "$API_KEY" --config mcpo-config.json
else
    mcpo --port "$MCPO_PORT" --config mcpo-config.json
fi
