# CMS Multi-Instance Launcher

一键启动多个 Claude Multi Starter 实例，实现多个 AI 助手的协同工作。基于 WezTerm，每个实例独立窗口，支持实例间快速消息传递。

## ✨ 特性

- 🚀 **一键启动** - 运行 `start.bat` 自动创建多个 Claude 实例
- 🪟 **独立窗口** - 每个实例独立窗口，标题显示实例名
- 💬 **快速通信** - `send` 命令实现实例间即时消息传递
- ⚙️ **动态配置** - 通过 `.cms_config/cms.config` 自定义实例数量和角色
- 🎯 **自动映射** - 启动时自动检测并保存 pane ID 映射

## 🔧 环境要求

- **Python 3.8+**
- **WezTerm** - [下载安装](https://wezfurlong.org/wezterm/installation.html)
- **CMS (Claude Multi Starter)** - Claude 命令行工具

## 📦 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd claude_code_bridge
```

### 2. 配置实例

编辑 `.cms_config/cms.config` 文件：

```json
{
  "providers": ["claude"],
  "claude": {
    "enabled": true,
    "instances": [
      {"id": "default", "role": "general coordinator", "autostart": true},
      {"id": "ui", "role": "UI/UX designer", "autostart": true},
      {"id": "coder", "role": "developer", "autostart": true},
      {"id": "test", "role": "QA engineer", "autostart": true}
    ]
  }
}
```

### 3. 启动

在 WezTerm 中运行：

```bash
start.bat
```

脚本会：
1. 为每个实例创建独立窗口
2. 设置窗口标题为实例名
3. 自动启动 CMS
4. 保存 pane 映射到 `.cms_config/pane_mapping.json`

## 📡 实例间通信

### send 命令

快速发送消息到指定实例：

```bash
send ui "设计登录页面"
send coder "实现用户认证功能"
send test "测试登录流程"
send default "汇总所有进度"
```

### 工作流示例

```bash
# 在 default 实例中协调任务
send ui "设计一个现代化的仪表板界面"
send coder "实现数据可视化组件"
send test "编写集成测试"

# UI 完成后通知 coder
send coder "UI 设计完成，请查看 designs/ 目录"

# Coder 实现后通知 test
send test "功能已实现，请开始测试"
```

## 📂 项目结构

```
claude_code_bridge/
├── .cms_config/
│   ├── cms.config           # 实例配置
│   └── pane_mapping.json    # Pane ID 映射（自动生成）
├── bin/
│   ├── send                 # 实例间消息命令
│   ├── ask                  # 异步任务命令
│   └── ...                  # 其他 CMS 命令
├── lib/                     # Python 库文件
├── skills/                  # CMS Skills
├── start-dynamic.py         # 动态启动脚本
├── start.bat                # Windows 启动入口
├── install-skills.ps1       # Skills 安装脚本（可选）
└── README.md
```

## ⚙️ 配置说明

### 实例配置

每个实例包含：

- `id` - 实例标识符（用于 send 命令）
- `role` - 角色描述
- `autostart` - 是否自动启动

支持 1-6 个实例，推荐 4-5 个。

### Pane 映射

启动时自动生成 `.cms_config/pane_mapping.json`：

```json
{
  "default": 0,
  "ui": 5,
  "coder": 8,
  "test": 12
}
```

`send` 命令优先读取此文件，确保消息发送到正确的窗口。

## 🛠️ 高级用法

### 自定义实例数量

在 `cms.config` 中添加或删除 instances 数组项：

```json
{
  "instances": [
    {"id": "architect", "role": "system architect", "autostart": true},
    {"id": "frontend", "role": "frontend dev", "autostart": true},
    {"id": "backend", "role": "backend dev", "autostart": true},
    {"id": "devops", "role": "DevOps engineer", "autostart": true}
  ]
}
```

### 调试 Pane 映射

查看映射文件：

```bash
cat .cms_config/pane_mapping.json
```

手动测试发送：

```bash
wezterm cli list
wezterm cli send-text --pane-id <PANE_ID> --no-paste "test message"
```

## 🚨 故障排除

### 实例未收到消息

1. 检查 `.cms_config/pane_mapping.json` 是否存在
2. 重新运行 `start.bat` 刷新映射
3. 确认在 WezTerm 环境中运行

### 启动失败

1. 确认 WezTerm 已安装并在 PATH 中
2. 检查 `.cms_config/cms.config` JSON 格式正确
3. 查看错误信息，确认 Python 版本 >= 3.8

### JSON 配置错误

确保 `cms.config` 中：
- 最后一个数组元素后**没有逗号**
- 所有引号匹配
- 使用 JSON 验证器检查语法

## 🔄 更新到新电脑

1. 复制项目文件夹到新电脑
2. 安装依赖（Python, WezTerm, CMS）
3. 在 WezTerm 中运行 `start.bat`

## 💡 使用场景

- **团队协作模拟** - 模拟前端、后端、测试等不同角色
- **任务分解** - 将复杂任务分配给专业化的 AI 实例
- **代码审查** - 一个实例写代码，另一个实例审查
- **学习辅助** - 一个实例讲解，另一个实例提问

## 📄 许可证

详见 [LICENSE](LICENSE) 文件。
