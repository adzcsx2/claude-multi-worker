#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 WezTerm 获取当前运行的窗格并创建 c1, c2, c3 映射
"""

import json
import subprocess
import shutil
from pathlib import Path

project_dir = Path.cwd()
config_dir = project_dir / ".cms_config"
mapping_file = config_dir / "tab_mapping.json"

# 查找 WezTerm
wezterm = shutil.which("wezterm") or shutil.which("wezterm.exe")
if not wezterm:
    common_path = Path("C:/Program Files/WezTerm/wezterm.exe")
    if common_path.exists():
        wezterm = str(common_path)

if not wezterm:
    print("[ERROR] WezTerm not found")
    print("Please install WezTerm from: https://wezfurlong.org/wezterm/")
    exit(1)

print(f"[OK] Found WezTerm: {wezterm}")
print("[INFO] Running wezterm cli list...")

# 获取所有窗格
try:
    # 尝试使用当前终端的环境
    import os

    env = os.environ.copy()

    # 使用文本格式（更稳定）
    result = subprocess.run(
        [wezterm, "cli", "list"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        timeout=5,
        env=env,
        cwd=str(project_dir),
    )

    print(f"[DEBUG] Return code: {result.returncode}")
    if result.stdout:
        print(f"[DEBUG] Output lines: {len(result.stdout.split(chr(10)))}")
    if result.stderr:
        print(f"[DEBUG] Stderr: {result.stderr[:200]}")

    if result.returncode != 0:
        print("[ERROR] Failed to get pane list from WezTerm")
        print("\n=== Troubleshooting ===")
        print("1. Make sure you are running this script FROM INSIDE a WezTerm tab")
        print("2. Try running manually first: wezterm cli list")
        print(
            "3. If manual command works but script fails, there's an environment issue"
        )
        exit(1)

    if not result.stdout:
        print("[ERROR] No output from wezterm cli list")
        exit(1)

    # 解析文本格式输出
    panes = []
    lines = result.stdout.strip().split("\n")

    for line in lines[1:]:  # 跳过表头
        if not line.strip():
            continue

        # 解析每一行: WINID TABID PANEID WORKSPACE SIZE TITLE
        parts = line.split()
        if len(parts) >= 3:
            try:
                pane_id = int(parts[2])  # PANEID 在第3列
                panes.append({"pane_id": pane_id})
            except:
                pass

    if len(panes) < 3:
        print(f"[ERROR] Found only {len(panes)} panes, need at least 3")
        print("\nPlease make sure you have 3 WezTerm windows/tabs open")
        exit(1)

    print(f"[OK] Found {len(panes)} panes")

    # 创建 c1, c2, c3 映射
    config_dir.mkdir(exist_ok=True)

    mapping = {
        "work_dir": str(project_dir),
        "tabs": {
            "c1": {"pane_id": str(panes[0]["pane_id"]), "role": "Design"},
            "c2": {"pane_id": str(panes[1]["pane_id"]), "role": "Main"},
            "c3": {"pane_id": str(panes[2]["pane_id"]), "role": "Test"},
        },
        "created_at": panes[0].get("created_at", 0),
    }

    # 保存映射
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"[OK] Tab mapping created: {mapping_file}")
    print("")
    print("Pane mappings:")
    print(f"  c1 (Design) -> pane {panes[0]['pane_id']}")
    print(f"  c2 (Main)   -> pane {panes[1]['pane_id']}")
    print(f"  c3 (Test)   -> pane {panes[2]['pane_id']}")
    print("")
    print("Test with:")
    print('  python send-tab.py c1 "继续"')
    print('  python send-tab.py c2 "继续"')
    print('  python send-tab.py c3 "继续"')
    print("")

except subprocess.TimeoutExpired:
    print("[ERROR] WezTerm CLI timeout")
    print("Make sure WezTerm is running")
    exit(1)
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback

    traceback.print_exc()
    exit(1)
