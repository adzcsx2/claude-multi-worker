# Vibe Coding 通用交互式项目指南

> 适用于任何软件项目的 AI 协作开发指南

**完整文档结构：**
- `PROJECT_GUIDE.md` - 本文件，核心规则与快速开始
- `TESTING_GUIDE.md` - 测试指南，四层测试验证详解
- `WORKFLOW_GUIDE.md` - 工作流程，详细操作说明
- `TEMPLATES.md` - 文档模板，Memory Bank 模板和示例

> 💡 **Claude 使用提示**: 这些文件位于 `project-guide/` 目录下，Claude 会优先读取这些文档来理解项目规范。

---

## ⚠️ CRITICAL RULES（代码编写前必须执行）

```yaml
# IMPORTANT:
# Always read memory-bank/04-architecture.md before writing any code. Include entire database schema.
# Always read memory-bank/02-product-requirements.md before writing any code.
# Always read memory-bank/07-design-system.md before implementing UI (统一的设计系统规范).
# Always read memory-bank/06-ui-design.md before implementing UI (includes /ui folder designs).
# After adding a major feature or completing a milestone, update memory-bank/04-architecture.md.

# CRITICAL: 步骤完成后必须更新 05-progress.md 状态！
# 将当前步骤从 "🔄 进行中" 改为 "✅ 已完成"
# 将下一步从 "⏳ 待开始" 改为 "🔄 进行中"
# 否则下次对话会重复执行！

# CRITICAL: 每完成一个步骤，必须进行完全自动化测试！
# 【测试流程 - 完全自动化，无需人工介入】
# 1. 编译项目（确保代码没有语法错误）
#    - Android: ./gradlew build
#    - Web: npm run build
#    - 后端: 对应的编译命令
# 2. 自动生成并运行测试（完全自动化，无人工介入）
#    【强制规则 - Android】
#    - 编译必须通过才能继续下一步（编译失败不允许跳过，必须修复）
#    - 单元测试必须通过才能继续下一步
#    - UI模拟测试（adb控制模拟器真实操作）必须通过才能继续下一步
#    - 任一测试失败自动修复并重测，不允许跳过
#    - 测试通过后自动更新进度，无需用户确认
# 【强制规则 - 所有项目】
# ⚠️ 编译是第一道关卡，编译失败绝对不允许进行下一步
# - 编译失败 → 自动修复，不允许继续，不允许跳过
# - 编译通过后才能执行测试
# - 测试失败 → 自动修复并重测，不允许跳过
# - 未执行测试 → 自动补测，不允许跳过
# - 编译和测试全部通过后，自动更新 05-progress.md 状态，无需用户确认

# 详细的测试流程请参考: TESTING_GUIDE.md
```

---

## 📂 相关文档

- **[TESTING_GUIDE.md](project-guide/TESTING_GUIDE.md)** - 测试指南
  - 测试文件目录结构
  - 测试验证详解（编译、单元测试、UI模拟测试）
  - 测试报告格式

- **[WORKFLOW_GUIDE.md](project-guide/WORKFLOW_GUIDE.md)** - 工作流程
  - 新建项目流程
  - 继续开发流程
  - 8种操作详细说明
  - 使用示例

- **[TEMPLATES.md](project-guide/TEMPLATES.md)** - 文档模板
  - Memory Bank 文档模板（5个核心文档）
  - 进度状态管理
  - Git 提交与回滚

- **[MULTI_WINDOW_GUIDE.md](project-guide/MULTI_WINDOW_GUIDE.md)** - 多窗口协同指南
  - 使用多个 Claude CLI 窗口协同开发
  - 避免上下文丢失
  - 任务队列系统
  - 窗口间通信机制

---

## 🚀 项目状态检测

Claude 会自动检测你的项目状态：

```
当前目录: {工作目录}

检测中...
├── memory-bank/ 文件夹存在？
│   ├── ❌ 不存在 → 【新建项目模式】→ 参考 WORKFLOW_GUIDE.md
│   └── ✅ 存在 → 继续检测
│       ├── 05-progress.md 存在？
│       │   ├── ❌ 不存在 → 【初始化项目模式】
│       │   └── ✅ 存在 → 【继续开发模式】→ 参考 WORKFLOW_GUIDE.md
```

---

## 📖 快速开始

### 新建项目
1. 在项目目录运行 `setup-project.bat` 或 `setup-project.sh`
2. Claude 会引导你完成项目初始化
3. 自动生成 `memory-bank/` 目录和文档

### 继续开发
1. 打开 Claude Code
2. Claude 会自动检测项目状态
3. 根据菜单选择操作

---

## ⚡ 快捷命令

| 用户输入 | 说明 |
|---------|------|
| `继续` 或 `1` | 执行下一步 |
| `查看` 或 `2` | 查看进度 |
| `架构` 或 `3` | 查看架构 |
| `添加` 或 `4` | 添加功能 |
| `修复 [问题描述]` | 快速修复问题 |
| `跳过` | 跳过当前步骤 |
| `重置` | 重置当前步骤状态 |

---

## 📌 Claude 行为规则总结

### 会话开始时
1. 检查 memory-bank/ 文件夹是否存在
2. 根据检测结果进入对应模式（新建/继续）
3. 展示对应操作菜单

### 代码编写前（CRITICAL - Always 规则）
```yaml
# IMPORTANT:
# Always read memory-bank/04-architecture.md before writing any code. Include entire database schema.
# Always read memory-bank/02-product-requirements.md before writing any code.
# Always read memory-bank/07-design-system.md before implementing UI (设计系统规范).
# Always read memory-bank/06-ui-design.md before implementing UI (UI 设计图).
```
1. 读取 04-architecture.md（包含完整数据库 schema）
2. 读取 02-product-requirements.md
3. 如果是 UI 开发，先读取 07-design-system.md（设计系统）
4. 如果是 UI 开发，再读取 06-ui-design.md（UI 设计图）
5. 读取 01-tech-stack.md
6. 检查是否有冲突

### 代码编写后（CRITICAL - 进度更新规则）

**必须按以下顺序执行（完全自动化）：**
1. **编译项目**（确保代码没有语法错误）⚠️ **编译必须通过才能继续，编译失败绝对不允许跳过**
2. **编译通过后，自动生成并运行测试（Android必须全部通过才能继续）**
   - 详见 TESTING_GUIDE.md
3. ⚠️ 如果编译失败 → **自动修复问题并重新编译，编译失败绝对不允许跳过，绝对不允许进行下一步**
4. 如果测试失败 → 自动修复问题并重新执行步骤 1-3
5. 编译和测试全部通过后，**自动更新** 05-progress.md（**状态转换**：进行中→已完成，下一步：待开始→进行中，无需用户确认）
6. 更新 04-architecture.md（如有结构变化）
7. **自动执行 Git 提交**（创建回滚节点）
8. 返回菜单

```bash
# 1. 更新进度文件（步骤状态转换）
# 2. Git 提交
git add .
git commit -m "feat: step X - [步骤名称]"
```

**警告**: 如果不正确更新 05-progress.md，下次对话时 AI 会重新执行已完成的步骤！

### 始终遵守
- 一次只执行一个步骤
- ⚠️ **编译必须通过才能进行下一步，编译失败绝对不允许跳过**
- **每完成一个步骤，必须进行完全自动化测试（编译通过+自动生成测试+运行测试）**
- 编译是第一道关卡，编译失败不允许继续，不允许跳过
- 测试必须全部通过，失败则自动修复并重测，无需用户确认
- 测试通过后自动更新进度，自动执行Git提交，无需等待用户确认
- 每次操作后自动更新对应文档

---

## 🔄 文档自动更新矩阵

| 操作 | 触发条件 | 自动更新的文档 |
|-----|---------|---------------|
| **继续下一步** | 完成一个 Step | `05-progress.md`, `04-architecture.md` |
| **添加新功能** | 用户添加功能 | `02-product-requirements.md`, `03-implementation-plan.md`, `05-progress.md` |
| **修改需求** | 用户修改需求 | `02-product-requirements.md`, `03-implementation-plan.md`, `01-tech-stack.md`, `05-progress.md` |
| **代码重构** | 结构变化 | `04-architecture.md` |
| **新建项目** | 初始创建 | 全部 5 个文档 |

---

*本文档遵循 Vibe Coding 方法论 V1.2.2*
*项目地址: https://github.com/EnzeD/vibe-coding*
