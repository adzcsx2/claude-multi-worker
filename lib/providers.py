from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProviderDaemonSpec:
    daemon_key: str
    protocol_prefix: str
    state_file_name: str
    log_file_name: str
    idle_timeout_env: str
    lock_name: str


@dataclass
class ProviderClientSpec:
    protocol_prefix: str
    enabled_env: str
    autostart_env_primary: str
    autostart_env_legacy: str
    state_file_env: str
    session_filename: str
    daemon_bin_name: str
    daemon_module: str


@dataclass
class ClaudeInstanceSpec:
    """Specification for a named Claude instance (e.g., 'alpha', 'beta', 'reviewer')"""
    instance_id: str
    role: str = ""
    session_filename: str = ".claude-session"
    daemon_key: str = "claude"
    protocol_prefix: str = "cms"

    @property
    def state_file_name(self) -> str:
        """Instance-specific state file"""
        if self.instance_id == "default":
            return "claude.json"
        return f"claude_{self.instance_id}.json"

    @property
    def log_file_name(self) -> str:
        """Instance-specific log file"""
        if self.instance_id == "default":
            return "claude.log"
        return f"claude_{self.instance_id}.log"

    @property
    def lock_name(self) -> str:
        """Instance-specific lock name"""
        if self.instance_id == "default":
            return "claude"
        return f"claude_{self.instance_id}"

    @property
    def idle_timeout_env(self) -> str:
        """Instance-specific idle timeout env var"""
        if self.instance_id == "default":
            return "CMS_CLAUDE_IDLE_TIMEOUT_S"
        return f"CMS_CLAUDE_{self.instance_id.upper()}_IDLE_TIMEOUT_S"

    @property
    def enabled_env(self) -> str:
        """Instance-specific enabled env var"""
        if self.instance_id == "default":
            return "CMS_CLAUDE"
        return f"CMS_CLAUDE_{self.instance_id.upper()}"

    @property
    def autostart_env_primary(self) -> str:
        """Instance-specific autostart env var"""
        if self.instance_id == "default":
            return "CMS_CLAUDE_AUTOSTART"
        return f"CMS_CLAUDE_{self.instance_id.upper()}_AUTOSTART"

    @property
    def state_file_env(self) -> str:
        """Instance-specific state file env var"""
        if self.instance_id == "default":
            return "CMS_CLAUDE_STATE_FILE"
        return f"CMS_CLAUDE_{self.instance_id.upper()}_STATE_FILE"


# Global registry of Claude instances
_CLAUDE_INSTANCES: dict[str, ClaudeInstanceSpec] = {
    "default": ClaudeInstanceSpec(
        instance_id="default",
        role="general",
        session_filename=".claude-session"
    )
}


def register_claude_instance(instance_id: str, role: str = "", session_filename: str = "") -> ClaudeInstanceSpec:
    """Register a new Claude instance dynamically"""
    if instance_id == "default":
        raise ValueError("Cannot override 'default' instance")

    spec = ClaudeInstanceSpec(
        instance_id=instance_id,
        role=role or instance_id,
        session_filename=session_filename or f".claude-{instance_id}-session"
    )
    _CLAUDE_INSTANCES[instance_id] = spec
    return spec


def get_claude_instance(instance_id: str) -> ClaudeInstanceSpec:
    """Get a Claude instance spec by ID"""
    return _CLAUDE_INSTANCES.get(instance_id or "default", _CLAUDE_INSTANCES["default"])


def list_claude_instances() -> list[str]:
    """List all registered Claude instance IDs"""
    return list(_CLAUDE_INSTANCES.keys())


def is_claude_instance(instance_id: str) -> bool:
    """Check if an instance ID is a registered Claude instance"""
    return instance_id in _CLAUDE_INSTANCES


# Auto-load Claude instances from config files
def _auto_load_claude_instances():
    """Automatically load Claude instances from config files"""
    try:
        import json
        from pathlib import Path

        config_paths = [
            Path.cwd() / ".cms_config" / "cms.config",
            Path.home() / ".cms" / "cms.config"
        ]

        for config_path in config_paths:
            if not config_path.exists():
                continue

            try:
                content = config_path.read_text(encoding="utf-8-sig")
                if not content.strip():
                    continue
                data = json.loads(content)
            except Exception:
                continue

            if not isinstance(data, dict):
                continue

            claude_config = data.get("claude", {})
            if isinstance(claude_config, bool):
                continue
            if not isinstance(claude_config, dict):
                continue

            instances = claude_config.get("instances", [])
            if not isinstance(instances, list):
                continue

            for inst in instances:
                if isinstance(inst, dict):
                    inst_id = inst.get("id", "")
                    if not inst_id or inst_id == "default":
                        continue
                    if inst_id not in _CLAUDE_INSTANCES:
                        role = inst.get("role", "")
                        session_file = inst.get("session_file", "")
                        register_claude_instance(inst_id, role, session_file)
                elif isinstance(inst, str):
                    if inst and inst != "default" and inst not in _CLAUDE_INSTANCES:
                        register_claude_instance(inst)

            # Only load from first successful config file
            break
    except Exception:
        pass  # Silently ignore errors during auto-load


# Auto-load instances when module is imported
_auto_load_claude_instances()
