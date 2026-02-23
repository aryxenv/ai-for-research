<#
.SYNOPSIS
    Start the mcpo proxy for OpenWebUI, connecting to the cloud MCP server.

.DESCRIPTION
    Starts mcpo (MCP-to-OpenAPI proxy) that connects to the cloud-hosted MCP
    server (configured in mcpo-config.json) and exposes an OpenAPI endpoint
    for OpenWebUI.

    After starting, add the server in OpenWebUI:
      Admin Panel > Settings > Tools > OpenAPI Servers > Add Connection
      URL  : http://localhost:<McpoPort>/azure-ai-search
      Key  : <ApiKey>

    Prerequisites: mcpo (pip install mcpo).

.PARAMETER McpoPort
    The port for the mcpo OpenAPI proxy (default: 8001).

.PARAMETER ApiKey
    API key for mcpo authentication (default: "top-secret"). Set to "" to disable.
#>
param(
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
    Write-Host "  mcpo endpoint : http://localhost:$McpoPort"    -ForegroundColor Magenta
    Write-Host "  Tools docs    : http://localhost:$McpoPort/azure-ai-search/docs" -ForegroundColor Magenta
    Write-Host "================================================" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Add to OpenWebUI -> Admin -> Settings -> Tools -> OpenAPI Servers:" -ForegroundColor Yellow
    Write-Host "  URL : http://localhost:$McpoPort/azure-ai-search"  -ForegroundColor Yellow
    Write-Host "  Key : $ApiKey"                                      -ForegroundColor Yellow
    Write-Host ""

    Write-Host "Starting mcpo proxy (port $McpoPort)..." -ForegroundColor Cyan
    $mcpoArgs = @("--port", $McpoPort, "--config", "mcpo-config.json")
    if ($ApiKey -ne "") {
        $mcpoArgs += @("--api-key", $ApiKey)
    }

    mcpo @mcpoArgs
}
finally {
    Pop-Location
}
