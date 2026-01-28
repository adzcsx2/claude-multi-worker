# Claude Multi Starter

[中文文档](README_CN.md) | English

Multi-instance Claude CLI launcher and communication tool. Run multiple independent Claude instances simultaneously in WezTerm for AI assistant collaboration.

## 📋 Prerequisites

Before using this tool, ensure you have:

1. **Python 3.10+** - Check version: `python --version`
2. **WezTerm** - Check if installed: `wezterm --version`
   - If not installed, visit: https://wezterm.org/index.html
3. **Claude CLI** - Check if installed: `claude --version`

## ✨ Core Features

- 🚀 **Multi-Instance Launch** - Start multiple Claude instances in WezTerm tabs with one command
- 💬 **Instance Communication** - Send messages between instances using the `send` command
- ⚡️ **Flexible Configuration** - Customize instance count and roles via `cms.config`
- 📍 **Auto Mapping** - Automatically save instance-to-tab mappings

## 🚀 Quick Start

### 1. Configure Instances

Edit `cms.config` to define your instances:

```json
{
  "providers": ["claude"],
  "flags": {
    "auto": true,
    "claudeArgs": ["--dangerously-skip-permissions"]
  },
  "claude": {
    "enabled": true,
    "instances": [
      { "id": "default", "role": "general coordinator", "autostart": true },
      { "id": "ui", "role": "UI/UX designer", "autostart": true },
      { "id": "coder", "role": "developer", "autostart": true },
      { "id": "test", "role": "QA engineer", "autostart": true }
    ]
  }
}
```

### 2. Launch Instances

**Run in WezTerm terminal:**

```bash
python run.py
```

The script will automatically:

- Read configuration from `cms.config`
- Launch all instances with `autostart: true`
- Create multiple WezTerm tabs
- Start a Claude instance in each tab
- Save mappings to `.cms_config/tab_mapping.json`

### 3. Send Messages Between Instances

```bash
python send default "Assign tasks to other instances"
python send ui "Design the login page"
python send coder "Implement user authentication"
python send test "Test the login flow"
```

## 💡 Usage Example

### Typical Workflow

```bash
# 1. Assign tasks from default instance
python send ui "Design a modern dashboard interface"
python send coder "Implement data visualization components"
python send test "Write unit tests"

# 2. UI design complete, notify developer
python send coder "UI design complete, files in /designs directory"

# 3. Development complete, notify tester
python send test "Feature implemented, please start testing"

# 4. Testing complete, report back
python send default "All tests passed, ready for release"
```

## 📂 Project Structure

```
claude-multi-starter/
├── .cms_config/
│   ├── tab_mapping.json        # Tab mappings (auto-generated)
│   └── .claude-*-session       # Session files for each instance
├── lib/                        # Core library files
├── cms.config                  # Instance configuration
├── run.py                      # Launch script
├── send                        # Communication script
├── README.md                   # This document
└── README_CN.md                # Chinese documentation
```

## ⚙️ Configuration Options

### Instance Configuration

- `id` - Instance identifier (used in send command)
- `role` - Role description (system prompt)
- `autostart` - Whether to auto-start this instance

**Supports 1-12 instances**, recommend 3-5 for optimal collaboration.

### Custom Instances

Modify `cms.config` based on your needs:

```json
{
  "claude": {
    "instances": [
      { "id": "architect", "role": "System Architect", "autostart": true },
      { "id": "frontend", "role": "Frontend Developer", "autostart": true },
      { "id": "backend", "role": "Backend Developer", "autostart": true },
      { "id": "devops", "role": "DevOps Engineer", "autostart": true }
    ]
  }
}
```

### Mapping File

Auto-generated at `.cms_config/tab_mapping.json`:

```json
{
  "work_dir": "/path/to/project",
  "tabs": {
    "default": { "pane_id": "0", "role": "general coordinator" },
    "ui": { "pane_id": "1", "role": "UI/UX designer" },
    "coder": { "pane_id": "2", "role": "developer" },
    "test": { "pane_id": "3", "role": "QA engineer" }
  },
  "created_at": 1234567890.123
}
```

The `send` command reads pane IDs from this file to route messages to specific tabs.

## 🚨 Troubleshooting

### Launch Failure

1. Confirm running in **WezTerm** terminal
2. Check Python version >= 3.10: `python --version`
3. Verify Claude CLI is installed: `claude --version`

### Message Send Failure

1. Confirm mapping file exists: `.cms_config/tab_mapping.json`
2. Restart instances to refresh mappings
3. Check instance ID is correct (case-sensitive)

### WezTerm Detection Failure

Ensure `wezterm` is in PATH:

```bash
wezterm --version
```

### Python Version Issues

If you see syntax errors, upgrade Python:

**Windows:**

```powershell
winget install Python.Python.3.12
```

**macOS:**

```bash
brew install python@3.12
```

**Linux:**

```bash
sudo apt install python3.12  # Ubuntu/Debian
sudo dnf install python3.12  # Fedora
```

## 💡 Use Cases

- **Team Collaboration Simulation** - Assign different roles (frontend, backend, testing, etc.)
- **Task Decomposition** - Break complex projects into specialized instances
- **Code Review** - One instance writes code, another reviews
- **Learning Assistant** - One instance explains, another asks questions

## 📝 Notes

- Must run `python run.py` in WezTerm terminal
- Use `python send <instance> "message"` for communication
- Each tab contains one Claude instance with a unique pane ID
- Each instance maintains independent session files
- Mapping file is auto-generated on each launch
- Use `Ctrl+C` to exit an instance
- Supports c1-c12 shorthand: `python send c1 "message"`

## 📄 License

See [LICENSE](LICENSE) file for details.
