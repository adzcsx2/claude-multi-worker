#!/usr/bin/env python3
"""
WezTerm detector for CMS startup scripts

This module provides reliable WezTerm detection without relying on wezterm cli.
"""
import os
import sys
from pathlib import Path

def is_wezterm() -> bool:
    """
    Detect if running inside WezTerm using multiple methods.

    Returns:
        True if running in WezTerm, False otherwise
    """
    # Method 1: Check for WezTerm-specific env vars
    # WezTerm sets these environment variables
    wezterm_env_vars = [
        "WEZTERM_EXECUTABLE",
        "WEZTERM_VERSION",
        "WEZTERM_PANE",
    ]

    for var in wezterm_env_vars:
        if os.environ.get(var):
            return True

    # Method 2: Check parent process name (Windows)
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            psapi = ctypes.WinDLL('psapi', use_last_error=True)

            # Get current process ID
            pid = os.getpid()

            # Get parent process ID
            h_process = kernel32.OpenProcess(0x0410, False, pid)
            if not h_process:
                return False

            ppid = ctypes.c_ulong()
            if not kernel32.GetParentProcessId(h_process, ctypes.byref(ppid)):
                kernel32.CloseHandle(h_process)
                return False

            kernel32.CloseHandle(h_process)

            # Get parent process name
            parent_pid = ppid.value
            h_parent = kernel32.OpenProcess(0x0410, False, parent_pid)
            if not h_parent:
                return False

            name_buf = (wintypes.WCHAR * 1024)()
            if psapi.GetModuleBaseNameW(h_parent, 0, name_buf, 1024):
                parent_name = name_buf.value.lower()
                kernel32.CloseHandle(h_parent)
                return "wezterm" in parent_name or "wezterm-gui" in parent_name

            kernel32.CloseHandle(h_parent)
        except Exception:
            pass

    # Method 3: Check TERM variable (Unix-like)
    term = os.environ.get("TERM", "")
    if "wezterm" in term.lower():
        return True

    # Method 4: Try wezterm cli commands as last resort
    try:
        import subprocess
        # Try different commands
        for cmd in [["wezterm", "cli", "list"], ["wezterm", "cli", "list-clients"]]:
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=2)
                if result.returncode == 0:
                    return True
            except Exception:
                continue
    except Exception:
        pass

    return False


def get_wezterm_version() -> str | None:
    """Get WezTerm version if available"""
    try:
        import subprocess
        result = subprocess.run(
            ["wezterm", "--version"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def main():
    """Test WezTerm detection"""
    print("WezTerm Detection Test")
    print("=" * 50)

    if is_wezterm():
        print("[OK] Running inside WezTerm")
        version = get_wezterm_version()
        if version:
            print(f"     Version: {version}")
        return 0
    else:
        print("[FAIL] Not running in WezTerm")
        print("\nDetection details:")
        print(f"  WEZTERM_EXECUTABLE: {os.environ.get('WEZTERM_EXECUTABLE', 'not set')}")
        print(f"  WEZTERM_PANE: {os.environ.get('WEZTERM_PANE', 'not set')}")
        print(f"  TERM: {os.environ.get('TERM', 'not set')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
