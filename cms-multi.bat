@echo off
REM CMS 多实例启动器

setlocal EnableDelayedExpansion

REM 解析参数
set INSTANCES=%~1
set "INSTANCES=%INSTANCES: =%"

REM 移除 claude: 前缀
set "INSTANCES=%INSTANCES:claude:=%"

echo ========================================
echo   CMS 多实例启动器
echo ========================================
echo.
echo 🚀 启动实例: %INSTANCES%
echo.

REM 使用 Python 补丁启动
python MULTI_INSTANCE_FIX.py %INSTANCES%

echo.
echo ========================================
echo.
pause
