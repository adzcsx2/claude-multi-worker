@echo off
cls
echo ========================================
echo   WezTerm 多窗口启动器
echo ========================================
echo.
echo 说明: 此脚本启动多个独立的 WezTerm 窗口
echo        每个窗口运行一个 Claude 实例
echo.
echo ========================================
echo.
echo 📊 效果预览:
echo.
echo   ┌─────────────┐  ┌─────────────┐
echo   │ 窗口 1      │  │ 窗口 2      │
echo   │ 标题: ui    │  │ 标题: coder │
echo   │             │  │             │
echo   │ claude>     │  │ claude>     │
echo   └─────────────┘  └─────────────┘
echo.
echo ========================================
echo.
echo 🚀 使用步骤:
echo.
echo   1. 确保已安装 WezTerm
echo      wezterm --version
echo.
echo   2. 进入项目目录 (如果尚未进入):
echo      cd E:\ai_project\claude-multi-starter
echo.
echo   3. 运行启动器:
echo      python START_MULTI_WINDOW.py ui,coder
echo.
echo   4. 输入 y 确认
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
echo   启动 2 个窗口:
echo      python START_MULTI_WINDOW.py ui,coder
echo.
echo   启动 3 个窗口:
echo      python START_MULTI_WINDOW.py ui,coder,test
echo.
echo   启动 4 个窗口:
echo      python START_MULTI_WINDOW.py default,ui,coder,test
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
echo ========================================
echo.
echo 🎯 窗口操作:
echo   - 使用 Alt+Tab 切换窗口
echo   - 可以自由移动和调整窗口大小
echo   - 适合多显示器环境
echo.
echo ========================================
echo.
echo 📚 更多文档:
echo   - MULTI_WINDOW_GUIDE.md (完整指南)
echo   - APPROACH_COMPARISON.md (方式对比)
echo.
echo ========================================
echo.

set /p CONTINUE="是否立即启动? (y/n): "

if /i "%CONTINUE%"=="y" (
    echo.
    echo [*] 启动多窗口...
    echo.
    echo     python START_MULTI_WINDOW.py ui,coder
    echo.
    python START_MULTI_WINDOW.py ui,coder
) else (
    echo.
    echo [*] 已取消
    echo [*] 当你准备好时，运行:
    echo.
    echo     python START_MULTI_WINDOW.py ui,coder
    echo.
)

echo.
pause
