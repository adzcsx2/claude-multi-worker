#!/usr/bin/env python3
"""快速测试脚本"""

import sys
from pathlib import Path

print("=" * 60)
print("CMS 快速测试")
print("=" * 60)
print()

# 测试 1: 检查文件
print("📁 检查文件...")
files_to_check = [
    "cms.py",
    "START_MULTI_TAB.py",
    "START_MULTI_PANE.py",
    "START_MULTI_WINDOW.py",
    "bin/send",
]

for f in files_to_check:
    exists = Path(f).exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {f}")

print()

# 测试 2: 检查配置目录
print("📂 检查配置...")
config_dir = Path(".cms_config")
if config_dir.exists():
    print(f"  ✅ .cms_config 目录存在")
    config_file = config_dir / "cms.config"
    if config_file.exists():
        print(f"  ✅ cms.config 存在")
        import json

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            instances = config.get("claude", {}).get("instances", [])
            print(f"  ✅ 配置的实例: {[i.get('id') for i in instances]}")
        except Exception as e:
            print(f"  ❌ 读取配置失败: {e}")
    else:
        print(f"  ⚠️  cms.config 不存在")
else:
    print(f"  ⚠️  .cms_config 目录不存在")

print()

# 测试 3: 测试导入
print("📦 测试模块导入...")
sys.path.insert(0, str(Path("lib")))
try:
    from cms_start_config import load_start_config

    print("  ✅ cms_start_config 导入成功")

    config = load_start_config(Path.cwd())
    print(f"  ✅ 配置加载成功")
    print(f"  ✅ Claude实例: {[i.id for i in config.claude_config.instances]}")
except Exception as e:
    print(f"  ❌ 导入失败: {e}")

print()

# 测试 4: 检查 WezTerm
print("🖥️  检查 WezTerm...")
import shutil

wezterm = shutil.which("wezterm") or shutil.which("wezterm.exe")
if wezterm:
    print(f"  ✅ WezTerm 已安装: {wezterm}")
    try:
        import subprocess

        result = subprocess.run(
            [wezterm, "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"  ✅ 版本: {result.stdout.strip()}")
    except:
        pass
else:
    print(f"  ⚠️  WezTerm 未找到 (需要安装才能使用)")

print()

# 测试 5: 显示正确用法
print("📖 正确用法:")
print()
print("  方式 1 (推荐 - Windows):")
print("    cms.bat tab")
print("    cms.bat tab ui,coder,test")
print()
print("  方式 2 (跨平台):")
print("    python cms.py tab")
print("    python cms.py tab ui,coder,test")
print()
print("  方式 3 (直接调用):")
print("    python START_MULTI_TAB.py ui,coder,test")
print()
print("  ❌ 错误用法:")
print("    python cms.bat tab    # .bat 不能用 python 执行!")
print()

print("=" * 60)
print("测试完成!")
print("=" * 60)
