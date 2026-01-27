@echo off
echo ========================================
echo   CMS 自动化测试启动器
echo ========================================
echo.
echo 📋 测试任务: 创建简单计算器
echo.
echo 🚀 接下来的步骤:
echo.
echo 1. 打开 WezTerm (如果尚未打开)
echo 2. 创建 3 个窗格 (Ctrl+Shift+T)
echo 3. 在每个窗格运行: claude
echo 4. 在窗格 1 输入: 我是 C1 窗口。启动自动化模式。
echo 5. 在窗格 2 输入: 我是 C2 窗口。启动自动化模式。
echo 6. 在窗格 3 输入: 我是 C3 窗口。启动自动化模式。
echo.
echo ========================================
echo.
echo 📁 当前任务配置:
echo.
type task-comms\automation-state.md | findstr /C:"Current Step" /C:"Current Window" /C:"Current Task"
echo.
echo ========================================
echo.
echo 💡 提示:
echo - 每完成一个窗口的任务，系统会提示切换到下一个窗口
echo - 切换后输入"继续"即可执行下一步
echo.
echo 📖 查看完整测试指南:
echo    type START_TEST.md
echo.
echo 🔍 监控进度:
echo    type task-comms\automation-state.md
echo.
pause
