"""
手动创建映射 - 适用于非 WezTerm 的 Claude 窗口
"""
import json
from pathlib import Path

print("=" * 60)
print("  手动创建 Tab Mapping")
print("=" * 60)
print()
print("由于无法自动检测窗口，需要手动输入 pane ID")
print()
print("如果你不知道 pane ID，可以使用简单的编号：")
print("  c1 -> 0")
print("  c2 -> 1")  
print("  c3 -> 2")
print()

try:
    c1_pane = input("C1 的 pane_id (或按回车使用 '0'): ").strip() or "0"
    c2_pane = input("C2 的 pane_id (或按回车使用 '1'): ").strip() or "1"
    c3_pane = input("C3 的 pane_id (或按回车使用 '2'): ").strip() or "2"
    
    project_dir = Path.cwd()
    config_dir = project_dir / ".cms_config"
    config_dir.mkdir(exist_ok=True)
    
    mapping = {
        "work_dir": str(project_dir),
        "tabs": {
            "c1": {"pane_id": c1_pane, "role": "Design"},
            "c2": {"pane_id": c2_pane, "role": "Main"},
            "c3": {"pane_id": c3_pane, "role": "Test"},
        },
        "created_at": 0
    }
    
    mapping_file = config_dir / "tab_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print()
    print("[OK] 映射已创建!")
    print(f"文件: {mapping_file}")
    print()
    print("映射关系:")
    print(f"  c1 -> pane {c1_pane}")
    print(f"  c2 -> pane {c2_pane}")
    print(f"  c3 -> pane {c3_pane}")
    print()
    print("⚠️  注意: 如果你的 Claude 窗口不是 WezTerm")
    print("   send-tab.py 将无法工作（它需要 wezterm cli）")
    print()
    print("建议:")
    print("  1. 关闭当前所有窗口")
    print("  2. 运行: python START_WEZTERM_SIMPLE.py")
    print("  3. 这会启动3个真正的 WezTerm 窗口")
    print()
    
except KeyboardInterrupt:
    print("\n[!] 已取消")
    exit(1)
