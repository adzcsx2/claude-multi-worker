@echo off
cls
echo ========================================
echo   🎯 WezTerm 多窗格启动说明
echo ========================================
echo.
echo ✅ 检测到你在 WezTerm 环境中！
echo.
echo ========================================
echo.
echo 📋 接下来的步骤:
echo.
echo  1. 确保你在正确的目录:
echo.
echo     cd E:\ai_project\claude-multi-starter
     echo.
echo 2. 运行启动器:
echo.
echo     python START_MULTI_PANE.py ui,coder
echo.
echo 3. 看到提示时输入: y
echo.
echo 4. 等待窗格创建完成
echo.
echo ========================================
echo.
echo 🎯 预期效果:
echo.
echo   ┌──────────────────────────────┐
echo   │  WezTerm 窗口            │
echo   ├──────────┬─────────────────┤
echo   │ ui       │ coder          │
echo   │          │                │
echo   │ claude>  │ claude>         │
echo   └──────────┴─────────────────┘
echo.
echo   - 一个 WezTerm 窗口
echo   - 两个子窗格
echo   - 可以使用 send 命令通信
echo.
echo ========================================
echo.
echo 📝 可用实例:
echo   - ui       (UI/UX 设计)
echo   - coder   (开发)
echo   - test    (测试)
echo   - default (协调者)
echo.
echo ========================================
echo.
echo 💡 窗格切换:
echo   Ctrl+Shift+方向键
echo.
echo ========================================
echo.
echo 🚀 立即开始:
echo.
echo   1. 检查当前目录:
echo      cd
echo.
echo   2. 如果不在项目目录:
echo      cd E:\ai_project\claude-multi-starter
echo.
echo   3. 运行启动器:
echo      python START_MULTI_PANE.py ui,coder
echo.
echo   4. 输入 y 并回车
echo.
echo ========================================
echo.

REM 询问用户是否要继续
set /p CONTINUE="是否现在运行? (y/n): "

if /i "%CONTINUE%"=="y" (
    echo.
    echo [*] 启动多窗格...
    echo.
    python START_MULTI_PANE.py ui,coder
) else (
    echo.
    echo [*] 已取消
    echo [*] 当你准备好时，再次运行此脚本
    echo.
    echo     cd E:\ai_project\claude-multi-starter
    echo     python START_MULTI_PANE.py ui,coder
    echo.
)

echo.
pause
