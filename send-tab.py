#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 WezTerm CLI 发送消息到指定窗格
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
        # 尝试常见安装路径
        common_paths = [
            Path.home()
            / "AppData"
            / "Local"
            / "Microsoft"
            / "WindowsApps"
            / "wezterm.exe",
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


def main():
    if len(sys.argv) < 3:
        print("Usage: send-tab <instance> <message>")
        print("Examples:")
        print("  python send-tab.py c1 '继续'")
        print("  python send-tab.py c2 '继续'")
        return 1

    instance = sys.argv[1].lower()
    message = " ".join(sys.argv[2:])

    # 查找 WezTerm
    wezterm_bin = find_wezterm()
    if not wezterm_bin:
        print("[ERROR] WezTerm not found")
        print("Please install WezTerm from https://wezfurlong.org/wezterm/")
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

    try:
        # 使用 WezTerm CLI 发送文本 - 两步策略
        # 第一步: 发送消息内容
        result1 = subprocess.run(
            [
                wezterm_bin,
                "cli",
                "send-text",
                "--pane-id",
                str(pane_id),
                "--no-paste",
                message,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=5,
        )

        if result1.returncode != 0:
            print(f"[ERROR] Failed to send message: {result1.stderr}")
            return 1

        # 第二步: 发送回车键提交
        result2 = subprocess.run(
            [wezterm_bin, "cli", "send-text", "--pane-id", str(pane_id), "--no-paste"],
            input=b"\r",  # 通过 stdin 发送回车键
            capture_output=True,
            timeout=5,
        )

        if result2.returncode == 0:
            print(
                f"[OK] Message sent and submitted to {instance} (pane {pane_id}): '{message}'"
            )
            return 0
        else:
            stderr_msg = (
                result2.stderr.decode("utf-8", errors="ignore")
                if result2.stderr
                else ""
            )
            print(f"[ERROR] Failed to submit: {stderr_msg}")
            return 1

    except subprocess.TimeoutExpired:
        print(f"[ERROR] Command timeout")
        return 1
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
