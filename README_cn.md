# CMS - Claude Multi Starter

[English](README.md)

> 多实例 Claude Code CLI 启动器，实现多个 AI 助手无缝协作。

## 特性

- **一键启动** - 单条命令自动创建多个 Claude 实例
- **独立窗口** - 每个实例在独立的终端窗口中运行，标题清晰标识
- **实例间通信** - 使用 `send` 命令在实例间即时发送消息
- **动态配置** - 通过 `.cms_config/cms.config` 自定义实例数量和角色
- **自动映射** - 启动时自动检测并保存窗格 ID 映射
- **基于角色的会话** - 每个实例维护独立的会话文件，上下文隔离

## 环境要求

- **Python 3.8+**
- **WezTerm** - [下载安装](https://wezfurlong.org/wezterm/installation.html)
- **Claude Code CLI** - Anthropic 官方命令行工具

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/claude-multi-starter.git
cd claude-multi-starter
```

### 2. 配置实例

编辑 `.cms_config/cms.config` 定义实例：

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
      {"id": "default", "role": "总体协调", "autostart": true},
      {"id": "ui", "role": "UI/UX 设计师", "autostart": true},
      {"id": "coder", "role": "开发工程师", "autostart": true},
      {"id": "test", "role": "测试工程师", "autostart": true}
    ]
  }
}
```

### 3. 启动实例

运行启动脚本：

```bash
./start-cms.sh
# 或在 Windows 上
start-dynamic.py
```

脚本将：
1. 为每个实例创建独立窗口
2. 设置窗口标题为实例名称
3. 在每个窗口中自动启动 CMS
4. 保存窗格映射到 `.cms_config/pane_mapping.json`

## 使用方法

### 实例间发送消息

使用 `send` 命令与其他实例通信：

```bash
# 向 UI 设计师实例发送任务
send ui "设计一个现代化的仪表板界面"

# 向开发者发送实现请求
send coder "实现用户认证功能"

# 请求测试
send test "测试登录流程"

# 从 default 实例协调
send default "汇总所有进度"
```

### 典型工作流

```bash
# 在 default 实例中协调任务
send ui "设计一个数据可视化组件"
send coder "使用 React 实现该组件"
send test "为组件编写集成测试"

# UI 设计完成后通知 coder
send coder "UI 设计完成，请查看 designs/ 目录"

# 实现完成后通知测试
send test "功能已实现，请开始测试"
```

## 项目结构

```
claude-multi-starter/
├── .cms_config/
│   ├── cms.config           # 实例配置
│   ├── pane_mapping.json    # 窗格 ID 映射（自动生成）
│   └── .claude-*-session    # 各实例会话文件
├── bin/
│   ├── send                 # 实例间消息命令
│   ├── ask                  # 异步任务命令
│   └── ...                  # 其他 CMS 工具
├── lib/                     # Python 库文件
├── skills/                  # CMS 技能
├── start-cms.sh             # Unix 启动脚本
├── start-dynamic.py         # Python 启动脚本
├── install.sh               # 安装脚本
└── README.md
```

## 配置说明

### 实例配置

`cms.config` 中每个实例包含：

- `id` - 实例标识符（用于 `send` 命令）
- `role` - 实例的角色描述
- `autostart` - 是否自动启动该实例
- `session_file`（可选）- 自定义会话文件名

支持 1-6 个实例，建议 4-5 个以获得最佳性能。

### 窗格映射

启动时自动生成 `.cms_config/pane_mapping.json`：

```json
{
  "default": 0,
  "ui": 5,
  "coder": 8,
  "test": 12
}
```

`send` 命令读取此文件以确保消息路由到正确的窗口。

## 高级用法

### 自定义实例

在 `cms.config` 中添加或删除实例：

```json
{
  "instances": [
    {"id": "architect", "role": "系统架构师", "autostart": true},
    {"id": "frontend", "role": "前端开发", "autostart": true},
    {"id": "backend", "role": "后端开发", "autostart": true},
    {"id": "devops", "role": "运维工程师", "autostart": true}
  ]
}
```

### 调试窗格映射

查看映射文件：

```bash
cat .cms_config/pane_mapping.json
```

手动测试消息发送：

```bash
wezterm cli list
wezterm cli send-text --pane-id <PANE_ID> --no-paste "测试消息"
```

### 启动特定实例

```bash
# 启动所有配置的实例
cms claude

# 启动特定实例
cms claude:ui,coder,test
```

## 架构说明

CMS 使用多守护进程架构，每个 Claude 实例：
- 运行独立的守护进程（`laskd`）
- 维护独立的会话文件
- 拥有隔离的状态和上下文
- 通过 WezTerm CLI 进行通信

## 使用场景

- **团队模拟** - 同时模拟前端、后端、测试等角色
- **任务分解** - 将复杂任务分配给专业化的 AI 实例
- **代码审查** - 一个实例编写代码，另一个实例审查
- **学习辅助** - 一个实例讲解概念，另一个实例提问
- **并行开发** - 使用专用实例同时处理多个功能

## 故障排除

### 实例未收到消息

1. 检查 `.cms_config/pane_mapping.json` 是否存在
2. 重新运行 `start-cms.sh` 刷新映射
3. 确认在 WezTerm 环境中运行

### 启动失败

1. 确保已安装 WezTerm 并在 PATH 中
2. 验证 `.cms_config/cms.config` JSON 格式正确
3. 查看错误信息，确认 Python 版本 >= 3.8

### JSON 配置错误

确保 `cms.config` 中：
- 最后一个数组元素后没有逗号
- 所有引号正确匹配
- 使用 JSON 验证器检查语法

## 版本历史

- **v5.2.0** - 简化为仅支持 Claude 的多实例架构
- **v5.1.0** - 添加 WezTerm 多实例支持和 `send` 命令
- 早期版本支持多个 AI 提供商（Codex、Gemini 等）

## 许可证

详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎贡献！请随时提交问题或拉取请求。

## 致谢

基于 Anthropic 的 [Claude Code](https://claude.ai/code) 构建
