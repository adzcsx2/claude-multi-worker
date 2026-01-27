# 🚀 CMS 快速开始 - 标签页模式

## ✨ 最简单的使用方式

### 方式一:直接使用 cms 命令 (推荐)

```bash
# 在项目目录下运行
python cms.bat tab

# 或指定实例
python cms.bat tab ui,coder,test
```

这会自动:

1. 启动 WezTerm (如果还没打开)
2. 创建多个标签页 (ui, coder, test)
3. 每个标签页运行一个 Claude 实例
4. 保存标签页映射到 `.cms_config/tab_mapping.json`

### 方式二:手动操作

#### 步骤 1: 打开 WezTerm

```bash
wezterm
```

#### 步骤 2: 进入项目目录

```bash
cd E:\ai_project\claude-multi-starter
```

#### 步骤 3: 启动标签页

```bash
python START_MULTI_TAB.py ui,coder,test
```

#### 步骤 4: 确认

```
Continue? (y/n): y
```

---

## 💬 实例间通信

启动完成后,在**任意终端**中使用 `send` 命令:

```bash
# 发送消息给 ui 实例
bin\send ui "设计一个登录页面"

# 发送消息给 coder 实例
bin\send coder "实现用户认证功能"

# 发送消息给 test 实例
bin\send test "测试登录流程"
```

**重要特性:**

- ✅ 消息会自动发送到对应的 Claude 实例
- ✅ 自动提交(就像按了回车)
- ✅ Claude 会立即看到并处理消息

---

## 📋 示例工作流

### 场景:开发一个用户登录功能

#### 1. 启动多实例

```bash
python cms.bat tab ui,coder,test
```

#### 2. 分配任务

在另一个终端窗口中:

```bash
# 给 UI 设计师分配任务
bin\send ui "设计一个现代化的登录页面,包含用户名、密码输入框和登录按钮"

# 给开发者分配任务
bin\send coder "实现登录API,使用JWT认证,连接数据库验证用户"

# 给测试工程师分配任务
bin\send test "为登录功能编写单元测试和集成测试"
```

#### 3. 查看结果

在 WezTerm 窗口中:

- 切换到 `ui` 标签页 → 查看 UI 设计
- 切换到 `coder` 标签页 → 查看代码实现
- 切换到 `test` 标签页 → 查看测试代码

#### 4. 协调反馈

```bash
# UI 完成后通知 coder
bin\send coder "UI设计已完成,请查看 designs/login.html"

# Coder 完成后通知 test
bin\send test "登录功能已实现,请开始测试"

# Test 发现问题反馈给 coder
bin\send coder "测试发现问题:密码长度验证未实现"
```

---

## 🎯 标签页操作

| 操作       | 快捷键           | 说明           |
| ---------- | ---------------- | -------------- |
| 切换标签页 | `Ctrl+Tab`       | 向右切换       |
| 反向切换   | `Ctrl+Shift+Tab` | 向左切换       |
| 关闭标签页 | `Ctrl+Shift+W`   | 关闭当前标签页 |
| 新建标签页 | `Ctrl+Shift+T`   | 手动新建标签页 |

---

## 📊 三种模式对比

| 模式       | 命令         | 优点             | 适用场景              |
| ---------- | ------------ | ---------------- | --------------------- |
| **标签页** | `cms tab`    | 🏆 紧凑、切换快  | 单显示器,需要快速切换 |
| **窗格**   | `cms pane`   | 可以同时看到多个 | 大显示器,需要同时监控 |
| **多窗口** | `cms window` | 独立窗口         | 多显示器,需要分屏显示 |

### 推荐使用标签页模式,因为:

- ✅ 更节省屏幕空间
- ✅ 切换更快速 (Ctrl+Tab)
- ✅ 更符合日常使用习惯
- ✅ 所有实例在同一个窗口中管理

---

## 🔧 可用实例

| 实例 ID   | 角色         | 用途               |
| --------- | ------------ | ------------------ |
| `ui`      | UI/UX 设计师 | 界面设计、用户体验 |
| `coder`   | 开发工程师   | 代码实现、功能开发 |
| `test`    | 测试工程师   | 单元测试、集成测试 |
| `default` | 协调者       | 整体协调、任务分配 |

### 自定义实例

编辑 `.cms_config/cms.config`:

```json
{
  "providers": ["claude"],
  "claude": {
    "enabled": true,
    "instances": [
      { "id": "ui", "role": "UI/UX designer", "autostart": true },
      { "id": "coder", "role": "developer", "autostart": true },
      { "id": "test", "role": "QA engineer", "autostart": true },
      { "id": "devops", "role": "DevOps engineer", "autostart": true }
    ]
  }
}
```

然后启动:

```bash
python cms.bat tab ui,coder,test,devops
```

---

## ❓ 常见问题

### Q: send 命令报错 "Unknown instance"

**A:** 确保已经运行了启动脚本,并且映射文件已生成:

```bash
ls .cms_config\tab_mapping.json
```

### Q: 消息发送了但 Claude 没反应

**A:** 检查:

1. Claude 是否正常运行
2. pane_id 是否正确
3. 尝试手动在对应标签页输入命令

### Q: 如何查看当前有哪些实例?

**A:** 查看映射文件:

```bash
type .cms_config\tab_mapping.json
```

### Q: 可以同时运行多种模式吗?

**A:** 可以,但会创建不同的映射文件。send 命令会优先使用标签页映射。

---

## 🎓 进阶技巧

### 1. 批量发送消息

创建一个批处理脚本 `distribute_tasks.bat`:

```batch
@echo off
bin\send ui "任务1: 设计登录页面"
bin\send coder "任务2: 实现登录API"
bin\send test "任务3: 编写测试用例"
echo 任务已分配!
```

运行:

```bash
distribute_tasks.bat
```

### 2. 使用 PowerShell 循环

```powershell
$tasks = @{
    "ui" = "设计任务"
    "coder" = "开发任务"
    "test" = "测试任务"
}

foreach ($instance in $tasks.Keys) {
    & bin\send $instance $tasks[$instance]
}
```

### 3. 保存会话历史

send 命令的输出可以重定向:

```bash
bin\send ui "任务内容" >> tasks.log
```

---

## 📚 相关文档

- [完整使用指南](USER_GUIDE.md)
- [多窗口模式](project-guide/MULTI_WINDOW_GUIDE.md)
- [自动化指南](project-guide/AUTOMATION_GUIDE.md)

---

## 🌟 快速参考卡

```
┌─────────────────────────────────────────────────────┐
│               CMS 快速参考                          │
├─────────────────────────────────────────────────────┤
│ 启动标签页:                                         │
│   python cms.bat tab                                │
│   python cms.bat tab ui,coder,test                  │
│                                                     │
│ 发送消息:                                           │
│   bin\send ui "消息内容"                            │
│   bin\send coder "消息内容"                         │
│   bin\send test "消息内容"                          │
│                                                     │
│ 切换标签页:                                         │
│   Ctrl+Tab          (下一个)                        │
│   Ctrl+Shift+Tab    (上一个)                        │
│                                                     │
│ 配置文件:                                           │
│   .cms_config\cms.config      (实例配置)            │
│   .cms_config\tab_mapping.json (标签页映射)         │
└─────────────────────────────────────────────────────┘
```

---

**祝你使用愉快! 🎉**

如有问题,请查看完整文档或提交 Issue。
