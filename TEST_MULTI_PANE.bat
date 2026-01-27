@echo off
cls
echo ========================================
echo   WezTerm 多窗格启动指南
echo ========================================
echo.
echo 说明: 此脚本用于在 WezTerm 中创建
echo        多个子窗格，每个运行 Claude
echo.
echo ========================================
echo.
echo 步骤 1: 打开 WezTerm
echo   - 从开始菜单启动 WezTerm
echo   - 或运行: wezterm
echo.
echo 步骤 2: 进入项目目录
echo   cd E:\ai_project\claude-multi-starter
echo.
echo 步骤 3: 启动多窗格
echo   python START_MULTI_PANE.py ui,coder
echo.
echo ========================================
echo.
echo 可用实例:
echo   - ui       (UI/UX 设计师)
echo   - coder   (开发者)
echo   - test    (QA 工程师)
echo   - default (协调者)
echo.
echo ========================================
echo.
echo 示例:
echo   python START_MULTI_PANE.py ui,coder
echo   python START_MULTI_PANE.py ui,coder,test
echo.
echo ========================================
echo.
pause
