@echo off
cls
echo ========================================
echo   CMS 多实例启动 - 快速开始
echo ========================================
echo.
echo CMS (Claude Multi Starter) 可以在
echo 一个 WezTerm 窗口中创建多个
echo 子窗格，每个运行独立的 Claude 实例
echo.
echo ========================================
echo.
echo 📋 什么是子窗格?
echo.
echo   ┌──────────────────────────────┐
echo   │  WezTerm 窗口            │
echo   ├──────────┬─────────────────┤
echo   │ 子窗格 1  │ 子窗格 2         │
echo   │ (ui)     │ (coder)         │
echo   │          │                 │
echo   │ claude>  │ claude>         │
echo   └──────────┴─────────────────┘
echo.
echo   ✓ 一个窗口
echo   ✓ 多个子窗格 (pane)
echo   ✓ 可以互相通信
echo   ✓ 每个窗格运行 Claude
echo.
echo ========================================
echo.
echo 🚀 使用步骤:
echo.
echo   1. 打开 WezTerm
echo      从开始菜单启动 WezTerm
echo.
echo   2. 进入项目目录
echo      cd E:\ai_project\claude-multi-starter
echo.
echo   3. 启动多实例
echo      python START_MULTI_PANE.py ui,coder
echo.
echo   4. 确认继续
echo      输入 y 并回车
echo.
echo ========================================
echo.
echo 📋 可用实例:
echo   - ui       (UI/UX 设计)
echo   - coder    (开发)
echo   - test     (测试)
echo   - default  (协调者)
echo.
echo ========================================
echo.
echo 💡 窗格切换快捷键:
echo   Ctrl+Shift+方向键
echo.
echo ========================================
echo.
echo 📡 测试通信:
echo   在新命令行窗口中运行:
echo      test_communication.bat
echo.
echo ========================================
echo.
echo 📚 更多文档:
echo   - APPROACH_COMPARISON.md  (方式对比)
echo   - MULTI_PANE_CORRECT.md   (使用指南)
echo   - FINAL_GUIDE.txt         (快速指南)
echo.
echo ========================================
echo.

set /p START="是否立即启动? (y/n): "

if /i "%START%"=="y" (
    echo.
    echo [*] 请在 WezTerm 中运行以下命令:
    echo.
    echo     cd E:\ai_project\claude-multi-starter
    echo     python START_MULTI_PANE.py ui,coder
    echo.
)

echo.
pause
