@echo off
REM Vibe Coding Automation Mode Startup Script
REM Automatically launches PowerShell version to avoid encoding issues

chcp 65001 >nul 2>&1

echo Starting Vibe Coding Automation...
echo.

REM Check if PowerShell is available
where powershell >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PowerShell not found
    echo Please install PowerShell to use automation mode
    pause
    exit /b 1
)

REM Check if scripts directory exists
if not exist "%~dp0scripts\" (
    echo [ERROR] scripts directory not found
    echo Expected path: %~dp0scripts\
    pause
    exit /b 1
)

REM Check if start-automation.ps1 exists
if not exist "%~dp0scripts\start-automation.ps1" (
    echo [ERROR] start-automation.ps1 not found
    pause
    exit /b 1
)

echo [OK] Found PowerShell script
echo.

REM Run PowerShell script from scripts directory
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-automation.ps1"

if errorlevel 1 pause
