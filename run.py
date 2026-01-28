#!/usr/bin/env python3
"""
WezTerm Multi-Tab Launcher
Create multiple tabs in a WezTerm window, each running a Claude instance

Usage:
    python run.py

Description:
    Read configuration from cms.config and launch all instances with autostart: true
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
    """Find WezTerm binary"""
    import shutil

    override = os.environ.get("CODEX_WEZTERM_BIN") or os.environ.get("WEZTERM_BIN")
    if override and Path(override).exists():
        return override
    return shutil.which("wezterm") or shutil.which("wezterm.exe")


def check_wezterm():
    """Check if WezTerm is available"""
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


def spawn_new_tab(wezterm_bin, cwd, instance_id, claude_args=""):
    """Create a new tab in current window and start Claude"""
    try:
        # Use spawn to create new tab (not using --new-window)
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
            # Output contains newly created pane_id
            pane_id = result.stdout.strip()
            print(f"[DEBUG] Created tab with pane: {pane_id}")

            if pane_id:
                # Start Claude in new tab
                time.sleep(0.5)
                send_cmd = f"claude{' ' + claude_args if claude_args else ''}"
                print(f"[DEBUG] Sending to pane {pane_id}: {send_cmd}")

                result2 = subprocess.run(
                    [
                        wezterm_bin,
                        "cli",
                        "send-text",
                        "--pane-id",
                        pane_id,
                        send_cmd + "\r",  # Use \r instead of \n to ensure execution
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                print(f"[DEBUG] Send-text return code: {result2.returncode}")
                print(f"[DEBUG] Send-text stderr: {result2.stderr}")

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
        import traceback

        traceback.print_exc()
        return None


def set_tab_title(wezterm_bin, pane_id, title):
    """Set pane title"""
    try:
        # Use set-tab-title to set current tab's title
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
    """Create tab mapping file"""
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
    """Check if running in WezTerm"""
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
    # Load configuration
    from cms_start_config import load_start_config

    work_dir = Path.cwd()
    config = load_start_config(work_dir)
    claude_config = config.claude_config

    # Get instances that need to be auto-started
    autostart_instances = [inst for inst in claude_config.instances if inst.autostart]

    if not autostart_instances:
        print("[!] No instances configured for autostart")
        print("[!] Please set autostart: true in cms.config")
        return 1

    instance_ids = [inst.id for inst in autostart_instances]
    print(f"[*] Loaded {len(instance_ids)} instances from config:")
    for inst in autostart_instances:
        print(f"    - {inst.id}: {inst.role}")
    print()

    # Read Claude parameters from config
    flags = config.data.get("flags", {})
    claude_args_list = flags.get("claudeArgs", [])
    claude_args = " ".join(claude_args_list) if claude_args_list else ""

    if claude_args:
        print(f"[*] Claude args: {claude_args}")
    print(f"[*] Will create {len(instance_ids)} tabs (from instances with autostart: true)")
    print()

    # Create instance mapping
    all_instances = {inst.id: inst for inst in autostart_instances}

    wezterm_bin = _find_wezterm_bin()
    if not wezterm_bin:
        print("[!] WezTerm not found")
        return 1

    print(f"[+] WezTerm: {wezterm_bin}")
    print()

    # Check if running in WezTerm
    in_wezterm = is_in_wezterm()

    if not in_wezterm:
        print("=" * 60)
        print("  WARNING: Please run this script in WezTerm terminal")
        print("=" * 60)
        print()
        print(
            "This script needs to run in WezTerm terminal environment to work properly."
        )
        print()
        print("Steps:")
        print("  1. Open WezTerm terminal")
        print(f"  2. Change to project directory: cd {work_dir}")
        print("  3. Run: python run.py")
        print()
        print("=" * 60)
        return 1
        print()
        print("[*] Starting WezTerm...")

        try:
            # Use wezterm start to launch first tab with command
            first_instance = instance_ids[0]
            spec = all_instances[first_instance]

            # Build startup command
            claude_cmd = f"claude{' ' + claude_args if claude_args else ''}"

            # Start WezTerm (simple method)
            result = subprocess.Popen(
                [
                    wezterm_bin,
                    "start",
                    "--cwd",
                    str(work_dir),
                ],
            )

            print(f"[+] WezTerm window started")
            print("[*] Waiting for WezTerm to initialize...")
            time.sleep(3)  # Wait for WezTerm to fully start and prepare CLI

            # Verify if CLI is available
            max_retries = 10
            cli_ready = False
            for retry in range(max_retries):
                try:
                    test_result = subprocess.run(
                        [wezterm_bin, "cli", "list"],
                        capture_output=True,
                        timeout=2,
                    )
                    if test_result.returncode == 0 and test_result.stdout.strip():
                        cli_ready = True
                        print("[+] WezTerm CLI ready")
                        break
                except:
                    pass
                if retry < max_retries - 1:
                    print(
                        f"[*] Waiting for CLI to be ready... ({retry+1}/{max_retries})"
                    )
                    time.sleep(1)

            if not cli_ready:
                print("[!] WezTerm CLI not ready, cannot continue")
                print("[!] Hint: Please ensure you run this script in WezTerm terminal")
                return 1

            # Get first pane's pane_id
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

            # Set up first tab and start Claude
            if first_pane_id:
                # Start Claude in first pane
                claude_cmd = f"claude{' ' + claude_args if claude_args else ''}"
                subprocess.run(
                    [
                        wezterm_bin,
                        "cli",
                        "send-text",
                        "--pane-id",
                        first_pane_id,
                        claude_cmd + "\r",
                    ],
                    capture_output=True,
                    timeout=5,
                )

                set_tab_title(
                    wezterm_bin, first_pane_id, f"{first_instance} - {spec.role}"
                )
                instance_tabs[first_instance] = {
                    "pane_id": first_pane_id,
                    "role": spec.role,
                }
                print(
                    f"[+] First tab configured: {first_instance} (pane {first_pane_id})"
                )
                time.sleep(1)

            # Create tabs for remaining instances
            for i, inst_id in enumerate(instance_ids[1:], 1):
                spec = all_instances[inst_id]
                print(
                    f"[*] Creating tab {i+1}/{len(instance_ids)}: {inst_id} - {spec.role}"
                )

                pane_id = spawn_new_tab(wezterm_bin, work_dir, inst_id, claude_args)
                if pane_id:
                    set_tab_title(wezterm_bin, pane_id, f"{inst_id} - {spec.role}")
                    instance_tabs[inst_id] = {
                        "pane_id": pane_id,
                        "role": spec.role,
                    }
                    time.sleep(1)
                else:
                    print(f"[!] Failed to create tab for {inst_id}")

            # Save mapping
            if instance_tabs:
                create_tab_mapping(work_dir, instance_tabs)

                print()
                print("=" * 60)
                print("[SUCCESS] All tabs created!")
                print("=" * 60)
                print()
                print("Use send command to communicate:")
                print()
                for inst_id in instance_ids:
                    print(f'  python send {inst_id} "your message"')
                print()
                return 0
            else:
                print("[!] No tabs were successfully created")
                return 1

        except Exception as e:
            print(f"[!] Error: {e}")
            import traceback

            traceback.print_exc()
            return 1

    else:
        # Running in WezTerm
        print("=" * 60)
        print("  Startup mode: Create tabs in current WezTerm window")
        print("=" * 60)
        print()
        print("Will do the following:")
        print(f"  1. Use current tab for first instance ({instance_ids[0]})")
        print(f"  2. Create {len(instance_ids)-1} new tab(s) for remaining instances")
        print("  3. Start Claude in each tab")
        print("  4. Set tab titles to instance names")
        print()
        print("  Hint: Use Ctrl+Tab or Ctrl+Shift+Tab to switch between tabs")
        print()
        print("=" * 60)
        print()
        print("[*] Starting setup...")
        print()

        # Get current pane ID
        current_pane_id = os.environ.get("WEZTERM_PANE")
        if not current_pane_id:
            # Try to get via wezterm cli list
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

        # First instance in current pane
        first_instance = instance_ids[0]
        spec = all_instances[first_instance]

        print(f"[*] Pane 1 (current): {first_instance} - {spec.role}")
        print(f"[DEBUG] Current pane ID: {current_pane_id}")

        # Start Claude in current pane
        print(f"[*] Starting Claude in current pane...")
        claude_cmd = f"claude{' ' + claude_args if claude_args else ''}"
        if current_pane_id:
            subprocess.run(
                [
                    wezterm_bin,
                    "cli",
                    "send-text",
                    "--pane-id",
                    current_pane_id,
                    claude_cmd + "\r",
                ],
                capture_output=True,
                timeout=5,
            )
            time.sleep(1)  # Wait for Claude to start

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

        # Create new panes for other instances
        for i, inst_id in enumerate(instance_ids[1:], 1):
            spec = all_instances[inst_id]
            print(f"[*] Creating tab {i+1} for {inst_id} ({spec.role})...")

            pane_id = spawn_new_tab(wezterm_bin, work_dir, inst_id, claude_args)

            if pane_id:
                print(f"[+] Created tab {i+1}: {inst_id}")
                set_tab_title(wezterm_bin, pane_id, f"{inst_id} - {spec.role}")
                instance_tabs[inst_id] = {"pane_id": pane_id, "role": spec.role}
                time.sleep(0.5)
            else:
                print(f"[!] Failed to create tab {i+1}")

        print()

        # Save mapping
        create_tab_mapping(work_dir, instance_tabs)

        print()
        print("=" * 60)
        print("[SUCCESS] Setup complete!")
        print("=" * 60)
        print()
        print("Use send command to communicate:")
        print()
        for inst_id in instance_ids:
            print(f'  python send {inst_id} "your message"')
        print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(130)
