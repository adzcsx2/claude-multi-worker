# CMS 多实例启动系统 - 完整指南

## 🎯 系统概述

CMS (Claude Multi Starter) 是一个多实例 Claude 协作系统，可以在一个 WezTerm 窗口中创建多个子窗格，每个子窗格运行独立的 Claude 实例，实例之间可以互相通信。

---

## 📊 核心概念

### 窗格 (Pane) = 子窗口 (Sub-window)

```
┌─────────────────────────────────────────┐
│         WezTerm 窗口                    │
├──────────────┬──────────────────────────┤
│ 子窗格 1      │ 子窗格 2                 │
│ (ui)         │ (coder)                 │
│              │                          │
│ claude>      │ claude>                 │
└──────────────┴──────────────────────────┘
```

**关键点:**
- ✅ 一个 WezTerm 主窗口
- ✅ 多个子窗格（pane）
- ✅ 每个子窗格运行独立的 Claude 实例
- ✅ 子窗格之间可以互相通信
- ✅ 每个子窗格的标题显示实例名称

---

## 🚀 快速开始

### 步骤 1: 打开 WezTerm

从 Windows 开始菜单启动 WezTerm，或运行:
```bash
wezterm
```

### 步骤 2: 进入项目目录

```bash
cd E:\ai_project\claude-multi-starter
```

### 步骤 3: 启动多实例

```bash
python START_MULTI_PANE.py ui,coder
```

### 步骤 4: 确认继续

```
Continue? (y/n): y
```

**输入 `y` 并回车**

### 步骤 5: 查看结果

你会看到:
- 一个 WezTerm 窗口
- 两个子窗格（左右分割）
- 左边窗格: ui 实例
- 右边窗格: coder 实例

---

## 📋 可用实例

| 实例 ID | 角色 | 描述 |
|---------|------|------|
| `ui` | UI/UX 设计师 | 负责界面设计和用户体验 |
| `coder` | 开发者 | 负责代码实现 |
| `test` | QA 工程师 | 负责测试和质量保证 |
| `default` | 协调者 | 负责整体协调 |

---

## 🎯 启动不同数量的实例

### 启动 2 个实例（左右分割）

```bash
python START_MULTI_PANE.py ui,coder
```

**布局:**
```
┌────────────┬────────────┐
│ ui         │ coder      │
└────────────┴────────────┘
```

### 启动 3 个实例（T 型布局）

```bash
python START_MULTI_PANE.py ui,coder,test
```

**布局:**
```
┌────────────┬────────────┐
│ ui         │ coder      │
├────────────┴────────────┤
│ test                    │
└─────────────────────────┘
```

### 启动 4 个实例（四象限）

```bash
python START_MULTI_PANE.py default,ui,coder,test
```

**布局:**
```
┌────────────┬────────────┐
│ default    │ ui         │
├────────────┼────────────┤
│ coder      │ test       │
└────────────┴────────────┘
```

---

## 📡 实例间通信

### 发送消息

在 Windows 命令行（新窗口）中:

```bash
# 发送任务到 ui 实例
bin\send ui "设计登录页面"

# 发送任务到 coder 实例
bin\send coder "实现登录功能"

# 发送任务到 test 实例
bin\send test "测试登录功能"
```

### 查看状态

```bash
show-status.bat
```

### 测试通信

```bash
test_communication.bat
```

---

## 💡 窗格操作

### 切换窗格

使用快捷键在不同窗格间切换:

```
Ctrl+Shift+→  切换到右边窗格
Ctrl+Shift+←  切换到左边窗格
Ctrl+Shift+↑  切换到上方窗格
Ctrl+Shift+↓  切换到下方窗格
```

### 调整窗格大小

```
Ctrl+Shift++   增大当前窗格
Ctrl+Shift+-   减小当前窗格
```

---

## 🔍 验证成功

执行后请检查:

- [ ] WezTerm 打开
- [ ] 只有一个 WezTerm 主窗口
- [ ] 主窗口内有多个子窗格
- [ ] 每个子窗格显示 `claude>` 提示符
- [ ] 子窗格标签/标题显示实例名称
- [ ] `bin\send ui "测试"` 可以发送消息
- [ ] 在对应窗格中能看到收到的消息
- [ ] `show-status.bat` 可以查看状态

---

## 🆘 故障排除

### 问题 1: "Not running in WezTerm"

**原因:** 不在 WezTerm 环境中运行

**解决方案:**
1. 打开 WezTerm（不是普通命令行）
2. 在 WezTerm 的终端中操作
3. 确保看到 WezTerm 的提示符

### 问题 2: 窗格创建失败

**检查 WezTerm 版本:**
```bash
wezterm --version
```

**确保:** WezTerm 2020.3 或更高版本

### 问题 3: send 命令无法通信

**检查映射文件:**
```bash
type .cms_config\pane_mapping.json
```

**确保:** pane_mapping.json 包含所有实例的映射

### 问题 4: 找不到配置文件

**检查配置:**
```bash
type .cms_config\cms.config
```

**如果不存在:** 系统会使用默认配置

---

## 📚 相关文档

| 文档 | 描述 |
|------|------|
| `START_HERE.bat` | 快速开始向导 |
| `APPROACH_COMPARISON.md` | 多实例方式对比 |
| `MULTI_PANE_CORRECT.md` | 正确使用指南 |
| `FINAL_GUIDE.txt` | 快速参考指南 |
| `TEST_MULTI_PANE.bat` | 测试启动器 |
| `test_communication.bat` | 测试通信功能 |

---

## 🎉 典型工作流程

### 场景: 三人协作开发

#### 1. 启动三个实例

```bash
python START_MULTI_PANE.py ui,coder,test
```

#### 2. 分配任务

在 Windows 命令行中:

```bash
# UI 设计任务
bin\send ui "设计用户登录页面，包括用户名、密码输入框和登录按钮"

# 开发任务
bin\send coder "实现用户登录功能，使用 Flask 框架，包含表单验证"

# 测试任务
bin\send test "编写登录功能的测试用例，包括正常和异常情况"
```

#### 3. 查看进度

在各窗格中使用 `Ctrl+Shift+方向键` 切换，查看每个实例的工作状态

#### 4. 检查状态

```bash
show-status.bat
```

---

## 📝 快速参考

```bash
# 启动
1. 打开 WezTerm
2. cd E:\ai_project\claude-multi-starter
3. python START_MULTI_PANE.py ui,coder,test
4. 输入 y 确认

# 切换窗格
Ctrl+Shift+方向键

# 通信
bin\send <instance> <message>

# 查看状态
show-status.bat
```

---

## ✅ 成功标志

完成上述步骤后，你应该看到:

1. ✅ WezTerm 窗口打开
2. ✅ 窗口内有多个子窗格
3. ✅ 每个子窗格显示 `claude>` 提示符
4. ✅ 子窗格标签显示实例名称
5. ✅ `bin\send ui "测试"` 可以发送消息
6. ✅ `show-status.bat` 可以查看状态
7. ✅ 窗格之间可以互相通信

---

**现在就开始吧！** 🚀

1. 打开 WezTerm
2. `cd E:\ai_project\claude-multi-starter`
3. `python START_MULTI_PANE.py ui,coder`
4. 输入 `y` 并回车

应该会在一个 WezTerm 窗口中创建 2 个子窗格！
