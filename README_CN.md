# Claude Multi Starter

中文文档 | [English](README.md)

多实例 Claude CLI 启动和通信工具。在 WezTerm 中同时运行多个独立的 Claude 实例，实现 AI 助手协同工作。

## ✨ 核心功能

- 🚀 **多实例启动** - 一键在 WezTerm 标签页中启动多个 Claude 实例
- 💬 **实例通信** - 使用 `send` 命令在实例间发送消息
- ⚡️ **灵活配置** - 通过 `cms.config` 自定义实例数量和角色
- 📍 **自动映射** - 自动保存实例到标签页的映射关系

## 📋 环境要求

- **Python 3.10+**（需要现代类型提示支持）
- **WezTerm** - 终端复用器（安装说明见下文）
- **Claude CLI** - Anthropic 官方命令行工具

### 安装 WezTerm

**Windows:**
```powershell
# 使用 winget
winget install wez.wezterm

# 或从官网下载安装包：
# https://wezfurlong.org/wezterm/installation.html
```

**macOS:**
```bash
# 使用 Homebrew
brew install --cask wezterm

# 或从官网下载：
# https://wezfurlong.org/wezterm/installation.html
```

**Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list
sudo apt update
sudo apt install wezterm

# Fedora/RHEL
sudo dnf copr enable wezfurlong/wezterm
sudo dnf install wezterm

# Arch Linux
yay -S wezterm
```

验证安装：
```bash
wezterm --version
```

## 🚀 快速开始

### 1. 配置实例

编辑 `cms.config` 定义你需要的实例：

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

### 2. 启动实例

在 **WezTerm 终端**中运行：

```bash
python RUN.py
```

脚本会自动：

- 从 `cms.config` 读取配置
- 启动所有 `autostart: true` 的实例
- 在 WezTerm 中创建多个标签页
- 每个标签页启动一个 Claude 实例
- 保存映射关系到 `.cms_config/tab_mapping.json`

### 3. 实例间通信

**Windows:**
```cmd
python send default "分配任务给其他实例"
python send ui "设计登录页面"
python send coder "实现用户认证功能"
python send test "测试登录流程"
```

**macOS/Linux:**
```bash
python send default "分配任务给其他实例"
python send ui "设计登录页面"
python send coder "实现用户认证功能"
python send test "测试登录流程"
```

## 💡 使用示例

### 典型工作流

```bash
# 1. 在 default 实例分配任务
bin\send ui "设计一个现代化的仪表板界面"
bin\send coder "实现数据可视化组件"
bin\send test "编写单元测试"

# 2. UI 设计完成后通知开发
bin\send coder "UI 设计已完成，文件在 /designs 目录"

# 3. 开发完成后通知测试
bin\send test "功能已实现，请开始测试"

# 4. 测试完成后汇报
bin\send default "所有测试通过，可以发布"
```

## 📂 项目结构

```
claude-multi-starter/
├── .cms_config/
│   ├── tab_mapping.json        # 标签页映射（自动生成）
│   └── .claude-*-session       # 各实例会话文件
├── lib/                        # 核心库文件
├── cms.config                  # 实例配置文件
├── RUN.py                      # 启动脚本
├── send                        # 通信脚本（Linux/Mac）
├── send.cmd                    # 通信脚本（Windows）
├── README.md                   # 英文文档
└── README_CN.md                # 中文文档
```

## ⚙️ 配置说明

### 实例配置选项

- `id` - 实例标识符（用于 send 命令）
- `role` - 角色描述（提示词）
- `autostart` - 是否自动启动

**支持 1-12 个实例**，推荐 3-5 个以获得最佳协作效果。

### 自定义实例

根据需求修改 `cms.config`：

```json
{
  "claude": {
    "instances": [
      { "id": "architect", "role": "系统架构师", "autostart": true },
      { "id": "frontend", "role": "前端开发", "autostart": true },
      { "id": "backend", "role": "后端开发", "autostart": true },
      { "id": "devops", "role": "运维工程师", "autostart": true }
    ]
  }
}
```

### 映射文件

启动后自动生成 `.cms_config/tab_mapping.json`：

```json
{
  "tabs": {
    "default": { "pane_id": "0", "tab_id": "0" },
    "ui": { "pane_id": "1", "tab_id": "1" },
    "coder": { "pane_id": "2", "tab_id": "2" },
    "test": { "pane_id": "3", "tab_id": "3" }
  }
}
```

`send` 命令自动读取此文件进行消息路由。

## 🚨 故障排除

### 启动失败

1. 确认在 **WezTerm** 终端中运行
2. 检查 Python 版本 >= 3.10：`python --version`
3. 确认 Claude CLI 已安装：`claude --version`

### 消息发送失败

1. 确认映射文件存在：`.cms_config/tab_mapping.json`
2. 重新启动实例刷新映射
3. 检查实例 ID 是否正确（区分大小写）

### WezTerm 检测失败

确保 `wezterm` 在 PATH 中：

```bash
wezterm --version
```

### Python 版本问题

如果遇到语法错误，请升级 Python：

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

## 💡 使用场景

- **团队协作模拟** - 分配不同角色（前端、后端、测试等）
- **任务分解** - 将复杂项目拆分给专门的实例
- **代码审查** - 一个实例写代码，另一个审查
- **学习辅助** - 一个实例讲解，另一个提问

## 📝 注意事项

- 必须在 WezTerm 终端中运行
- 每个实例维护独立的会话文件
- 映射文件会在每次启动时更新
- 使用 `Ctrl+C` 可以退出某个实例

## 📄 许可证

详见 [LICENSE](LICENSE) 文件。
