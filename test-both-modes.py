#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试两种发送模式的区别
必须在 WezTerm 标签页内运行
"""

import sys
import json
import subprocess
import shutil
from pathlib import Path


def find_wezterm():
    """查找 WezTerm 可执行文件"""
    wezterm = shutil.which("wezterm") or shutil.which("wezterm.exe")
    if not wezterm:
        common_paths = [
            Path.home() / "AppData" / "Local" / "Microsoft" / "WindowsApps" / "wezterm.exe",
            Path("C:/Program Files/WezTerm/wezterm.exe"),
        ]
        for path in common_paths:
            if path.exists():
                return str(path)
    return wezterm


def load_config():
    work_dir = Path.cwd()
    mapping_file = work_dir / ".cms_config" / "tab_mapping.json"

    if not mapping_file.exists():
        return None

    try:
        with open(mapping_file, "r", encoding="utf-8-sig") as f:
            mapping = json.load(f)
    except:
        with open(mapping_file, "r", encoding="utf-8") as f:
            mapping = json.load(f)

    return mapping.get("tabs", {})


def test_mode(wezterm_bin, pane_id, message, use_no_paste):
    """测试指定模式"""
    mode_name = "no-paste" if use_no_paste else "bracketed-paste"
    message_with_newline = message + "\n"
    
    cmd = [wezterm_bin, "cli", "send-text", "--pane-id", str(pane_id)]
    if use_no_paste:
        cmd.append("--no-paste")
    cmd.append(message_with_newline)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=5,
        )
        
        if result.returncode == 0:
            print(f"[{mode_name}] SUCCESS: Message sent")
            return True
        else:
            print(f"[{mode_name}] FAILED: {result.stderr}")
            return False
    except Exception as e:
        print(f"[{mode_name}] ERROR: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python test-both-modes.py <instance> [message]")
        print("Examples:")
        print("  python test-both-modes.py c2")
        print("  python test-both-modes.py c2 'custom message'")
        return 1

    instance = sys.argv[1].lower()
    message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "test message"

    wezterm_bin = find_wezterm()
    if not wezterm_bin:
        print("[ERROR] WezTerm not found")
        return 1

    tabs = load_config()
    if not tabs:
        print("[ERROR] Could not load tab_mapping.json")
        return 1

    if instance not in tabs:
        print(f"[ERROR] Unknown instance '{instance}'")
        print(f"Available: {', '.join(tabs.keys())}")
        return 1

    tab_info = tabs[instance]
    pane_id = tab_info.get("pane_id", tab_info.get("tab_index"))

    if not pane_id:
        print(f"[ERROR] No pane_id found for {instance}")
        return 1

    print(f"\n=== Testing message send to {instance} (pane {pane_id}) ===")
    print(f"Message: '{message}'")
    print()
    
    print("Test 1: Bracketed Paste Mode (default)")
    test_mode(wezterm_bin, pane_id, message + " [bracketed]", False)
    
    print()
    input("Press Enter to continue to test 2...")
    print()
    
    print("Test 2: No-Paste Mode (direct)")
    test_mode(wezterm_bin, pane_id, message + " [no-paste]", True)
    
    print()
    print("=== Tests complete ===")
    print("Check the target pane to see which mode auto-submits!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
