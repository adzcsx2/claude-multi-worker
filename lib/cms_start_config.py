from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Optional, Tuple


CONFIG_FILENAME = "cms.config"
DEFAULT_PROVIDERS = ["codex", "gemini", "opencode", "claude"]


@dataclass
class ClaudeInstanceConfig:
    """Claude instance configuration from cms.config"""
    id: str
    role: str = ""
    autostart: bool = True
    session_file: str = ""


@dataclass
class ClaudeConfig:
    """Claude provider configuration"""
    enabled: bool = True
    instances: list[ClaudeInstanceConfig] = None

    def __post_init__(self):
        if self.instances is None:
            self.instances = [ClaudeInstanceConfig(id="default")]


@dataclass
class StartConfig:
    data: dict
    path: Optional[Path] = None
    claude_config: ClaudeConfig = None

    def __post_init__(self):
        if self.claude_config is None:
            self.claude_config = _parse_claude_config(self.data)


_ALLOWED_PROVIDERS = {"codex", "gemini", "opencode", "claude", "droid"}


def _parse_claude_config(obj: dict) -> ClaudeConfig:
    """Parse Claude-specific configuration from config object"""
    claude_obj = obj.get("claude", {})

    if isinstance(claude_obj, bool):
        return ClaudeConfig(enabled=claude_obj)

    if isinstance(claude_obj, dict):
        enabled = claude_obj.get("enabled", True)
        instances_raw = claude_obj.get("instances", [])
        instances = []

        for inst_raw in instances_raw:
            if isinstance(inst_raw, str):
                instances.append(ClaudeInstanceConfig(id=inst_raw))
            elif isinstance(inst_raw, dict):
                instances.append(ClaudeInstanceConfig(
                    id=inst_raw.get("id", "default"),
                    role=inst_raw.get("role", ""),
                    autostart=inst_raw.get("autostart", True),
                    session_file=inst_raw.get("session_file", "")
                ))

        if not instances:
            instances = [ClaudeInstanceConfig(id="default")]

        return ClaudeConfig(enabled=enabled, instances=instances)

    return ClaudeConfig()


def _parse_tokens(raw: str) -> list[str]:
    if not raw:
        return []
    lines: list[str] = []
    for line in raw.splitlines():
        stripped = line
        if "//" in stripped:
            stripped = stripped.split("//", 1)[0]
        if "#" in stripped:
            stripped = stripped.split("#", 1)[0]
        lines.append(stripped)
    cleaned = " ".join(lines)
    cleaned = re.sub(r"[\[\]\{\}\"']", " ", cleaned)
    parts = re.split(r"[,\s]+", cleaned)
    return [p for p in (part.strip() for part in parts) if p]


def _parse_claude_instances_token(token: str) -> tuple[bool, list[ClaudeInstanceConfig]]:
    """
    Parse claude instance syntax like: claude:alpha,beta:reviewer,gamma
    Returns (is_claude_token, list_of_instance_configs)
    """
    if ":" not in token:
        return False, []

    provider, instances_part = token.split(":", 1)
    if provider.lower() != "claude":
        return False, []

    instances: list[ClaudeInstanceConfig] = []
    for part in instances_part.split(","):
        part = part.strip()
        if not part:
            continue

        if ":" in part:
            # Format: instance_id:role
            inst_id, role = part.split(":", 1)
            instances.append(ClaudeInstanceConfig(id=inst_id.strip(), role=role.strip()))
        else:
            # Format: instance_id only
            instances.append(ClaudeInstanceConfig(id=part))

    return True, instances


def _normalize_providers(tokens: list[str]) -> tuple[list[str], bool, list[ClaudeInstanceConfig]]:
    providers: list[str] = []
    seen: set[str] = set()
    cmd_enabled = False
    claude_instances: list[ClaudeInstanceConfig] = []

    for raw in tokens:
        token = str(raw).strip()

        # Check for claude instance syntax (e.g., claude:alpha,beta:reviewer)
        is_claude, instances = _parse_claude_instances_token(token)
        if is_claude:
            if "claude" not in seen:
                seen.add("claude")
                providers.append("claude")
            claude_instances.extend(instances)
            continue

        token = token.lower()
        if not token:
            continue
        if token == "cmd":
            cmd_enabled = True
            continue
        if token not in _ALLOWED_PROVIDERS:
            continue
        if token in seen:
            continue
        seen.add(token)
        providers.append(token)

    return providers, cmd_enabled, claude_instances


def _parse_config_obj(obj: object) -> dict:
    if isinstance(obj, dict):
        data = dict(obj)
        raw_providers = data.get("providers")
        tokens: list[str] = []
        if isinstance(raw_providers, str):
            tokens = _parse_tokens(raw_providers)
        elif isinstance(raw_providers, list):
            tokens = [str(p) for p in raw_providers if p is not None]
        elif raw_providers is not None:
            tokens = [str(raw_providers)]

        if tokens:
            providers, cmd_enabled, claude_instances = _normalize_providers(tokens)
            data["providers"] = providers
            if cmd_enabled and "cmd" not in data:
                data["cmd"] = True
            if claude_instances:
                if "claude" not in data:
                    data["claude"] = {}
                if isinstance(data["claude"], dict):
                    existing_instances = data["claude"].get("instances", [])
                    if not existing_instances:
                        data["claude"]["instances"] = [i.__dict__ for i in claude_instances]
        return data

    if isinstance(obj, list):
        tokens = [str(p) for p in obj if p is not None]
        providers, cmd_enabled, claude_instances = _normalize_providers(tokens)
        data: dict = {"providers": providers}
        if cmd_enabled:
            data["cmd"] = True
        if claude_instances:
            data["claude"] = {"instances": [i.__dict__ for i in claude_instances]}
        return data

    if isinstance(obj, str):
        tokens = _parse_tokens(obj)
        providers, cmd_enabled, claude_instances = _normalize_providers(tokens)
        data = {"providers": providers}
        if cmd_enabled:
            data["cmd"] = True
        if claude_instances:
            data["claude"] = {"instances": [i.__dict__ for i in claude_instances]}
        return data

    return {}


def _read_config(path: Path) -> dict:
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except Exception:
        return {}
    if not raw.strip():
        return {}
    try:
        obj = json.loads(raw)
    except Exception:
        obj = None
    if obj is None:
        tokens = _parse_tokens(raw)
        providers, cmd_enabled, claude_instances = _normalize_providers(tokens)
        data: dict = {"providers": providers}
        if cmd_enabled:
            data["cmd"] = True
        if claude_instances:
            data["claude"] = {"instances": [i.__dict__ for i in claude_instances]}
        return data
    return _parse_config_obj(obj)


def _config_paths(work_dir: Path) -> Tuple[Path, Path]:
    project = Path(work_dir) / ".cms_config" / CONFIG_FILENAME
    global_path = Path.home() / ".cms" / CONFIG_FILENAME
    return project, global_path


def load_start_config(work_dir: Path) -> StartConfig:
    project, global_path = _config_paths(work_dir)
    if project.exists():
        return StartConfig(data=_read_config(project), path=project)
    if global_path.exists():
        return StartConfig(data=_read_config(global_path), path=global_path)
    return StartConfig(data={}, path=None)


def ensure_default_start_config(work_dir: Path) -> Tuple[Optional[Path], bool]:
    project, _global_path = _config_paths(work_dir)
    if project.exists():
        return project, False
    try:
        project.parent.mkdir(parents=True, exist_ok=True)
        payload = ",".join(DEFAULT_PROVIDERS) + "\n"
        project.write_text(payload, encoding="utf-8")
        return project, True
    except Exception:
        return None, False
