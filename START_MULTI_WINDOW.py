#!/usr/bin/env python3
"""
WezTerm 多窗口启动器
启动多个独立的 WezTerm 窗口，每个运行 Claude 实例
"""

import sys
import os
import subprocess
import time
import json
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


def check_wezterm():
    """检查 WezTerm 是否可用"""
    wezterm_bin = _find_wezterm_bin()
    if not wezterm_bin:
        return False, "WezTerm not found"

    try:
        result = subprocess.run(
            [wezterm_bin, "--version"], capture_output=True, timeout=5
        )
        if result.returncode == 0:
            return True, wezterm_bin
    except:
        pass

    return False, "WezTerm not working"


def list_wezterm_windows(wezterm_bin):
    """列出所有 WezTerm 窗口"""
    try:
        result = subprocess.run(
            [wezterm_bin, "cli", "list", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            # Parse JSON output
            windows = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    try:
                        data = json.loads(line)
                        windows.append(data)
                    except:
                        pass
            return windows
    except Exception as e:
        print(f"[!] Error listing windows: {e}")

    return []


def get_window_id_field(wezterm_bin):
    """检测 WezTerm 版本，确定使用哪个字段作为 window ID"""
    try:
        result = subprocess.run(
            [wezterm_bin, "--version"], capture_output=True, text=True, timeout=5
        )
        version = result.stdout.strip()
        print(f"[*] WezTerm version: {version}")

        # 根据版本返回字段名
        # 新版本使用 window_id，旧版本使用 window_id 或其他字段
        # 这里我们先尝试 window_id
        return "window_id"
    except:
        # 默认使用 window_id
        return "window_id"


def create_window_mapping(work_dir, instance_windows):
    """创建窗口映射文件"""
    config_dir = work_dir / ".cms_config"
    config_dir.mkdir(exist_ok=True)

    mapping_file = config_dir / "window_mapping.json"

    mapping = {
        "work_dir": str(work_dir),
        "windows": instance_windows,
        "created_at": time.time(),
    }

    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"[+] Created window mapping: {mapping_file}")
    return mapping_file


def main():
    # 检查参数
    if len(sys.argv) < 2:
        print("Usage: python START_MULTI_WINDOW.py ui,coder,test")
        print()
        print(
            "This script creates multiple WezTerm windows, each running a Claude instance."
        )
        print()
        print("Each window will have:")
        print("  - Window title set to instance name")
        print("  - Independent Claude instance")
        print("  - Ability to communicate via 'send' command")
        return 1

    # 检查 WezTerm
    ok, result = check_wezterm()
    if not ok:
        print(f"[!] {result}")
        print()
        print("Please install WezTerm:")
        print("  https://wezfurlong.org/wezterm/")
        return 1

    wezterm_bin = result
    print(f"[+] WezTerm found: {wezterm_bin}")
    print()

    # 解析实例
    instances_arg = sys.argv[1]
    instance_ids = [inst.strip() for inst in instances_arg.split(",") if inst.strip()]

    print(f"[*] Will create {len(instance_ids)} windows for: {', '.join(instance_ids)}")
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

    print("=" * 60)
    print("  INSTRUCTIONS")
    print("=" * 60)
    print()
    print("This script will:")
    print(f"  1. Create {len(instance_ids)} independent WezTerm windows")
    print("  2. Start Claude in each window")
    print("  3. Set window title to instance name")
    print("  4. Enable communication via 'send' command")
    print()
    print("=" * 60)
    print()
    print("[*] Starting setup...")
    print()

    # 获取启动前的窗口列表
    print("[*] Listing existing windows...")
    initial_windows = list_wezterm_windows(wezterm_bin)
    initial_window_ids = set()

    window_id_field = get_window_id_field(wezterm_bin)

    for win in initial_windows:
        if window_id_field in win:
            initial_window_ids.add(win[window_id_field])

    print(f"[*] Found {len(initial_window_ids)} existing windows")
    print()

    # 启动每个实例的新窗口
    instance_windows = {}

    for i, inst_id in enumerate(instance_ids):
        spec = all_instances[inst_id]
        print(f"[*] Creating window {i+1} for {inst_id} ({spec.role})...")

        # 准备环境变量
        env = os.environ.copy()
        env["CMS_CLAUDE_INSTANCE"] = inst_id
        env["CMS_RUN_DIR"] = str(work_dir)
        env["WEZTERM_WINDOW_TITLE"] = inst_id  # 设置窗口标题

        # 使用 wezterm start 启动新窗口
        # 方法1: 直接启动 claude
        start_cmd = [
            str(wezterm_bin),
            "start",
            "--",
            "claude",
            "--dangerously-skip-permissions",
        ]

        try:
            # 在后台启动
            subprocess.Popen(
                start_cmd,
                env=env,
                cwd=str(work_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"[+] Started window {i+1}")
            time.sleep(1)  # 等待窗口启动
        except Exception as e:
            print(f"[!] Failed to start window {i+1}: {e}")

    print()
    print("[*] Waiting for windows to initialize...")
    time.sleep(2)

    # 获取启动后的窗口列表
    print("[*] Detecting new windows...")
    final_windows = list_wezterm_windows(wezterm_bin)

    # 找出新创建的窗口
    new_windows = []
    for win in final_windows:
        if window_id_field in win:
            win_id = win[window_id_field]
            if win_id not in initial_window_ids:
                new_windows.append(win)

    print(f"[+] Found {len(new_windows)} new windows")
    print()

    # 将实例ID映射到窗口ID
    # 假设新窗口按创建顺序排列
    if len(new_windows) == len(instance_ids):
        for i, win in enumerate(new_windows):
            inst_id = instance_ids[i]
            win_id = win[window_id_field]
            instance_windows[inst_id] = {
                "window_id": win_id,
                "instance_id": inst_id,
                "title": inst_id,
            }
            print(f"[+] Mapped instance '{inst_id}' to window {win_id}")

        # 创建映射文件
        create_window_mapping(work_dir, instance_windows)
    else:
        print(
            f"[!] Warning: Expected {len(instance_ids)} windows, found {len(new_windows)}"
        )
        print("[!] Window mapping may be incorrect")
        print()
        print("Available windows:")
        for i, win in enumerate(new_windows):
            print(f"  Window {i}: {win}")

    print()
    print("=" * 60)
    print("  SETUP COMPLETE")
    print("=" * 60)
    print()
    print(f"[*] Created {len(instance_ids)} WezTerm windows")
    print("[*] Each window should be running Claude")
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
