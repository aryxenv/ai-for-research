<#
.SYNOPSIS
    Start the Azure AI Search MCP server in PRODUCTION mode.

.DESCRIPTION
    Runs the server with streamable-http transport, exposing an HTTP endpoint
    that GitHub Copilot, Claude Desktop, mcpo, and other MCP clients can connect to.

    Prerequisites: uv must be installed and 'uv sync' must have been run.

.PARAMETER BindAddress
    Host address to bind to (default: 0.0.0.0).

.PARAMETER Port
    The port for the HTTP server (default: 8000).
#>
param(
    [string]$BindAddress = "0.0.0.0",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir

Push-Location $ProjectRoot
try {
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host "  Azure AI Search MCP - PROD MODE"          -ForegroundColor Green
    Write-Host "  Transport : streamable-http"              -ForegroundColor Green
    Write-Host "  Endpoint  : http://${BindAddress}:$Port/mcp"     -ForegroundColor Green
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host ""

    uv run python main.py --transport streamable-http --host $BindAddress --port $Port
}
finally {
    Pop-Location
}
