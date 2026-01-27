# 🧪 CMS 自动化测试指南

## 测试任务：创建一个简单的计算器

### 📋 测试流程

#### 阶段 1：启动 Claude 实例

1. **打开 WezTerm**
2. **创建 3 个窗格**（Ctrl+Shift+T）
3. **在每个窗格中运行**：
   ```bash
   claude
   ```

#### 阶段 2：初始化自动化模式

**窗格 1 (C1 - 设计)**:
```
我是 C1 窗口。启动自动化模式。
```

**窗格 2 (C2 - 开发)**:
```
我是 C2 窗口。启动自动化模式。
```

**窗格 3 (C3 - 测试)**:
```
我是 C3 窗口。启动自动化模式。
```

#### 阶段 3：观察自动化流程

自动化将按以下顺序执行：

1. **C1 (设计)** 分析需求并创建设计方案
   - 读取: `task-comms/automation-state.md`
   - 输出: `task-comms/from-c1-design.md`
   - 状态更新: STEP_INIT → STEP_DESIGN

2. **C2 (开发)** 根据设计实现代码
   - 读取: `task-comms/from-c1-design.md`
   - 输出: `calculator.html`
   - 状态更新: STEP_DESIGN → STEP_DEVELOP

3. **C3 (测试)** 编写并执行测试
   - 读取: `calculator.html`
   - 输出: 测试报告到 `task-comms/from-c3-test.md`
   - 状态更新: STEP_DEVELOP → STEP_TEST

4. **循环**: 如果测试失败 → 回到 C2 修复
5. **完成**: 如果测试通过 → 任务完成

#### 阶段 4：手动切换窗口

每次完成当前窗口的任务后，系统会提示：

```
✅ 任务完成！请切换到 CX 窗口并输入：继续
```

**操作方法**：
1. 点击 WezTerm 中的目标窗格
2. 输入：`继续`
3. 该窗口会自动执行下一步任务

### 📁 相关文件

```
task-comms/
├── automation-state.md      # 中央状态文件
├── from-c1-design.md        # C1 设计输出
├── from-c2-main.md          # C2 开发输出
└── from-c3-test.md          # C3 测试输出
```

### 🔍 监控进度

在命令行中查看状态：

```batch
# 查看自动化状态
type task-comms\automation-state.md

# 查看 C1 设计
type task-comms\from-c1-design.md

# 查看 C2 开发
type task-comms\from-c2-main.md

# 查看 C3 测试
type task-comms\from-c3-test.md
```

### ⚙️ 使用 send 命令（可选）

如果需要手动发送消息到某个窗口：

```batch
# 发送设计任务到 C1
bin\send ui "请优化计算器的界面设计"

# 发送开发任务到 C2
bin\send coder "请添加清除按钮功能"

# 发送测试任务到 C3
bin\send test "请增加边界值测试"
```

### 🎯 预期结果

成功完成后，你将获得：
1. ✅ `calculator.html` - 完整的计算器页面
2. ✅ 设计文档 - `from-c1-design.md`
3. ✅ 开发笔记 - `from-c2-main.md`
4. ✅ 测试报告 - `from-c3-test.md`

### 🚨 故障排除

**问题 1**: 窗口没有响应
- **解决**: 检查是否在正确的窗格输入了"继续"

**问题 2**: 状态文件未更新
- **解决**: 手动检查 `task-comms/automation-state.md`

**问题 3**: Claude 没有读取状态文件
- **解决**: 确保在 Claude 中明确说"启动自动化模式"

### 📝 测试检查清单

- [ ] 成功启动 3 个 Claude 实例
- [ ] 每个实例都初始化了自动化模式
- [ ] C1 完成设计并创建设计方案
- [ ] C2 完成开发并创建 calculator.html
- [ ] C3 完成测试并创建测试报告
- [ ] 所有任务完成后状态更新为 STEP_COMPLETE

---

**开始测试**: 打开 WezTerm → 创建 3 个窗格 → 运行 claude → 初始化自动化模式！
