#!/usr/bin/env python3
"""
WezTerm 多标签页启动器
在一个 WezTerm 窗口中创建多个标签页(tabs),每个运行 Claude 实例
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


def spawn_new_tab(wezterm_bin, cwd, instance_id, index, total):
    """在当前窗口创建一个新窗格并启动 Claude"""
    try:
        # 根据窗格数量决定分割方向和百分比
        # 2个窗格: 左右分割 50%
        # 3个窗格: 先左右50%，再上下50%
        # 4个窗格: 2x2网格
        # 5+个窗格: 自适应布局

        if total <= 2:
            # 左右分割
            direction = "--right"
            percent = 50
        elif total == 3:
            # 第2个窗格右侧分割，第3个在右侧上下分割
            if index == 1:
                direction = "--right"
                percent = 50
            else:
                direction = "--bottom"
                percent = 50
        else:
            # 更多窗格，使用底部分割，每次占用剩余空间的均分
            direction = "--bottom"
            # 计算百分比：剩余窗格数的均分
            remaining = total - index
            percent = int(100 / (remaining + 1))

        # 使用 split-pane 创建窗格
        cmd = [
            wezterm_bin,
            "cli",
            "split-pane",
            direction,
            "--percent",
            str(percent),
            "--cwd",
            str(cwd),
        ]

        print(f"[DEBUG] Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        print(f"[DEBUG] Return code: {result.returncode}")
        print(f"[DEBUG] Stdout: {result.stdout}")
        print(f"[DEBUG] Stderr: {result.stderr}")

        if result.returncode == 0:
            # 输出包含新创建的 pane_id
            pane_id = result.stdout.strip()
            print(f"[DEBUG] Created pane: {pane_id}")

            if pane_id:
                # 在新窗格中启动 Claude
                time.sleep(0.5)
                send_cmd = f"claude --dangerously-skip-permissions"
                print(f"[DEBUG] Sending to pane {pane_id}: {send_cmd}")

                result2 = subprocess.run(
                    [
                        wezterm_bin,
                        "cli",
                        "send-text",
                        "--pane-id",
                        pane_id,
                        "--no-paste",
                        send_cmd,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                print(f"[DEBUG] Send-text return code: {result2.returncode}")

                subprocess.run(
                    [
                        wezterm_bin,
                        "cli",
                        "send-text",
                        "--pane-id",
                        pane_id,
                        "--no-paste",
                    ],
                    input=b"\r",
                    capture_output=True,
                    timeout=5,
                )
                return pane_id
            return None
        else:
            print(f"[!] Failed to create pane: {result.stderr}")
            return None

    except Exception as e:
        print(f"[!] Exception creating pane: {e}")
        import traceback

        traceback.print_exc()
        return None


def set_tab_title(wezterm_bin, pane_id, title):
    """设置窗格标题"""
    try:
        # 使用 set-tab-title 设置当前标签页的标题
        result = subprocess.run(
            [wezterm_bin, "cli", "set-tab-title", "--pane-id", pane_id, title],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            print(f"[DEBUG] Set title for pane {pane_id}: {title}")
            return True
        else:
            print(f"[DEBUG] Failed to set title: {result.stderr}")
            return False
    except Exception as e:
        print(f"[DEBUG] Exception setting title: {e}")
        return False


def create_tab_mapping(work_dir, instance_tabs):
    """创建标签页映射文件"""
    config_dir = work_dir / ".cms_config"
    config_dir.mkdir(exist_ok=True)

    mapping_file = config_dir / "tab_mapping.json"

    mapping = {
        "work_dir": str(work_dir),
        "tabs": instance_tabs,
        "created_at": time.time(),
    }

    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"[+] Tab mapping saved to: {mapping_file}")
    return mapping_file


def is_in_wezterm():
    """检查是否在 WezTerm 中运行"""
    # 检查 WezTerm 环境变量
    wezterm_vars = [
        "WEZTERM_PANE",
        "WEZTERM_EXECUTABLE",
        "WEZTERM_VERSION",
    ]

    for var in wezterm_vars:
        if os.environ.get(var):
            return True

    # 检查 TERM 变量
    term = os.environ.get("TERM", "")
    if "wezterm" in term.lower():
        return True

    return False


def main():
    # 检查参数
    if len(sys.argv) < 2:
        print("Usage: python START_MULTI_TAB.py ui,coder,test")
        print()
        print("This script creates multiple tabs in WezTerm.")
        print()
        print("选项 1: 在 WezTerm 中运行 (推荐)")
        print("  1. 打开 WezTerm")
        print(f"  2. cd {Path.cwd()}")
        print(f"  3. python {Path(__file__).name} ui,coder,test")
        print()
        print("选项 2: 直接运行 (自动启动 WezTerm)")
        print(f"  python {Path(__file__).name} ui,coder,test")
        return 1

    # 解析实例
    instances_arg = sys.argv[1]
    instance_ids = [inst.strip() for inst in instances_arg.split(",") if inst.strip()]

    print(f"[*] Will create {len(instance_ids)} tabs for: {', '.join(instance_ids)}")
    print()

    # 加载配置
    from cms_start_config import load_start_config

    work_dir = Path.cwd()
    config = load_start_config(work_dir)
    claude_config = config.claude_config

    # 获取所有实例
    all_instances = {inst.id: inst for inst in claude_config.instances}

    # 自动创建未定义的实例
    from cms_start_config import ClaudeInstanceConfig

    for inst_id in instance_ids:
        if inst_id not in all_instances:
            print(f"[*] Auto-creating instance: {inst_id}")
            all_instances[inst_id] = ClaudeInstanceConfig(
                id=inst_id, role=f"Assistant ({inst_id})", autostart=True
            )

    wezterm_bin = _find_wezterm_bin()
    if not wezterm_bin:
        print("[!] WezTerm not found")
        return 1

    print(f"[+] WezTerm: {wezterm_bin}")
    print()

    # 检查是否在 WezTerm 中
    in_wezterm = is_in_wezterm()

    if not in_wezterm:
        print("=" * 60)
        print("  启动模式: 自动启动 WezTerm")
        print("=" * 60)
        print()
        print("将自动:")
        print(f"  1. 启动一个新的 WezTerm 窗口")
        print(f"  2. 在该窗口中创建 {len(instance_ids)} 个标签页")
        print("  3. 每个标签页启动一个 Claude 实例")
        print()
        print("=" * 60)
        print()
        print("[*] 启动 WezTerm...")

        # 首先启动一个 WezTerm 窗口
        first_instance = instance_ids[0]
        spec = all_instances[first_instance]

        try:
            # 启动第一个 WezTerm 窗口
            result = subprocess.Popen(
                [
                    wezterm_bin,
                    "start",
                    "--cwd",
                    str(work_dir),
                    "--",
                    "claude",
                    "--dangerously-skip-permissions",
                ],
                env={
                    **os.environ,
                    "CMS_CLAUDE_INSTANCE": first_instance,
                    "CMS_RUN_DIR": str(work_dir),
                },
            )

            print(f"[+] 启动第一个标签页: {first_instance} - {spec.role}")
            time.sleep(2)  # 等待 WezTerm 完全启动

            # 获取刚创建的 pane ID
            list_result = subprocess.run(
                [wezterm_bin, "cli", "list", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if list_result.returncode == 0:
                panes = []
                for line in list_result.stdout.strip().split("\n"):
                    if line.strip():
                        try:
                            panes.append(json.loads(line))
                        except:
                            pass

                if panes:
                    first_pane_id = str(panes[-1].get("pane_id", ""))
                    if first_pane_id:
                        # 设置第一个标签页的标题
                        set_tab_title(
                            wezterm_bin,
                            first_pane_id,
                            f"{first_instance} - {spec.role}",
                        )

                        instance_tabs = {
                            first_instance: {
                                "pane_id": first_pane_id,
                                "role": spec.role,
                            }
                        }

                        # 创建其余的标签页
                        for inst_id in instance_ids[1:]:
                            spec = all_instances[inst_id]
                            print(f"[*] 创建标签页: {inst_id} - {spec.role}")

                            pane_id = spawn_new_tab(wezterm_bin, work_dir, inst_id)
                            if pane_id:
                                set_tab_title(
                                    wezterm_bin, pane_id, f"{inst_id} - {spec.role}"
                                )
                                instance_tabs[inst_id] = {
                                    "pane_id": pane_id,
                                    "role": spec.role,
                                }
                                time.sleep(0.5)

                        # 保存映射
                        create_tab_mapping(work_dir, instance_tabs)

                        print()
                        print("=" * 60)
                        print("[✓] 所有标签页已创建!")
                        print("=" * 60)
                        print()
                        print("使用 send 命令进行通信:")
                        print()
                        for inst_id in instance_ids:
                            print(f'  bin\\send {inst_id} "你的消息"')
                        print()

                        return 0

        except Exception as e:
            print(f"[!] 错误: {e}")
            import traceback

            traceback.print_exc()
            return 1

    else:
        # 在 WezTerm 中运行
        print("=" * 60)
        print("  启动模式: 在当前 WezTerm 窗口中创建标签页")
        print("=" * 60)
        print()
        print("将在当前窗口中:")
        print(f"  1. 保持当前窗格作为第一个实例 ({instance_ids[0]})")
        print(f"  2. 创建 {len(instance_ids)-1} 个新窗格 (split-pane)")
        print("  3. 在每个窗格中启动 Claude")
        print("  4. 设置窗格标题为实例名称")
        print()
        print("  提示: 使用 Ctrl+Shift+方向键 在窗格间切换")
        print()
        print("=" * 60)
        print()
        print("[*] Starting setup...")
        print()

        # 获取当前 pane ID
        current_pane_id = os.environ.get("WEZTERM_PANE")
        if not current_pane_id:
            # 尝试通过 wezterm cli list 获取
            try:
                result = subprocess.run(
                    [wezterm_bin, "cli", "list", "--format", "json"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    panes = []
                    for line in result.stdout.strip().split("\n"):
                        if line.strip():
                            try:
                                panes.append(json.loads(line))
                            except:
                                pass
                    if panes:
                        current_pane_id = str(panes[0].get("pane_id", ""))
            except:
                pass

        # 第一个实例在当前窗格
        first_instance = instance_ids[0]
        spec = all_instances[first_instance]

        print(f"[*] Pane 1 (current): {first_instance} - {spec.role}")
        print(f"[DEBUG] Current pane ID: {current_pane_id}")

        # 在当前窗格启动 Claude
        print(f"[*] Starting Claude in current pane...")
        if current_pane_id:
            subprocess.run(
                [
                    wezterm_bin,
                    "cli",
                    "send-text",
                    "--pane-id",
                    current_pane_id,
                    "--no-paste",
                    "claude --dangerously-skip-permissions",
                ],
                capture_output=True,
                timeout=5,
            )
            subprocess.run(
                [
                    wezterm_bin,
                    "cli",
                    "send-text",
                    "--pane-id",
                    current_pane_id,
                    "--no-paste",
                ],
                input=b"\r",
                capture_output=True,
                timeout=5,
            )
            time.sleep(1)  # 等待 Claude 启动

            set_tab_title(
                wezterm_bin, current_pane_id, f"{first_instance} - {spec.role}"
            )
        else:
            print(f"[!] Warning: Could not get current pane ID")

        instance_tabs = {}
        if current_pane_id:
            instance_tabs[first_instance] = {
                "pane_id": current_pane_id,
                "role": spec.role,
            }

        print()

        # 为其他实例创建新窗格
        for i, inst_id in enumerate(instance_ids[1:], 1):
            spec = all_instances[inst_id]
            print(f"[*] Creating pane {i+1} for {inst_id} ({spec.role})...")

            pane_id = spawn_new_tab(wezterm_bin, work_dir, inst_id)

            if pane_id:
                print(f"[+] Created pane {i+1}: {inst_id}")
                set_tab_title(wezterm_bin, pane_id, f"{inst_id} - {spec.role}")
                instance_tabs[inst_id] = {"pane_id": pane_id, "role": spec.role}
                time.sleep(0.5)
            else:
                print(f"[!] Failed to create pane {i+1}")

        print()

        # 保存映射
        create_tab_mapping(work_dir, instance_tabs)

        print()
        print("=" * 60)
        print("[✓] Setup complete!")
        print("=" * 60)
        print()
        print("Use send command to communicate:")
        print()
        for inst_id in instance_ids:
            print(f'  bin\\send {inst_id} "your message"')
        print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(130)
