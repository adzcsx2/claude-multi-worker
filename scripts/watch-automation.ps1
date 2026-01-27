# File Watcher for Automation State
# Usage: .\scripts\watch-automation.ps1

[CmdletBinding()]
param()

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         Automation State File Watcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_DIR = (Get-Location).Path
$stateFile = Join-Path $PROJECT_DIR "task-comms\automation-state.md"

if (-not (Test-Path $stateFile)) {
    Write-Host "[ERROR] automation-state.md not found" -ForegroundColor Red
    Write-Host "Path: $stateFile" -ForegroundColor Yellow
    Write-Host "Please run start-automation.ps1 first to initialize" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Found automation-state.md" -ForegroundColor Green
Write-Host "Watching: $stateFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop watching..." -ForegroundColor Yellow
Write-Host ""

# Create FileSystemWatcher
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = Split-Path $stateFile
$watcher.Filter = Split-Path $stateFile -Leaf
$watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite
$watcher.EnableRaisingEvents = $true

# Define the action on file change
$action = {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] State file changed!" -ForegroundColor Green
    
    # Read and parse the state
    try {
        $content = Get-Content $stateFile -Raw
        
        if ($content -match '- \*\*Current Step\*\*: (.+)') {
            $step = $matches[1].Trim()
        }
        if ($content -match '- \*\*Current Window\*\*: (.+)') {
            $window = $matches[1].Trim()
        }
        if ($content -match '- \*\*Current Index\*\*: (.+)') {
            $index = $matches[1].Trim()
        }
        
        Write-Host "  Step: $step | Window: $window | Index: $index" -ForegroundColor Cyan
        Write-Host ""
    }
    catch {
        Write-Host "  Error reading state file: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Register event
Register-ObjectEvent -InputObject $watcher -EventName Changed -Action $action | Out-Null

Write-Host "[WATCHING] Waiting for state changes..." -ForegroundColor Magenta
Write-Host ""

# Display initial state
$content = Get-Content $stateFile -Raw
if ($content -match '- \*\*Current Step\*\*: (.+)') {
    $step = $matches[1].Trim()
}
if ($content -match '- \*\*Current Window\*\*: (.+)') {
    $window = $matches[1].Trim()
}
if ($content -match '- \*\*Current Index\*\*: (.+)') {
    $index = $matches[1].Trim()
}

Write-Host "Initial State:" -ForegroundColor Yellow
Write-Host "  Step: $step | Window: $window | Index: $index" -ForegroundColor Cyan
Write-Host ""

# Keep script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    $watcher.Dispose()
    Write-Host ""
    Write-Host "[STOPPED] File watcher stopped" -ForegroundColor Gray
}
