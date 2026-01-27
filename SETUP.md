# CMS 多实例启动 - 快速设置指南

## 新电脑设置步骤

### 1. 安装依赖

- **Python 3.8+**: [下载地址](https://www.python.org/downloads/)
- **WezTerm**: [下载地址](https://wezfurlong.org/wezterm/installation.html)
- **CMS (Claude Multi Starter)**: 需要先安装cms工具

### 2. 安装Skills

双击运行 `install-skills.bat` 或在PowerShell中运行：

```powershell
.\install-skills.ps1
```

这会自动将send skill安装到 `~/.claude/skills/` 目录。

### 3. 配置实例

编辑 `.cms_config/cms.config` 文件，根据需要添加或删除实例：

```json
{
  "claude": {
    "instances": [
      {"id": "default", "role": "general coordinator", "autostart": true},
      {"id": "ui", "role": "UI/UX designer", "autostart": true},
      {"id": "coder", "role": "developer", "autostart": true},
      {"id": "test", "role": "QA engineer", "autostart": true}
    ]
  }
}
```

支持1-12个实例，会自动创建对应的网格布局。

### 4. 启动

在WezTerm终端中运行：

```batch
start.bat
```

脚本会自动：
- 创建网格布局（根据实例数量）
- 在每个pane显示角色标签
- 启动对应的cms实例

## 使用

### 发送消息到其他实例

在任意CMS实例中使用send命令：

```
send ui "请帮我设计这个界面"
send coder "实现这个功能"
send test "测试这个API"
```

### 实例映射

Pane ID按照配置文件中的instances数组顺序映射：
- 第0个instance → pane 0
- 第1个instance → pane 1
- ...以此类推

### 文件说明

- `start.bat` - 启动脚本（调用start-dynamic.py）
- `start-dynamic.py` - 动态布局和启动逻辑
- `send_dynamic.py` - 发送消息到指定实例
- `send_to_pane.py` - 底层WezTerm pane通信
- `install-skills.ps1` - Skills自动安装脚本
- `.cms_config/cms.config` - 实例配置文件

## 故障排除

### Skills未加载

1. 确认已运行 `install-skills.bat`
2. 检查 `~/.claude/skills/send/` 目录是否存在
3. 重启CMS实例

### 发送消息失败

1. 确认在WezTerm环境中运行
2. 检查pane ID是否正确（使用 `wezterm cli list` 查看）
3. 确认目标实例已启动

### 布局混乱

1. 关闭所有pane重新启动
2. 检查 `.cms_config/cms.config` 配置是否正确
3. 实例数量不要超过12个

## 项目迁移

将整个项目文件夹复制到新电脑后：

1. 运行 `install-skills.bat` 安装skills
2. 在WezTerm中运行 `start.bat`
3. 完成！

无需手动配置，所有设置都在项目文件夹中。
