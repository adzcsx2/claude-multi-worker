@echo off
cls
echo ========================================
echo   WezTerm 多标签页启动器
echo ========================================
echo.
echo 说明: 此脚本在一个 WezTerm 窗口中创建多个标签页
echo        每个标签页运行一个 Claude 实例
echo.
echo ========================================
echo.
echo 📊 效果预览:
echo.
echo   ┌─────────────────────────────────────┐
echo   │ WezTerm 窗口                        │
echo   ├─────┬─────┬─────┬─────┐            │
echo   │ ui  │coder│test │...  │ (标签页)    │
echo   ├─────┴─────┴─────┴─────┴────────────┤
echo   │                                     │
echo   │ claude>                             │
echo   │                                     │
echo   └─────────────────────────────────────┘
echo.
echo ========================================
echo.
echo 🚀 使用步骤:
echo.
echo   选项 1: 在 WezTerm 中运行 (推荐)
echo     1. 打开 WezTerm
echo     2. cd %CD%
echo     3. python START_MULTI_TAB.py ui,coder,test
echo.
echo   选项 2: 直接运行 (自动启动 WezTerm)
echo     python START_MULTI_TAB.py ui,coder,test
echo.
echo ========================================
echo.
echo 📋 可用实例:
echo   - ui       (UI/UX 设计师)
echo   - coder    (开发者)
echo   - test     (QA 工程师)
echo   - default  (协调者)
echo.
echo ========================================
echo.
echo 💡 使用示例:
echo.
echo   启动 2 个标签页:
echo      python START_MULTI_TAB.py ui,coder
echo.
echo   启动 3 个标签页:
echo      python START_MULTI_TAB.py ui,coder,test
echo.
echo   启动 4 个标签页:
echo      python START_MULTI_TAB.py default,ui,coder,test
echo.
echo ========================================
echo.
echo 📡 通信命令:
echo   启动后，在任意终端中:
echo.
echo     bin\send ui "设计任务"
echo     bin\send coder "开发任务"
echo     bin\send test "测试任务"
echo.
echo   消息会自动发送并提交(就像按回车)
echo.
echo ========================================
echo.
echo 🎯 标签页操作:
echo   - 使用 Ctrl+Tab 切换标签页
echo   - 使用 Ctrl+Shift+Tab 反向切换
echo   - 所有标签页在同一个窗口中
echo   - 更加紧凑和高效
echo.
echo ========================================
echo.

set /p CONTINUE="是否立即启动? (y/n): "

if /i "%CONTINUE%"=="y" (
    echo.
    echo [*] 启动多标签页...
    echo.
    echo     python START_MULTI_TAB.py ui,coder,test
    echo.
    python START_MULTI_TAB.py ui,coder,test
) else (
    echo.
    echo [*] 已取消
    echo [*] 当你准备好时，运行:
    echo.
    echo     python START_MULTI_TAB.py ui,coder,test
    echo.
)

echo.
pause
