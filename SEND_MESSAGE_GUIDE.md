# 📋 完整使用指南 - 发送消息到 WezTerm 标签页

## ⚠️ 重要前提

**以下命令必须在 WezTerm 的某个标签页内运行，而不是外部的 PowerShell！**

---

## ✅ 当前状态

你已经有：
- ✅ 3个 WezTerm 标签页运行 Claude（pane 0, 1, 2）
- ✅ 映射文件已创建（`.cms_config/tab_mapping.json`）
- ✅ 映射关系：c1→0, c2→1, c3→2

---

## 🚀 发送消息步骤

### 步骤 1：切换到 WezTerm 标签页

**在 WezTerm 的第4个标签页（cmd）中运行以下命令：**

```cmd
cd E:\ai_project\claude-multi-starter
```

### 步骤 2：测试发送消息

**⚠️ 必须在 WezTerm 标签页内运行：**

```cmd
python send-tab.py c1 "继续"
```

如果成功，你会在第1个标签页（pane 0）看到消息"继续"被自动输入。

### 步骤 3：向其他标签页发送消息

```cmd
REM 发送到 c2（pane 1）
python send-tab.py c2 "继续"

REM 发送到 c3（pane 2）
python send-tab.py c3 "继续"
```

---

## 🔍 如果发送失败

### 诊断命令（⚠️ 必须在 WezTerm 内运行）：

```cmd
python test-wezterm-cli.py
```

这会测试：
1. `wezterm cli list` 是否工作
2. `wezterm cli send-text` 是否工作

### 常见问题：

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `Command timeout` | 从 PowerShell 运行而不是 WezTerm | 在 WezTerm 标签页内运行 |
| `Socket connection failed` | WezTerm 进程不匹配 | 确保在同一个 WezTerm 窗口内 |
| `pane_id not found` | 映射文件错误 | 重新创建映射 |

---

## 📝 自动化工作流示例

在 WezTerm 的 cmd 标签页中创建一个批处理文件：

**auto-trigger.bat:**
```bat
@echo off
echo [C1] 触发设计任务...
python send-tab.py c1 "继续"
timeout /t 30 /nobreak

echo [C2] 触发开发任务...
python send-tab.py c2 "继续"
timeout /t 30 /nobreak

echo [C3] 触发测试任务...
python send-tab.py c3 "继续"
timeout /t 30 /nobreak

echo [循环] 回到 C1...
goto :loop
```

**运行：**
```cmd
REM ⚠️ 在 WezTerm 标签页内运行
auto-trigger.bat
```

---

## 🎯 快速参考

### 在 WezTerm 外（PowerShell）可以做的：
- ✅ 查看映射文件：`Get-Content .cms_config\tab_mapping.json`
- ✅ 编辑文件
- ✅ Git 操作
- ❌ **不能**发送消息（send-tab.py 会超时）

### 在 WezTerm 内（任意标签页）可以做的：
- ✅ 发送消息：`python send-tab.py c1 "继续"`
- ✅ 测试 CLI：`wezterm cli list`
- ✅ 创建映射：`python fix-mapping.py`
- ✅ 所有自动化操作

---

## 💡 原理说明

`wezterm cli` 命令需要连接到当前 WezTerm 进程的 mux server。

- 从 **WezTerm 标签页内**运行 → 自动连接到正确的 socket ✅
- 从 **外部 PowerShell** 运行 → 找不到 socket，超时 ❌

这就是为什么必须在 WezTerm 内运行发送命令！
