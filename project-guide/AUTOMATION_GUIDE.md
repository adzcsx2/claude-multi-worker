# 多窗口自动化协作指南

> 三个窗口全自动循环工作，无需人工干预

---

## 🚨 AI 必须遵守的核心规则

```yaml
🤖 自动化执行规则（AI 必读）:

  启动条件:
    - 用户输入包含 "我是 C1/C2/C3 窗口" 和 "启动自动化模式"
    - 立即检查状态文件并执行任务（如果轮到自己）

  执行模式（省 Token 优化）:
    方案 A - 手动触发（推荐）:
      1. 读取 task-comms/automation-state.md
      2. 检查 current_window 是否等于自己的窗口ID
      3. 如果是自己 → 立即执行任务 → 更新状态 → 显示提示
      4. 如果不是自己 → 显示等待消息并停止（等待用户再次输入）
      5. 完成后明确提示用户："✅ 任务完成！请切换到 CX 窗口并输入：继续"

    方案 B - 文件监控（高级）:
      1. 使用 PowerShell FileSystemWatcher 监控文件变化
      2. 仅在 automation-state.md 被修改时才触发检查
      3. 避免持续轮询，节省 Token

  执行任务后（重要！）:
    ✅ 必须更新 task-comms/automation-state.md
    ✅ 必须修改以下字段：
       - Current Step: 更新为下一步骤
       - Current Window: 更新为下一窗口
       - Current Index: 如需要则递增
    ✅ 必须在状态历史表格中添加记录
    ✅ 显示明确的切换提示："🔄 请切换到 CX 窗口"
    ✅ 停止执行，等待用户手动触发下一窗口

  禁止行为:
    ❌ 不要持续轮询（浪费 Token）
    ❌ 不要在不是自己的回合时反复检查
    ❌ 不要忘记更新状态文件
    ❌ 不要忘记提示用户切换窗口
```

---

## 🎯 自动化流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    全自动循环工作流程                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   C1 (设计窗口)                                                         │
│      ↓ 设计完成                                                         │
│   C2 (主任务窗口) ──→ 自动通知 ──→ C3 (测试窗口)                        │
│      ↓ 开发完成                      ↓ 测试完成                          │
│   C3 (测试窗口)                   └──→ 返回 C1 (下一个界面)              │
│                                                                         │
│   循环: C1 → C2 → C3 → C1 → C2 → C3 ...                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 目录结构

```
project/
├── task-comms/
│   ├── automation-state.md         # 中央状态文件（核心！）
│   ├── from-c1-design.md           # C1 发送的消息
│   ├── from-c2-main.md             # C2 发送的消息
│   └── from-c3-test.md             # C3 发送的消息
│
└── memory-bank/
    ├── 07-design-system.md         # 设计系统（C1 创建）
    ├── 06-ui-design.md             # UI 设计文档（C1 维护）
    └── 05-progress.md              # 项目进度
```

---

## 🔄 中央状态文件（核心）

**`task-comms/automation-state.md`**

```markdown
# 自动化状态

## 当前状态

- **当前步骤**: STEP_INIT
- **当前窗口**: C1
- **当前界面索引**: 0
- **自动化模式**: ENABLED

## 界面列表

- [0] 登录页面
- [1] 主页
- [2] 个人中心
- [3] 设置页面

## 步骤定义

| 步骤          | 执行窗口 | 动作             | 下一步       |
| ------------- | -------- | ---------------- | ------------ |
| STEP_INIT     | C1       | 创建设计系统     | STEP_DESIGN  |
| STEP_DESIGN   | C1       | 设计当前界面     | STEP_DEVELOP |
| STEP_DEVELOP  | C2       | 开发当前界面     | STEP_TEST    |
| STEP_TEST     | C3       | 测试当前界面     | STEP_NEXT    |
| STEP_NEXT     | -        | 移动到下一个界面 | STEP_DESIGN  |
| STEP_COMPLETE | -        | 所有界面完成     | 结束         |

## 状态历史

| 时间   | 窗口 | 步骤      | 操作   |
| ------ | ---- | --------- | ------ |
| {时间} | C1   | STEP_INIT | 初始化 |
```

---

## 🚀 启动自动化

### 第 1 步：初始化项目

在任意一个窗口运行：

```bash
你: 初始化自动化项目
```

AI 会自动创建：

- `task-comms/automation-state.md`（中央状态文件）
- `task-comms/from-c1-design.md`
- `task-comms/from-c2-main.md`
- `task-comms/from-c3-test.md`

### 第 2 步：启动三个窗口

```bash
# 终端 1 - C1 设计窗口
cd your-project
claude

# 终端 2 - C2 主任务窗口
cd your-project
claude

# 终端 3 - C3 测试窗口
cd your-project
claude
```

### 第 3 步：为每个窗口分配角色

**C1 窗口（设计）：**

```
你: 我是 C1 窗口，设计任务。启动自动化模式。
```

**C2 窗口（主任务）：**

```
你: 我是 C2 窗口，主任务。启动自动化模式。
```

**C3 窗口（测试）：**

```
你: 我是 C3 窗口，测试任务。启动自动化模式。
```

---

## 🤖 窗口自动化逻辑

### C1（设计窗口）自动化逻辑

```python
# 伪代码
def c1_automation():
    while True:
        # 1. 读取状态
        state = read_state("task-comms/automation-state.md")

        # 2. 检查是否轮到自己
        if state.current_window != "C1":
            sleep(5)  # 等待 5 秒后重试
            continue

        # 3. 执行当前步骤
        if state.current_step == "STEP_INIT":
            # 初始化：创建设计系统
            create_design_system()
            update_state(step="STEP_DESIGN", window="C1")

        elif state.current_step == "STEP_DESIGN":
            # 设计当前界面
            current_index = state.current_index
            design_interface(current_index)

            # 通知 C2 开始开发
            notify("from-c1-design.md",
                   f"界面 {current_index} 设计完成，请开发")
            update_state(step="STEP_DEVELOP", window="C2")

        elif state.current_step == "STEP_NEXT":
            # 移动到下一个界面
            next_index = state.current_index + 1
            if next_index < len(interface_list):
                update_state(step="STEP_DESIGN",
                           window="C1",
                           index=next_index)
            else:
                update_state(step="STEP_COMPLETE", window="ALL")
```

### C2（主任务窗口）自动化逻辑

```python
def c2_automation():
    while True:
        state = read_state("task-comms/automation-state.md")

        if state.current_window != "C2":
            sleep(5)
            continue

        if state.current_step == "STEP_DEVELOP":
            # 读取设计文档
            read("memory-bank/07-design-system.md")
            read("memory-bank/06-ui-design.md")

            # 开发当前界面
            current_index = state.current_index
            develop_interface(current_index)

            # 通知 C3 开始测试
            notify("from-c2-main.md",
                   f"界面 {current_index} 开发完成，请测试")
            update_state(step="STEP_TEST", window="C3")
```

### C3（测试窗口）自动化逻辑

```python
def c3_automation():
    while True:
        state = read_state("task-comms/automation-state.md")

        if state.current_window != "C3":
            sleep(5)
            continue

        if state.current_step == "STEP_TEST":
            # 测试当前界面
            current_index = state.current_index
            test_interface(current_index)

            if test_passed:
                # 生成测试报告
                generate_test_report(
                    output_dir="test/reports/",
                    screenshots_dir="test/screenshots/",
                    logs_dir="test/logs/"
                )

                # 通知 C1 进行下一个界面
                notify("from-c3-test.md",
                       f"界面 {current_index} 测试通过，进行下一个\n"
                       f"测试报告: test/reports/\n"
                       f"截图: test/screenshots/\n"
                       f"日志: test/logs/")
                update_state(step="STEP_NEXT", window="C1")
            else:
                # 保存失败截图和日志
                save_failure_artifacts(
                    screenshots_dir="test/screenshots/failures/",
                    logs_dir="test/logs/failures/"
                )

                # 通知 C2 修复问题
                notify("from-c3-test.md",
                       f"界面 {current_index} 测试失败，请修复\n"
                       f"失败截图: test/screenshots/failures/\n"
                       f"失败日志: test/logs/failures/")
                update_state(step="STEP_DEVELOP", window="C2")

def test_interface(index):
    """测试界面的完整流程"""
    # 1. 确保 test/ 目录结构存在
    ensure_test_dirs()

    # 2. 单元测试
    run_unit_tests(
        output_report="test/reports/unit/"
    )

    # 3. UI 模拟测试（Android）
    if is_android():
        run_ui_simulation_tests(
            screenshots_dir="test/screenshots/ui-simulation/",
            logs_dir="test/logs/ui-simulation/",
            report_dir="test/reports/ui-simulation/"
        )

    # 4. 生成测试报告
    generate_report(
        output_file="test/reports/summary.json"
    )

def ensure_test_dirs():
    """确保测试目录结构存在"""
    dirs = [
        "test/screenshots/",
        "test/screenshots/ui-simulation/",
        "test/screenshots/failures/",
        "test/reports/",
        "test/reports/unit/",
        "test/reports/ui-simulation/",
        "test/logs/",
        "test/logs/ui-simulation/",
        "test/logs/failures/",
        "test/scripts/",
        "test/temp/"
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
```

---

## � 状态更新函数（AI 必须使用）

### update_state() 函数说明

**每次完成任务后，必须调用此函数更新状态文件！**

```python
def update_state(step, window, index=None):
    """
    更新 task-comms/automation-state.md

    Args:
        step: 下一步骤 (STEP_DESIGN, STEP_DEVELOP, STEP_TEST, STEP_NEXT, STEP_COMPLETE)
        window: 下一窗口 (C1, C2, C3, ALL)
        index: 界面索引（可选，仅在 STEP_NEXT 时递增）
    """
    # 1. 读取当前状态文件
    with open("task-comms/automation-state.md", "r") as f:
        content = f.read()

    # 2. 更新 Current State 部分
    content = re.sub(
        r'- \*\*Current Step\*\*: .*',
        f'- **Current Step**: {step}',
        content
    )
    content = re.sub(
        r'- \*\*Current Window\*\*: .*',
        f'- **Current Window**: {window}',
        content
    )

    if index is not None:
        content = re.sub(
            r'- \*\*Current Index\*\*: .*',
            f'- **Current Index**: {index}',
            content
        )

    # 3. 添加状态历史记录
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_line = f"| {current_time} | {window} | {step} | {index or 'N/A'} | 状态已更新 |"

    # 在状态历史表格末尾添加新记录
    content = content.rstrip() + f"\n{history_line}\n"

    # 4. 写回文件
    with open("task-comms/automation-state.md", "w") as f:
        f.write(content)

    print(f"✅ 状态已更新: {step} → {window}")
```

### 实际使用示例

**C1 完成设计后：**

```python
# 设计完成，通知 C2 开始开发
update_state(
    step="STEP_DEVELOP",
    window="C2",
    index=None  # 保持当前索引不变
)
```

**C2 完成开发后：**

```python
# 开发完成，通知 C3 开始测试
update_state(
    step="STEP_TEST",
    window="C3",
    index=None
)
```

**C3 测试通过后：**

```python
# 测试通过，通知 C1 进入下一界面
update_state(
    step="STEP_NEXT",
    window="C1",
    index=None
)
```

**C1 收到 STEP_NEXT 后：**

```python
# 读取当前索引
current_index = read_current_index()
next_index = current_index + 1

# 检查是否还有更多界面
if next_index < total_interfaces:
    # 继续下一个界面
    update_state(
        step="STEP_DESIGN",
        window="C1",
        index=next_index
    )
else:
    # 所有界面完成
    update_state(
        step="STEP_COMPLETE",
        window="ALL",
        index=None
    )
```

---

## 📋 窗口启动命令

### 🎯 方案 A：手动触发模式（推荐 - 省 Token）

**C1 窗口启动：**

```bash
你: 我是 C1 窗口，设计任务。启动自动化模式。

AI 会执行：
├── 1. 读取 task-comms/automation-state.md
├── 2. 检查 current_window 是否为 "C1"
├── 3. 如果是 → 执行任务 → 更新状态 → 提示切换
├── 4. 如果不是 → 显示 "⏸️ 等待中，当前轮到 CX" 并停止
└── 5. 完成后提示："✅ 任务完成！🔄 请切换到 C2 窗口并输入：继续"
```

**后续触发（在任意窗口）：**

```bash
你: 继续

AI 会执行：
├── 1. 读取 task-comms/automation-state.md
├── 2. 检查是否轮到自己
├── 3. 执行任务 → 更新状态 → 提示下一窗口
└── 4. 显示："✅ 完成！🔄 请切换到 CX 窗口并输入：继续"
```

### C2 窗口启动

```bash
你: 我是 C2 窗口，主任务。启动自动化模式。

AI 会执行：（同 C1 逻辑）
├── 检查是否轮到自己
├── 是 → 执行开发任务
├── 否 → 显示等待消息并停止
└── 完成后提示："✅ 开发完成！🔄 请切换到 C3 窗口并输入：继续"
```

### C3 窗口启动

```bash
你: 我是 C3 窗口，测试任务。启动自动化模式。

AI 会执行：（同上）
├── 检查是否轮到自己
├── 是 → 执行测试任务
├── 否 → 显示等待消息并停止
└── 完成后提示："✅ 测试完成！🔄 请切换到 C1 窗口并输入：继续"

⚠️ 测试文件保存位置：
- 截图 → test/screenshots/
- 报告 → test/reports/
- 日志 → test/logs/
```

---

### 🔧 方案 B：文件监控模式（高级 - 自动触发）

创建监控脚本 `watch-automation.ps1`：

```powershell
# 监控 automation-state.md 文件变化
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "task-comms"
$watcher.Filter = "automation-state.md"
$watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite

$action = {
    Write-Host "🔔 状态文件已更新，检查是否需要执行任务..."
    # 这里可以触发 Claude API 调用（需要额外开发）
}

Register-ObjectEvent $watcher "Changed" -Action $action
Write-Host "📡 开始监控 automation-state.md..."
while ($true) { Start-Sleep -Seconds 1 }
```

**优点：** 完全自动，无需手动切换窗口  
**缺点：** 需要额外开发 API 集成

---

## 💡 使用建议

| 场景             | 推荐方案        | 原因                 |
| ---------------- | --------------- | -------------------- |
| 少量界面 (1-5个) | 方案 A 手动触发 | 省 Token，控制性强   |
| 大量界面 (10+个) | 方案 B 文件监控 | 完全自动化，节省时间 |
| 测试阶段         | 方案 A          | 便于观察每步结果     |
| 生产部署         | 方案 B          | 提高效率             |

---

## 🔄 状态转换流程

```
初始状态
   ↓
┌─────────────────────────────────────────────────────┐
│ STEP_INIT                                           │
│ 当前窗口: C1                                        │
│ 动作: C1 创建设计系统                               │
│ 下一步: STEP_DESIGN, 窗口 C1                        │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ STEP_DESIGN                                         │
│ 当前窗口: C1                                        │
│ 动作: C1 设计当前界面                               │
│ 下一步: STEP_DEVELOP, 窗口 C2                       │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ STEP_DEVELOP                                        │
│ 当前窗口: C2                                        │
│ 动作: C2 开发当前界面                               │
│ 下一步: STEP_TEST, 窗口 C3                          │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ STEP_TEST                                           │
│ 当前窗口: C3                                        │
│ 动作: C3 测试当前界面                               │
│   ├─ 通过 → STEP_NEXT, 窗口 C1                      │
│   └─ 失败 → STEP_DEVELOP, 窗口 C2 (修复)            │
└─────────────────────────────────────────────────────┘
   ↓ (测试通过)
┌─────────────────────────────────────────────────────┐
│ STEP_NEXT                                           │
│ 当前窗口: C1                                        │
│ 动作: 移动到下一个界面                              │
│   ├─ 有下一个 → STEP_DESIGN, 界面索引+1             │
│   └─ 无下一个 → STEP_COMPLETE, 所有窗口            │
└─────────────────────────────────────────────────────┘
```

---

## 🔁 恢复中断的任务

### 场景：关闭了窗口，如何继续？

```bash
# 重新打开窗口，输入：
你: 我是 C1 窗口，恢复自动化模式。

# AI 会自动：
├── 1. 读取 task-comms/automation-state.md
├── 2. 查看当前步骤和界面索引
├── 3. 从中断的地方继续执行
└── 4. 无需手动输入，自动继续
```

### 示例：中断恢复

```
关闭前的状态：
- 当前步骤: STEP_TEST
- 当前窗口: C3
- 当前界面: 2 (个人中心)

重新打开所有窗口后：
├── C1: 读取状态，发现轮到 C3，等待
├── C2: 读取状态，发现轮到 C3，等待
└── C3: 读取状态，发现轮到自己，继续 STEP_TEST

C3 完成测试后，自动进入 STEP_NEXT，通知 C1 继续下一个界面
```

---

## 📊 监控自动化进度

### 查看当前状态

```bash
你: 查看自动化状态

AI 会显示：
┌─────────────────────────────────────────────────────┐
│ 🤖 自动化状态                                       │
├─────────────────────────────────────────────────────┤
│ 当前步骤: STEP_DEVELOP                              │
│ 当前窗口: C2                                        │
│ 当前界面: 1 (主页)                                  │
│ 进度: 1/4 界面 (25%)                                │
├─────────────────────────────────────────────────────┤
│ C1 状态: 等待中                                     │
│ C2 状态: 🔄 开发中...                               │
│ C3 状态: 等待中                                     │
└─────────────────────────────────────────────────────┘
```

---

## ⚙️ 完全自动化规则

### AI 必须遵守的规则

```yaml
自动化规则:
  检查状态:
    - 每 5 秒检查一次 task-comms/automation-state.md
    - 读取 current_step 和 current_window

  判断是否轮到自己:
    - 是 current_window == 自己的窗口ID
    - 否: 继续等待

  执行任务:
    - 读取相关文档
    - 执行任务
    - 更新状态文件
    - 通知下一个窗口

  无需人工确认:
    - 不等待用户输入 "继续"
    - 不等待用户输入 "同意"
    - 自动执行下一步

  错误处理:
    - 测试失败: 自动通知 C2 修复
    - 修复失败: 自动重试，最多 3 次
```

---

## 🎬 快速开始

### 一键启动三个窗口

```bash
# 终端 1
cd your-project && claude
# 输入: 我是 C1 窗口，设计任务。启动自动化模式。

# 终端 2
cd your-project && claude
# 输入: 我是 C2 窗口，主任务。启动自动化模式。

# 终端 3
cd your-project && claude
# 输入: 我是 C3 窗口，测试任务。启动自动化模式。

# 然后就可以离开了，AI 会自动循环工作！
```

---

## 📝 状态文件模板

**`task-comms/automation-state.md` 初始模板：**

```markdown
# 自动化状态

## 当前状态

- **当前步骤**: STEP_INIT
- **当前窗口**: C1
- **当前界面索引**: 0
- **自动化模式**: ENABLED
- **开始时间**: {时间}

## 界面列表

请在此处添加所有需要设计/开发/测试的界面：

- [0] {界面名称}
- [1] {界面名称}
- [2] {界面名称}
- ...

## 步骤定义

| 步骤          | 执行窗口 | 动作                               | 下一步                            |
| ------------- | -------- | ---------------------------------- | --------------------------------- |
| STEP_INIT     | C1       | 创建设计系统 (07-design-system.md) | STEP_DESIGN                       |
| STEP_DESIGN   | C1       | 设计当前界面                       | STEP_DEVELOP                      |
| STEP_DEVELOP  | C2       | 开发当前界面                       | STEP_TEST                         |
| STEP_TEST     | C3       | 测试当前界面                       | 通过→STEP_NEXT, 失败→STEP_DEVELOP |
| STEP_NEXT     | -        | 索引+1, 移动到下一个界面           | STEP_DESIGN                       |
| STEP_COMPLETE | ALL      | 所有界面完成                       | 结束                              |

## 状态历史

| 时间 | 窗口 | 步骤 | 界面索引 | 操作 |
| ---- | ---- | ---- | -------- | ---- |
```

---

_本文档遵循 Vibe Coding 方法论 V1.2.2_
