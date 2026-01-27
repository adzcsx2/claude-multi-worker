# Launch Development Environment
# Usage: .\scripts\start-automation.ps1

[CmdletBinding()]
param()

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         Launch Development Environment" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_DIR = (Get-Location).Path
$wtPath = Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps\wt.exe"

if (-not (Test-Path $wtPath)) {
    Write-Host "[ERROR] Windows Terminal not found" -ForegroundColor Red
    Write-Host "Please install Windows Terminal from Microsoft Store" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Windows Terminal found" -ForegroundColor Green
Write-Host ""

# Check and initialize automation state
Write-Host "Checking automation environment..." -ForegroundColor Cyan

$taskCommsDir = Join-Path $PROJECT_DIR "task-comms"
$automationStateFile = Join-Path $taskCommsDir "automation-state.md"
$fromC1File = Join-Path $taskCommsDir "from-c1-design.md"
$fromC2File = Join-Path $taskCommsDir "from-c2-main.md"
$fromC3File = Join-Path $taskCommsDir "from-c3-test.md"

# Create task-comms directory if not exists
if (-not (Test-Path $taskCommsDir)) {
    Write-Host "[INIT] Creating task-comms directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $taskCommsDir -Force | Out-Null
    Write-Host "[OK] task-comms directory created" -ForegroundColor Green
} else {
    Write-Host "[OK] task-comms directory exists" -ForegroundColor Green
}

# Create automation-state.md if not exists
if (-not (Test-Path $automationStateFile)) {
    Write-Host "[INIT] Creating automation-state.md..." -ForegroundColor Yellow
    
    $stateContent = @"
# Automation State

## Current State
- **Current Step**: STEP_INIT
- **Current Window**: C1
- **Current Index**: 0
- **Automation Mode**: ENABLED

## Interface List
- [0] Login Page
- [1] Home Page
- [2] Profile Page
- [3] Settings Page

## Step Definitions
| Step | Window | Action | Next |
|------|--------|-------|------|
| STEP_INIT | C1 | Create Design System | STEP_DESIGN |
| STEP_DESIGN | C1 | Design Current Interface | STEP_DEVELOP |
| STEP_DEVELOP | C2 | Develop Current Interface | STEP_TEST |
| STEP_TEST | C3 | Test Current Interface | Pass->STEP_NEXT, Fail->STEP_DEVELOP |
| STEP_NEXT | - | Index+1, Move to Next | STEP_DESIGN |
| STEP_COMPLETE | ALL | All Interfaces Complete | END |

## State History
| Time | Window | Step | Index | Action |
|------|--------|------|-------|--------|
| $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | LAUNCHER | STEP_INIT | - | Automation state initialized |
"@

    Set-Content -Path $automationStateFile -Value $stateContent -Encoding UTF8
    Write-Host "[OK] automation-state.md created" -ForegroundColor Green
} else {
    Write-Host "[OK] automation-state.md exists" -ForegroundColor Green
}

# Create communication files if not exists
$commFiles = @(
    @{Path = $fromC1File; Title = "from-c1-design.md"; Window = "C1"}
    @{Path = $fromC2File; Title = "from-c2-main.md"; Window = "C2"}
    @{Path = $fromC3File; Title = "from-c3-test.md"; Window = "C3"}
)

foreach ($file in $commFiles) {
    if (-not (Test-Path $file.Path)) {
        Write-Host "[INIT] Creating $($file.Title)..." -ForegroundColor Yellow
        $commContent = @"
# Communication from $($file.Window)

## Latest Message
*No messages yet*

## Message History
| Time | From | To | Message |
|------|------|----|---------|
"@
        Set-Content -Path $file.Path -Value $commContent -Encoding UTF8
        Write-Host "[OK] $($file.Title) created" -ForegroundColor Green
    } else {
        Write-Host "[OK] $($file.Title) exists" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "[SUCCESS] Automation environment ready" -ForegroundColor Green
Write-Host ""

# Detect system language - check multiple sources
$sysLocale = (Get-WinSystemLocale).Name
$uiLang = $Host.CurrentUICulture.TwoLetterISOLanguageName
$isChinese = $sysLocale -like "zh*" -or $uiLang -eq "zh"

Write-Host "System Locale: $sysLocale" -ForegroundColor Cyan
Write-Host "UI Language: $uiLang" -ForegroundColor Cyan
Write-Host "Using Chinese: $isChinese" -ForegroundColor Cyan
Write-Host ""

# Set commands based on language (embedded in script)
if ($isChinese) {
    # Simple trigger mode - user inputs "继续" to check and execute
    $c1Cmd = @"
我是 C1 窗口，负责设计任务。启动自动化模式。

【自动化规则】
1. 读取 task-comms/automation-state.md 检查当前状态
2. 如果 Current Window 是 C1，立即执行任务
3. 执行任务后必须更新状态文件：
   - 更新 Current Step 到下一步骤
   - 更新 Current Window 到下一窗口
   - 在 State History 中添加记录
4. 如果不是 C1 的回合，显示简短等待信息并停止

【重要】完成后显示："✅ 任务完成！请在 C2 窗口输入：继续"
"@

    $c2Cmd = @"
我是 C2 窗口，负责开发任务。启动自动化模式。

【自动化规则】
1. 读取 task-comms/automation-state.md 检查当前状态
2. 如果 Current Window 是 C2，立即执行任务
3. 执行任务后必须更新状态文件：
   - 更新 Current Step 到下一步骤
   - 更新 Current Window 到下一窗口
   - 在 State History 中添加记录
4. 如果不是 C2 的回合，显示简短等待信息并停止

【重要】完成后显示："✅ 任务完成！请在 C3 窗口输入：继续"
"@

    $c3Cmd = @"
我是 C3 窗口，负责测试任务。启动自动化模式。

【自动化规则】
1. 读取 task-comms/automation-state.md 检查当前状态
2. 如果 Current Window 是 C3，立即执行任务
3. 执行任务后必须更新状态文件：
   - 更新 Current Step 到下一步骤
   - 更新 Current Window 到下一窗口
   - 在 State History 中添加记录
4. 如果不是 C3 的回合，显示简短等待信息并停止

【重要】完成后显示："✅ 任务完成！请在 C1 窗口输入：继续"
"@

    $cmdPrompt = "请在 Claude 启动后输入以下命令："
} else {
    # English template - simple trigger mode
    $c1Cmd = @"
I am C1 window, design task. Start automation mode.

[Automation Rules]
1. Read task-comms/automation-state.md to check current state
2. If Current Window is C1, execute task immediately
3. After completing task, MUST update state file:
   - Update Current Step to next step
   - Update Current Window to next window
   - Add record to State History
4. If not C1's turn, display brief waiting message and stop

[IMPORTANT] After completion, display: "Task done! In C2 window, type: continue"
"@

    $c2Cmd = @"
I am C2 window, development task. Start automation mode.

[Automation Rules]
1. Read task-comms/automation-state.md to check current state
2. If Current Window is C2, execute task immediately
3. After completing task, MUST update state file:
   - Update Current Step to next step
   - Update Current Window to next window
   - Add record to State History
4. If not C2's turn, display brief waiting message and stop

[IMPORTANT] After completion, display: "Task done! In C3 window, type: continue"
"@

    $c3Cmd = @"
I am C3 window, testing task. Start automation mode.

[Automation Rules]
1. Read task-comms/automation-state.md to check current state
2. If Current Window is C3, execute task immediately
3. After completing task, MUST update state file:
   - Update Current Step to next step
   - Update Current Window to next window
   - Add record to State History
4. If not C3's turn, display brief waiting message and stop

[IMPORTANT] After completion, display: "Task done! In C1 window, type: continue"
"@

    $cmdPrompt = "Enter this command after Claude launches:"
}

Write-Host ""

# Build command blocks for each Claude window
$c1Block = @"
Set-Location '$PROJECT_DIR'
`$Host.UI.RawUI.WindowTitle = 'C1-Design'
Write-Host ''
Write-Host '====================================' -ForegroundColor Cyan
Write-Host '    Claude Window: C1-Design' -ForegroundColor Yellow
Write-Host '====================================' -ForegroundColor Cyan
Write-Host ''
Write-Host '$cmdPrompt' -ForegroundColor Green
Write-Host ''
Write-Host '$c1Cmd' -ForegroundColor White
Write-Host ''
Write-Host 'Launching Claude...' -ForegroundColor Cyan
Write-Host ''
claude
"@

$c2Block = @"
Set-Location '$PROJECT_DIR'
`$Host.UI.RawUI.WindowTitle = 'C2-Main'
Write-Host ''
Write-Host '====================================' -ForegroundColor Cyan
Write-Host '    Claude Window: C2-Main' -ForegroundColor Yellow
Write-Host '====================================' -ForegroundColor Cyan
Write-Host ''
Write-Host '$cmdPrompt' -ForegroundColor Green
Write-Host ''
Write-Host '$c2Cmd' -ForegroundColor White
Write-Host ''
Write-Host 'Launching Claude...' -ForegroundColor Cyan
Write-Host ''
claude
"@

$c3Block = @"
Set-Location '$PROJECT_DIR'
`$Host.UI.RawUI.WindowTitle = 'C3-Test'
Write-Host ''
Write-Host '====================================' -ForegroundColor Cyan
Write-Host '    Claude Window: C3-Test' -ForegroundColor Yellow
Write-Host '====================================' -ForegroundColor Cyan
Write-Host ''
Write-Host '$cmdPrompt' -ForegroundColor Green
Write-Host ''
Write-Host '$c3Cmd' -ForegroundColor White
Write-Host ''
Write-Host 'Launching Claude...' -ForegroundColor Cyan
Write-Host ''
claude
"@

# Encode commands in Base64
$c1Bytes = [System.Text.Encoding]::Unicode.GetBytes($c1Block)
$c1Encoded = [Convert]::ToBase64String($c1Bytes)

$c2Bytes = [System.Text.Encoding]::Unicode.GetBytes($c2Block)
$c2Encoded = [Convert]::ToBase64String($c2Bytes)

$c3Bytes = [System.Text.Encoding]::Unicode.GetBytes($c3Block)
$c3Encoded = [Convert]::ToBase64String($c3Bytes)

Write-Host "Launching Windows Terminal with 3 tabs..." -ForegroundColor Cyan
Write-Host ""

try {
    $wtArgs = @(
        "new-tab", "--title", "C1-Design", "pwsh", "-NoExit", "-NoLogo", "-EncodedCommand", $c1Encoded, ";",
        "new-tab", "--title", "C2-Main", "pwsh", "-NoExit", "-NoLogo", "-EncodedCommand", $c2Encoded, ";",
        "new-tab", "--title", "C3-Test", "pwsh", "-NoExit", "-NoLogo", "-EncodedCommand", $c3Encoded
    )
    
    Start-Process -FilePath $wtPath -ArgumentList $wtArgs -ErrorAction Stop
    
    Write-Host "[SUCCESS] Windows Terminal launched with 3 tabs" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Failed to launch Windows Terminal" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Launcher will close in 3 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# Ask user if they want to start auto-continue
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         Start Auto-Continue?" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Auto-Continue will automatically send '继续' to the active window." -ForegroundColor Yellow
Write-Host ""
$autoContinue = Read-Host "Start auto-continue now? (Y/n)"

if ($autoContinue -ne "n" -and $autoContinue -ne "N") {
    Write-Host ""
    Write-Host "[STARTING] Auto-continue script..." -ForegroundColor Green

    $autoContinueScript = Join-Path $PROJECT_DIR "scripts\auto-continue.ps1"

    if (Test-Path $autoContinueScript) {
        Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$autoContinueScript`""
        Write-Host "[OK] Auto-continue started in new window" -ForegroundColor Green
    } else {
        Write-Host "[WARN] auto-continue.ps1 not found" -ForegroundColor Yellow
    }
}
