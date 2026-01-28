# Auto-Continue Script for Automation
# Monitor state changes and auto-trigger next window

param(
    [string]$ProjectDir = (Get-Location).Path
)

# Fix encoding issues
chcp 65001 > $null
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# Clear console
Clear-Host

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         Auto-Continue Monitor" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$stateFile = Join-Path $ProjectDir "task-comms\automation-state.md"

if (-not (Test-Path $stateFile)) {
    Write-Host "[ERROR] automation-state.md not found" -ForegroundColor Red
    Write-Host "Please run start-automation.ps1 first" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Found automation-state.md" -ForegroundColor Green
Write-Host "Watching for state changes..." -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "  When window completes task:" -ForegroundColor Yellow
Write-Host "  Auto-continue will notify you" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
Write-Host ""

# Track last known window
$lastWindow = ""
$lastStep = ""
$triggerCount = 0

# Function to copy "继续" to clipboard and show notification
function Trigger-Continue {
    param([string]$WindowName, [string]$Step)

    # Copy to clipboard
    "continue" | Set-Clipboard

    $global:triggerCount++

    # Show notification (English only to avoid encoding issues)
    Write-Host ""
    Write-Host "========================================================" -BackgroundColor DarkGreen
    Write-Host "  [$($global:triggerCount)] SWITCH TO: $WindowName" -ForegroundColor Black -BackgroundColor Green
    Write-Host "  Step: $Step" -ForegroundColor Black -BackgroundColor Green
    Write-Host "  Clipboard ready - Press Ctrl+V" -ForegroundColor Black -BackgroundColor Green
    Write-Host "========================================================" -BackgroundColor DarkGreen
    Write-Host ""

    # Play sound
    [console]::beep(800, 200)
}

# Watch for file changes
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = Split-Path $stateFile
$watcher.Filter = Split-Path $stateFile -Leaf
$watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite
$watcher.EnableRaisingEvents = $true

$action = {
    Start-Sleep -Milliseconds 300  # Wait for file write to complete

    try {
        $content = Get-Content $stateFile -Raw -Encoding UTF8

        if ($content -match '- \*\*Current Step\*\*: (\S+)') {
            $currentStep = $matches[1].Trim()
        }

        if ($content -match '- \*\*Current Window\*\*: (C[123])') {
            $currentWindow = $matches[1].Trim()

            # Only trigger if window changed
            if ($currentWindow -ne $global:lastWindow -and $currentWindow -ne "") {
                $global:lastWindow = $currentWindow
                $global:lastStep = $currentStep

                $windowName = switch ($currentWindow) {
                    "C1" { "C1-Design" }
                    "C2" { "C2-Main" }
                    "C3" { "C3-Test" }
                }

                # Wait a bit for the previous window to finish
                Start-Sleep -Seconds 2

                Trigger-Continue -WindowName $windowName -Step $currentStep
            }
        }
    }
    catch {
        Write-Host "Error reading state file: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Register the event
Register-ObjectEvent -InputObject $watcher -EventName Changed -Action $action | Out-Null

# Initial state check
Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Checking initial state..." -ForegroundColor Cyan
& $action

Write-Host ""
Write-Host "[RUNNING] Auto-continue is active. Waiting for state changes..." -ForegroundColor Magenta
Write-Host ""

try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    $watcher.Dispose()
    Write-Host ""
    Write-Host "[STOPPED] Auto-continue disabled" -ForegroundColor Gray
    Write-Host "Total triggers: $triggerCount" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to close"
}
