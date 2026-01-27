#!/usr/bin/env python3
"""
CMS - Claude Multi Starter
一键启动多个 Claude 实例的快捷命令
"""

import sys
import os
from pathlib import Path

# Add lib to path
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir / "lib"))


def main():
    """Main entry point for cms command"""

    # 检查参数
    if len(sys.argv) < 2:
        print("CMS - Claude Multi Starter")
        print()
        print("Usage:")
        print("  python cms claude:ui,coder,test    # 启动多个Claude实例")
        print("  python cms claude                  # 启动默认实例 (ui,coder,test)")
        print()
        print("也支持传统模式:")
        print("  python cms tab ui,coder,test       # 标签页模式")
        print("  python cms pane ui,coder,test      # 窗格模式")
        print("  python cms window ui,coder,test    # 多窗口模式")
        print()
        return 1

    arg = sys.argv[1].lower()

    # 默认实例列表
    default_instances = "ui,coder,test"

    # 解析参数
    mode = None
    instances = default_instances

    # 新格式: claude:ui,coder,test
    if arg.startswith("claude:"):
        mode = "tab"  # 默认使用标签页模式
        instances = arg.split(":", 1)[1] if ":" in arg else default_instances
    elif arg == "claude":
        mode = "tab"
        instances = sys.argv[2] if len(sys.argv) >= 3 else default_instances
    # 传统格式: tab/pane/window
    elif arg in ["tab", "pane", "window"]:
        mode = arg
        instances = sys.argv[2] if len(sys.argv) >= 3 else default_instances
    else:
        print(f"Unknown command: {arg}", file=sys.stderr)
        print()
        print("Use: python cms claude:ui,coder,test")
        print("Or:  python cms pane ui,coder,test")
        return 1

    # 根据模式调用相应的启动脚本
    if mode == "tab":
        # 标签页模式
        start_script = script_dir / "START_MULTI_TAB.py"
        if start_script.exists():
            os.execv(sys.executable, [sys.executable, str(start_script), instances])
        else:
            print(f"Error: {start_script} not found", file=sys.stderr)
            return 1

    elif mode == "pane":
        # 窗格模式
        start_script = script_dir / "START_MULTI_PANE.py"
        if start_script.exists():
            os.execv(sys.executable, [sys.executable, str(start_script), instances])
        else:
            print(f"Error: {start_script} not found", file=sys.stderr)
            return 1

    elif mode == "window":
        # 多窗口模式
        start_script = script_dir / "START_MULTI_WINDOW.py"
        if start_script.exists():
            os.execv(sys.executable, [sys.executable, str(start_script), instances])
        else:
            print(f"Error: {start_script} not found", file=sys.stderr)
            return 1

    else:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        print()
        print("Available modes:")
        print("  tab     - 多标签页模式 (推荐)")
        print("  pane    - 多窗格模式")
        print("  window  - 多窗口模式")
        return 1

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(130)
