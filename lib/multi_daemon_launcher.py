"""
CMS Multi-Daemon Multi-Pane Patch

Adds support for launching multiple Claude instances simultaneously
with adaptive grid layout.

Usage:
    cms claude                          # Auto-launch all configured instances
    cms claude ui,coder,test            # Launch specific instances
    cms claude:ui,coder                 # Alternative syntax

Compatible with:
- tmux
- WezTerm
"""

import sys
import os
import re
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

# Add lib to path
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir / "lib"))

from cms_start_config import load_start_config, ClaudeInstanceConfig
from providers import get_claude_instance, list_claude_instances
from multi_instance_layout import calculate_grid_layout, get_pane_direction, get_pane_percent


@dataclass
class ClaudeInstanceLaunch:
    """Specification for launching a Claude instance"""
    instance_id: str
    role: str
    title: str
    env_overrides: dict


def parse_claude_instances(providers: List[str], config_path: Optional[Path] = None) -> Tuple[List[str], List[str]]:
    """
    Parse provider list to extract Claude instances.

    Supports syntax:
    - claude                    -> All configured instances
    - claude:ui,coder,test       -> Specific instances
    - claude ui coder            -> Alternative syntax

    Returns:
        (other_providers, claude_instances)
        other_providers: List of non-claude providers (codex, gemini, etc.)
        claude_instances: List of Claude instance IDs to launch
    """
    other_providers = []
    claude_instances = []

    # Load config to get Claude instances
    work_dir = Path.cwd()
    config = load_start_config(work_dir)
    claude_config = config.claude_config

    # Get all configured Claude instances
    all_instances = [inst.id for inst in claude_config.instances]

    for provider in providers:
        provider_lower = provider.lower().strip()

        # Check for claude:instance1,instance2 syntax
        if ":" in provider_lower and provider_lower.startswith("claude:"):
            # Extract instances
            parts = provider_lower.split(":", 1)
            instances_spec = parts[1].strip()
            if instances_spec:
                # Parse comma-separated instances
                specified = [inst.strip() for inst in instances_spec.split(",") if inst.strip()]

                # Validate instances exist
                for inst_id in specified:
                    if inst_id in all_instances:
                        claude_instances.append(inst_id)
                    else:
                        print(f"WARNING: Claude instance '{inst_id}' not found in config", file=sys.stderr)

        # Check for standalone "claude"
        elif provider_lower == "claude":
            # Add all configured instances
            claude_instances.extend(all_instances)

        # Other providers
        elif provider_lower in {"codex", "gemini", "opencode", "droid"}:
            other_providers.append(provider_lower)

    # Remove duplicates while preserving order
    seen = set()
    unique_instances = []
    for inst in claude_instances:
        if inst not in seen:
            seen.add(inst)
            unique_instances.append(inst)

    return other_providers, unique_instances


def create_instance_launch_specs(instance_ids: List[str]) -> List[ClaudeInstanceLaunch]:
    """
    Create launch specifications for Claude instances.

    Args:
        instance_ids: List of instance IDs to launch

    Returns:
        List of ClaudeInstanceLaunch objects
    """
    launches = []

    for instance_id in instance_ids:
        spec = get_claude_instance(instance_id)

        # Create title
        if instance_id == "default":
            title = f"CMS-Claude"
        else:
            title = f"CMS-Claude-{instance_id.capitalize()}"

        # Environment overrides
        env_overrides = {
            "CMS_CLAUDE_INSTANCE": instance_id,
        }

        launch = ClaudeInstanceLaunch(
            instance_id=instance_id,
            role=spec.role,
            title=title,
            env_overrides=env_overrides
        )
        launches.append(launch)

    return launches


def format_launch_summary(launches: List[ClaudeInstanceLaunch], grid_layout) -> str:
    """Format a summary of instances to be launched"""
    lines = []
    lines.append(f"📊 Layout: {grid_layout}")
    lines.append("🤖 Claude instances:")
    for launch in launches:
        role_display = f" ({launch.role})" if launch.role else ""
        lines.append(f"   - {launch.instance_id}{role_display}")
    return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    # Test parsing
    test_cases = [
        (["claude"], "All instances"),
        (["claude:ui,coder,test"], "Specific instances"),
        (["codex", "claude:ui,coder"], "Mixed providers"),
    ]

    for providers, description in test_cases:
        print(f"\nTest: {description}")
        print(f"Input: {providers}")

        other, instances = parse_claude_instances(providers)
        print(f"Other providers: {other}")
        print(f"Claude instances: {instances}")

        if instances:
            launches = create_instance_launch_specs(instances)
            grid = calculate_grid_layout(len(instances))
            print(format_launch_summary(launches, grid))
