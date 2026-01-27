@echo off
echo ========================================
echo   测试实例间通信
echo ========================================
echo.
echo 此脚本测试多实例启动后的通信功能
echo.
echo ========================================
echo.
echo 测试步骤:
echo.
echo 1. 首先启动多实例 (在 WezTerm 中):
echo    python START_MULTI_PANE.py ui,coder
echo.
echo 2. 然后运行此测试脚本发送消息:
echo.
echo ========================================
echo.

REM 检查是否在正确的目录
if not exist ".cms_config\pane_mapping.json" (
    echo [!] 未找到 pane_mapping.json
    echo [!] 请先运行: python START_MULTI_PANE.py ui,coder
    echo.
    pause
    exit /b 1
)

echo [+] 找到 pane_mapping.json
echo.

REM 发送测试消息到 ui 实例
echo [*] 发送测试消息到 ui 实例...
bin\send ui "这是发送到 ui 实例的测试消息"
echo.

REM 等待用户确认
pause

REM 发送测试消息到 coder 实例
echo [*] 发送测试消息到 coder 实例...
bin\send coder "这是发送到 coder 实例的测试消息"
echo.

echo ========================================
echo.
echo ✓ 测试完成
echo.
echo 请在 WezTerm 的各个窗格中查看收到的消息
echo.
echo ========================================
echo.
pause
