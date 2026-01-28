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


def spawn_new_tab(wezterm_bin, cwd, instance_id):
    """在当前窗口创建一个新标签页(tab)并启动 Claude"""
    try:
        # 使用 spawn 创建新标签页（不使用 --new-window）
        cmd = [
            wezterm_bin,
            "cli",
            "spawn",
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
            print(f"[DEBUG] Created tab with pane: {pane_id}")

            if pane_id:
                # 在新标签页中启动 Claude
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
                        send_cmd + "\n",  # 添加换行符自动执行
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                print(f"[DEBUG] Send-text return code: {result2.returncode}")

                return pane_id
            return None
        else:
            print(f"[!] Failed to create tab: {result.stderr}")
            return None

    except Exception as e:
        print(f"[!] Exception creating tab: {e}")
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
    # 检查参数 - 默认使用 c1,c2,c3
    if len(sys.argv) < 2:
        print("Using default instances: c1,c2,c3")
        instances_arg = "c1,c2,c3"
    else:
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

        try:
            # 使用 wezterm start 直接启动带命令的第一个标签页
            first_instance = instance_ids[0]
            spec = all_instances[first_instance]

            # 启动 WezTerm 并在第一个标签页运行 pwsh（等待命令）
            result = subprocess.Popen(
                [
                    wezterm_bin,
                    "start",
                    "--cwd",
                    str(work_dir),
                    "pwsh",
                    "-NoExit",
                    "-Command",
                    f"Write-Host '[{first_instance}] Ready. Starting Claude...'; claude --dangerously-skip-permissions",
                ],
            )

            print(f"[+] WezTerm 窗口已启动，第一个标签页: {first_instance}")
            print("[*] 等待 WezTerm 初始化...")
            time.sleep(4)  # 等待 WezTerm 完全启动并准备好 CLI

            # 验证 CLI 是否可用
            max_retries = 5
            cli_ready = False
            for retry in range(max_retries):
                try:
                    test_result = subprocess.run(
                        [wezterm_bin, "cli", "list"],
                        capture_output=True,
                        timeout=2,
                    )
                    if test_result.returncode == 0:
                        cli_ready = True
                        print("[+] WezTerm CLI 已就绪")
                        break
                except:
                    pass
                print(f"[*] 等待 CLI 就绪... ({retry+1}/{max_retries})")
                time.sleep(1)

            if not cli_ready:
                print("[!] WezTerm CLI 未就绪，无法继续")
                return 1

            # 获取第一个窗格的 pane_id
            list_result = subprocess.run(
                [wezterm_bin, "cli", "list", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            first_pane_id = None
            if list_result.returncode == 0:
                panes = []
                for line in list_result.stdout.strip().split("\n"):
                    if line.strip():
                        try:
                            panes.append(json.loads(line))
                        except:
                            pass
                if panes:
                    first_pane_id = str(panes[0].get("pane_id", ""))

            instance_tabs = {}

            # 设置第一个标签页
            if first_pane_id:
                set_tab_title(
                    wezterm_bin, first_pane_id, f"{first_instance} - {spec.role}"
                )
                instance_tabs[first_instance] = {
                    "pane_id": first_pane_id,
                    "role": spec.role,
                }
                print(
                    f"[+] 第一个标签页已配置: {first_instance} (pane {first_pane_id})"
                )

            # 为其余实例创建标签页
            for i, inst_id in enumerate(instance_ids[1:], 1):
                spec = all_instances[inst_id]
                print(
                    f"[*] 创建标签页 {i+1}/{len(instance_ids)}: {inst_id} - {spec.role}"
                )

                pane_id = spawn_new_tab(wezterm_bin, work_dir, inst_id)
                if pane_id:
                    set_tab_title(wezterm_bin, pane_id, f"{inst_id} - {spec.role}")
                    instance_tabs[inst_id] = {
                        "pane_id": pane_id,
                        "role": spec.role,
                    }
                    time.sleep(1)
                else:
                    print(f"[!] 创建标签页 {inst_id} 失败")

            # 保存映射
            if instance_tabs:
                create_tab_mapping(work_dir, instance_tabs)

                print()
                print("=" * 60)
                print("[✓] 所有标签页已创建!")
                print("=" * 60)
                print()
                print("使用 send-tab 命令进行通信:")
                print()
                for inst_id in instance_ids:
                    print(f'  python send-tab.py {inst_id} "继续"')
                print()
                return 0
            else:
                print("[!] 没有成功创建任何标签页")
                return 1

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
            print(f"[*] Creating tab {i+1} for {inst_id} ({spec.role})...")

            pane_id = spawn_new_tab(wezterm_bin, work_dir, inst_id)

            if pane_id:
                print(f"[+] Created tab {i+1}: {inst_id}")
                set_tab_title(wezterm_bin, pane_id, f"{inst_id} - {spec.role}")
                instance_tabs[inst_id] = {"pane_id": pane_id, "role": spec.role}
                time.sleep(0.5)
            else:
                print(f"[!] Failed to create tab {i+1}")

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
