@echo off
cls
echo ========================================
echo   测试多窗口模式
echo ========================================
echo.
echo 此脚本测试 START_MULTI_WINDOW.py 的功能
echo.
echo ========================================
echo.

REM 检查 WezTerm
echo [1/4] 检查 WezTerm...
wezterm --version >nul 2>&1
if errorlevel 1 (
    echo [!] WezTerm 未安装
    echo     请安装: https://wezfurlong.org/wezterm/
    pause
    exit /b 1
)
echo [+] WezTerm 已安装
wezterm --version
echo.

REM 检查 Python
echo [2/4] 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python 未安装
    pause
    exit /b 1
)
echo [+] Python 已安装
python --version
echo.

REM 检查启动脚本
echo [3/4] 检查启动脚本...
if not exist "START_MULTI_WINDOW.py" (
    echo [!] START_MULTI_WINDOW.py 不存在
    pause
    exit /b 1
)
echo [+] START_MULTI_WINDOW.py 存在
echo.

REM 测试启动
echo [4/4] 测试启动 2 个窗口...
echo.
echo 这将:
echo   1. 启动 2 个独立的 WezTerm 窗口
echo   2. 每个窗口运行 Claude 实例
echo   3. 创建窗口映射文件
echo.
echo ========================================
echo.

set /p CONTINUE="是否继续测试? (y/n): "

if /i "%CONTINUE%"=="y" (
    echo.
    echo [*] 启动多窗口...
    echo.

    REM 自动输入 y
    echo y | python START_MULTI_WINDOW.py ui,coder

    echo.
    echo ========================================
    echo.
    echo [*] 测试完成
    echo.
    echo 请检查:
    echo   [ ] 是否打开了 2 个 WezTerm 窗口
    echo   [ ] 窗口标题是否显示 "ui" 和 "coder"
    echo   [ ] 每个窗口是否显示 claude>
    echo   [ ] 是否创建了 window_mapping.json
    echo.
    echo ========================================
    echo.

    REM 显示映射文件
    if exist ".cms_config\window_mapping.json" (
        echo [*] 窗口映射文件:
        type .cms_config\window_mapping.json
        echo.
        echo ========================================
        echo.
    )

    echo [*] 测试通信:
    echo.
    echo     bin\send ui "测试消息到 ui"
    echo     bin\send coder "测试消息到 coder"
    echo.

) else (
    echo.
    echo [*] 已取消测试
    echo.
)

pause
