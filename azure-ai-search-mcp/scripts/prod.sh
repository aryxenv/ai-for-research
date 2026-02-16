#!/usr/bin/env bash
# -------------------------------------------------------
# Start Azure AI Search MCP server in PRODUCTION mode
# Uses streamable-http transport (HTTP endpoint).
# -------------------------------------------------------
set -euo pipefail

HOST="${1:-0.0.0.0}"
PORT="${2:-8000}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "==========================================="
echo "  Azure AI Search MCP - PROD MODE"
echo "  Transport : streamable-http"
echo "  Endpoint  : http://$HOST:$PORT/mcp"
echo "==========================================="
echo ""

uv run python main.py --transport streamable-http --host "$HOST" --port "$PORT"
