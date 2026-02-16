#!/usr/bin/env bash
# -------------------------------------------------------
# Start Azure AI Search MCP server in DEVELOPMENT mode
# Uses MCP Inspector (browser UI) with streamable-http.
# -------------------------------------------------------
set -euo pipefail

PORT="${1:-8000}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "==========================================="
echo "  Azure AI Search MCP - DEV MODE"
echo "  Transport : streamable-http (port $PORT)"
echo "  Inspector : http://localhost:6274"
echo "==========================================="
echo ""

uv run mcp dev main.py --port "$PORT"
