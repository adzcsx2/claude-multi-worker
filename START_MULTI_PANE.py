#!/usr/bin/env python3
"""
WezTerm 多窗格启动器 v2
在一个 WezTerm 窗口中创建多个子窗格，每个运行 Claude 实例
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add lib to path
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir / "lib"))


def _find_wezterm_bin():
    """查找 WezTerm"""
    import shutil

    override = os.environ.get("CODEX_WEZTERM_BIN") or os.environ.get("WEZTERM_BIN")
    if override and Path(override).exists():
        return override
    return shutil.which("wezterm") or shutil.which("wezterm.exe")


def check_wezterm_env():
    """检查是否在 WezTerm 中运行"""
    # WezTerm 可能设置的环境变量
    wezterm_vars = [
        "WEZTERM_PANE_ID",
        "WEZTERM_WINDOW_ID",
        "WEZTERM_TAB_ID",
        "WEZTERM_VERSION",
        "WEZTERM_EXECUTABLE",
        # Windows 特定
        "TERM_PROGRAM",
        "TERM",
    ]

    # 检查是否有任何 WezTerm 相关的环境变量
    for var in wezterm_vars:
        if os.environ.get(var):
            return True

    # 检查 WezTerm 可执行文件路径
    wezterm_exe = _find_wezterm_bin()
    if wezterm_exe and "wezterm" in wezterm_exe.lower():
        return True

    # 放宽检测：如果在 PATH 中找到 wezterm，认为可能在 WezTerm 中
    import shutil

    if shutil.which("wezterm.exe") or shutil.which("wezterm"):
        return True

    # 最终检查：是否可以运行 wezterm cli
    try:
        result = subprocess.run(
            ["wezterm", "cli", "--help"], capture_output=True, timeout=2
        )
        # 如果能运行 wezterm cli，很可能在 WezTerm 环境中
        return result.returncode == 0
    except:
        pass

    return False


def main():
    # 检查参数
    if len(sys.argv) < 2:
        print("Usage: python START_MULTI_PANE.py ui,coder,test")
        print()
        print("This script creates multiple panes in one WezTerm window.")
        print()
        print("IMPORTANT: Run this script from within WezTerm!")
        return 1

    # 检查环境
    if not check_wezterm_env():
        print("[!] Not running in WezTerm")
        print()
        print("Please:")
        print("  1. Open WezTerm")
        print("  2. Navigate to your project:")
        print(f"     cd {Path.cwd()}")
        print(f"  3. Run this script:")
        print(f"     python {Path(__file__).name} ui,coder,test")
        return 1

    # 解析实例
    instances_arg = sys.argv[1]
    instance_ids = [inst.strip() for inst in instances_arg.split(",") if inst.strip()]

    print(f"[*] Will create {len(instance_ids)} panes for: {', '.join(instance_ids)}")
    print()

    # 加载配置
    from cms_start_config import load_start_config

    work_dir = Path.cwd()
    config = load_start_config(work_dir)
    claude_config = config.claude_config

    # 获取所有实例
    all_instances = {inst.id: inst for inst in claude_config.instances}

    # 验证
    for inst_id in instance_ids:
        if inst_id not in all_instances:
            print(f"[!] Unknown instance: {inst_id}")
            return 1

    wezterm_bin = _find_wezterm_bin()
    if not wezterm_bin:
        print("[!] WezTerm not found")
        return 1

    print(f"[+] WezTerm: {wezterm_bin}")
    print()
    print("=" * 60)
    print("  INSTRUCTIONS")
    print("=" * 60)
    print()
    print("This script will:")
    print(f"  1. Create {len(instance_ids)} panes in this WezTerm window")
    print("  2. Start Claude in each pane")
    print("  3. Set pane titles to instance names")
    print()
    print("=" * 60)
    print()
    print("[*] Starting setup...")
    print()

    # 创建分割窗格的命令
    # 注意：WezTerm split-pane 会返回新 pane 的 ID
    current_pane_id = os.environ.get("WEZTERM_PANE_ID", "")

    # 第一个实例在当前窗格
    first_instance = instance_ids[0]
    spec = all_instances[first_instance]

    print(f"[*] Pane 1 (current): {first_instance} - {spec.role}")
    print()

    # 为其他实例创建新窗格
    directions = ["right", "bottom", "left", "top"]
    created_panes = []

    for i, inst_id in enumerate(instance_ids[1:], 1):
        direction = directions[min(i - 1, len(directions) - 1)]
        percent = 50 if len(instance_ids) == 2 else (33 if i == 1 else 50)

        spec = all_instances[inst_id]
        print(f"[*] Creating pane {i+1} for {inst_id} ({direction}, {percent}%)...")

        # 准备环境变量
        env = os.environ.copy()
        env["CMS_CLAUDE_INSTANCE"] = inst_id
        env["CMS_RUN_DIR"] = str(work_dir)

        # 使用 WezTerm CLI 分割窗格并启动 Claude
        # 方法：使用 wezterm cli split-pane --right --percent 50 -- sh "cd /path && claude"
        claude_cmd = [
            str(wezterm_bin),
            "cli",
            "split-pane",
            f"--{direction}",
            f"--percent={percent}",
            "--cwd",
            str(work_dir),
            "--",
            "claude",
            "--dangerously-skip-permissions",
        ]

        try:
            # 运行 split-pane 命令
            result = subprocess.run(
                claude_cmd, env=env, capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                print(f"[+] Created pane {i+1}")
                time.sleep(0.5)  # 等待启动
            else:
                print(f"[!] Failed to create pane {i+1}")
                print(f"    Error: {result.stderr}")
        except Exception as e:
            print(f"[!] Exception: {e}")

    print()
    print("=" * 60)
    print("  SETUP COMPLETE")
    print("=" * 60)
    print()
    print("[*] Claude instances should be starting in each pane")
    print("[*] Use Ctrl+Shift+Arrow keys to switch between panes")
    print()
    print("[*] Use send command to communicate:")
    for inst_id in instance_ids:
        print(f"     bin\\send {inst_id} <message>")
    print()
    print("[*] View status:")
    print("     show-status.bat")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
