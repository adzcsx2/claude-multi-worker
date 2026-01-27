#!/usr/bin/env python3
"""测试 WezTerm 窗格创建和标题设置"""

import subprocess
import time
import json

wezterm = "C:\\Program Files\\WezTerm\\wezterm.exe"

print("=" * 60)
print("测试 WezTerm CLI 功能")
print("=" * 60)
print()

# 测试 1: 列出当前窗格
print("1. 列出当前窗格...")
result = subprocess.run(
    [wezterm, "cli", "list", "--format", "json"], capture_output=True, text=True
)
if result.returncode == 0:
    print("✅ 成功")
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            try:
                pane = json.loads(line)
                print(f"   Pane ID: {pane.get('pane_id')}, Title: {pane.get('title')}")
            except:
                pass
else:
    print(f"❌ 失败: {result.stderr}")

print()

# 测试 2: 创建新窗格
print("2. 创建新窗格...")
result = subprocess.run([wezterm, "cli", "split-pane"], capture_output=True, text=True)
if result.returncode == 0:
    new_pane_id = result.stdout.strip()
    print(f"✅ 成功创建窗格: {new_pane_id}")

    # 测试 3: 在新窗格中发送命令
    print()
    print("3. 在新窗格中发送命令...")
    time.sleep(0.5)
    result = subprocess.run(
        [
            wezterm,
            "cli",
            "send-text",
            "--pane-id",
            new_pane_id,
            "--no-paste",
            "echo Hello from new pane",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("✅ 发送文本成功")
        subprocess.run(
            [wezterm, "cli", "send-text", "--pane-id", new_pane_id, "--no-paste"],
            input=b"\r",
        )
    else:
        print(f"❌ 失败: {result.stderr}")

    # 测试 4: 设置标题
    print()
    print("4. 设置窗格标题...")
    result = subprocess.run(
        [wezterm, "cli", "set-tab-title", "--pane-id", new_pane_id, "Test Pane"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("✅ 设置标题成功")
    else:
        print(f"❌ 失败: {result.stderr}")
        print("   尝试不带 --pane-id 参数...")
        result2 = subprocess.run(
            [wezterm, "cli", "set-tab-title", "Test Pane"],
            capture_output=True,
            text=True,
        )
        if result2.returncode == 0:
            print("   ✅ 不带参数成功")
        else:
            print(f"   ❌ 仍然失败: {result2.stderr}")
else:
    print(f"❌ 创建窗格失败: {result.stderr}")

print()
print("=" * 60)
print("测试完成")
print("=" * 60)
