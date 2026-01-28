#!/usr/bin/env python3
"""
MCP Server for Claude instance communication
Provides send_message tool to send messages between Claude instances
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Any

# Get project root directory
server_dir = Path(__file__).resolve().parent
project_root = server_dir.parent.parent
send_script = project_root / "send"

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "send-tool", "version": "0.1.0"}

TOOL_DEFS = [
    {
        "name": "send_message",
        "description": "Send a message to another Claude instance and automatically execute it (press Enter). Simply provide the message parameter with any text (ASCII or non-ASCII, Chinese, emoji, etc. are all supported). The server will handle encoding automatically.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "instance": {
                    "type": "string",
                    "description": "Target instance ID (e.g., 'ui', 'coder', 'test', 'default', or c1-c12)",
                },
                "message": {
                    "type": "string",
                    "description": "Message content to send. Supports any characters including Chinese, emoji, etc.",
                },
            },
            "required": ["instance", "message"],
        },
    }
]


def _send(obj: dict[str, Any]) -> None:
    """Send JSON-RPC response to stdout"""
    sys.stdout.write(json.dumps(obj, ensure_ascii=True) + "\n")
    sys.stdout.flush()


def _rpc_result(req_id: Any, result: dict[str, Any]) -> None:
    """Send successful JSON-RPC result"""
    _send({"jsonrpc": "2.0", "id": req_id, "result": result})


def _rpc_error(req_id: Any, code: int, message: str) -> None:
    """Send JSON-RPC error"""
    _send({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


def _tool_ok(text: str) -> dict[str, Any]:
    """Format successful tool response"""
    return {"content": [{"type": "text", "text": text}]}


def _tool_error(message: str) -> dict[str, Any]:
    """Format error tool response"""
    return {"content": [{"type": "text", "text": message}], "isError": True}


def _fix_encoding(text: str) -> str:
    """
    Fix Chinese text that was UTF-8 but incorrectly decoded as GBK by Claude CLI.
    This is a Windows-specific issue where UTF-8 bytes are interpreted as GBK.
    """
    try:
        # Step 1: Encode the garbled text back to GBK bytes
        # Use 'surrogateescape' to handle the invalid surrogate characters
        gbk_bytes = text.encode("gbk", errors="surrogateescape")

        # Step 2: Decode those bytes as UTF-8 (their original encoding)
        fixed = gbk_bytes.decode("utf-8")
        return fixed
    except Exception:
        # If fix fails, return original
        return text


def _handle_send_message(args: dict[str, Any]) -> dict[str, Any]:
    """Handle send_message tool call"""
    instance = str(args.get("instance", "")).strip()
    message = str(args.get("message", "")).strip()

    if not instance or not message:
        return _tool_error("Error: Both 'instance' and 'message' are required")

    try:
        # Fix encoding: Claude CLI decodes UTF-8 as GBK on Windows
        fixed_message = _fix_encoding(message)

        # Debug: write what we received to a log file
        import os

        debug_log = Path(__file__).parent / "debug.log"
        with open(debug_log, "a", encoding="utf-8") as f:
            f.write(f"\n=== New Message ===\n")
            f.write(f"Original message repr: {repr(message)}\n")
            f.write(f"Fixed message: {repr(fixed_message)}\n")

        # Use base64 encoding to safely pass message as command-line argument
        import base64

        message_bytes = fixed_message.encode("utf-8")
        message_b64 = base64.b64encode(message_bytes).decode("ascii")

        with open(debug_log, "a", encoding="utf-8") as f:
            f.write(f"UTF-8 bytes: {message_bytes.hex()}\n")
            f.write(f"Base64 encoded: {message_b64}\n")

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"

        result = subprocess.run(
            ["python", str(send_script), instance, "--base64", message_b64],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
            env=env,
        )

        if result.returncode == 0:
            return _tool_ok(f"Message sent to {instance}: {result.stdout.strip()}")
        else:
            error_msg = result.stderr.strip() or result.stdout.strip() or "Send failed"
            return _tool_error(f"Error: {error_msg}")

    except subprocess.TimeoutExpired:
        return _tool_error("Error: Send command timed out")
    except Exception as e:
        return _tool_error(f"Error: {str(e)}")


def _handle_tool_call(name: str, args: dict[str, Any]) -> dict[str, Any]:
    """Handle tool call based on tool name"""
    if name == "send_message":
        return _handle_send_message(args)
    return _tool_error(f"Unknown tool: {name}")


def _handle_request(msg: dict[str, Any]) -> None:
    """Handle incoming JSON-RPC request"""
    method = msg.get("method")
    req_id = msg.get("id")

    if method == "initialize":
        params = msg.get("params") or {}
        proto = params.get("protocolVersion") or PROTOCOL_VERSION
        result = {
            "protocolVersion": proto,
            "capabilities": {"tools": {"list": True}},
            "serverInfo": SERVER_INFO,
        }
        _rpc_result(req_id, result)
        return

    if method == "initialized":
        return

    if method == "tools/list":
        _rpc_result(req_id, {"tools": TOOL_DEFS})
        return

    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        if not name:
            _rpc_error(req_id, -32602, "missing tool name")
            return
        result = _handle_tool_call(str(name), args)
        _rpc_result(req_id, result)
        return

    if method in ("shutdown", "exit"):
        _rpc_result(req_id, {})
        raise SystemExit(0)

    if req_id is not None:
        _rpc_error(req_id, -32601, f"unknown method: {method}")


def main() -> int:
    """Main server loop - read JSON-RPC from stdin, write to stdout"""
    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except Exception:
            continue
        if not isinstance(msg, dict):
            continue
        try:
            _handle_request(msg)
        except SystemExit:
            return 0
        except Exception:
            req_id = msg.get("id")
            if req_id is not None:
                _rpc_error(req_id, -32603, "internal error")
    return 0


if __name__ == "__main__":
    sys.exit(main())
