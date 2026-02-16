<#
.SYNOPSIS
    Start the Azure AI Search MCP server + mcpo proxy for OpenWebUI.

.DESCRIPTION
    1. Launches the MCP server with streamable-http transport (background).
    2. Starts mcpo (MCP-to-OpenAPI proxy) that connects to the MCP server
       over streamable-http and exposes an OpenAPI endpoint for OpenWebUI.

    After starting, add the server in OpenWebUI:
      Admin Panel > Settings > Tools > OpenAPI Servers > Add Connection
      URL  : http://localhost:<McpoPort>/azure-ai-search
      Key  : <ApiKey>

    Prerequisites: uv, mcpo (pip install mcpo), and 'uv sync' must have been run.

.PARAMETER McpPort
    The port for the MCP streamable-http server (default: 8000).

.PARAMETER McpoPort
    The port for the mcpo OpenAPI proxy (default: 8001).

.PARAMETER ApiKey
    API key for mcpo authentication (default: "top-secret"). Set to "" to disable.
#>
param(
    [int]$McpPort = 8000,
    [int]$McpoPort = 8001,
    [string]$ApiKey = "top-secret"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir

Push-Location $ProjectRoot
try {
    Write-Host "================================================" -ForegroundColor Magenta
    Write-Host "  Azure AI Search MCP - OpenWebUI (via mcpo)"    -ForegroundColor Magenta
    Write-Host "  MCP server    : http://localhost:$McpPort/mcp" -ForegroundColor Magenta
    Write-Host "  mcpo endpoint : http://localhost:$McpoPort"    -ForegroundColor Magenta
    Write-Host "  Tools docs    : http://localhost:$McpoPort/azure-ai-search/docs" -ForegroundColor Magenta
    Write-Host "================================================" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Add to OpenWebUI -> Admin -> Settings -> Tools -> OpenAPI Servers:" -ForegroundColor Yellow
    Write-Host "  URL : http://localhost:$McpoPort/azure-ai-search"  -ForegroundColor Yellow
    Write-Host "  Key : $ApiKey"                                      -ForegroundColor Yellow
    Write-Host ""

    # 1. Start the MCP server in the background
    Write-Host "Starting MCP server (streamable-http on port $McpPort)..." -ForegroundColor Cyan
    $mcpJob = Start-Job -ScriptBlock {
        param($Root, $Port)
        Set-Location $Root
        uv run python main.py --transport streamable-http --host 127.0.0.1 --port $Port
    } -ArgumentList $ProjectRoot, $McpPort

    # Give it a moment to start
    Start-Sleep -Seconds 3

    # 2. Start mcpo pointing at the running MCP server
    Write-Host "Starting mcpo proxy (port $McpoPort)..." -ForegroundColor Cyan
    $mcpoArgs = @("--port", $McpoPort, "--config", "mcpo-config.json")
    if ($ApiKey -ne "") {
        $mcpoArgs += @("--api-key", $ApiKey)
    }

    try {
        mcpo @mcpoArgs
    }
    finally {
        # Clean up MCP server when mcpo exits
        Write-Host "Stopping MCP server..." -ForegroundColor Yellow
        Stop-Job $mcpJob -ErrorAction SilentlyContinue
        Remove-Job $mcpJob -ErrorAction SilentlyContinue
    }
}
finally {
    Pop-Location
}
