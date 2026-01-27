# 📘 CMS 完整使用指南

## 📖 目录

1. [快速开始](#快速开始)
2. [核心概念](#核心概念)
3. [基本命令](#基本命令)
4. [自动化模式](#自动化模式)
5. [实战示例](#实战示例)
6. [故障排除](#故障排除)
7. [最佳实践](#最佳实践)

---

## 🚀 快速开始

### 前置要求

1. **已安装 WezTerm**
   - 下载: https://wezfurlong.org/wezterm/installation.html
   - 验证: 打开命令行输入 `wezterm --version`

2. **已安装 Claude CLI**
   - 验证: 打开命令行输入 `claude --version`

3. **Python 3.8+**
   - 验证: 打开命令行输入 `python --version`

### 5 分钟上手

#### 步骤 1: 打开 WezTerm
```batch
wezterm
```

#### 步骤 2: 创建多个窗格
按 `Ctrl+Shift+T` 创建新窗格（建议创建 3 个）

#### 步骤 3: 在每个窗格启动 Claude
```bash
claude
```

#### 步骤 4: 使用 send 命令通信
```batch
# 在 Windows 命令行中
bin\send coder "请实现登录功能"
bin\send ui "设计登录页面"
bin\send test "测试登录功能"
```

---

## 🎯 核心概念

### 什么是 CMS？

**CMS (Claude Multi Starter)** 是一个多实例 Claude 协作工具，通过自动化流程让多个 Claude 实例协同工作。

### 三窗口模式

```
┌─────────┬─────────┬─────────┐
│   C1    │   C2    │   C3    │
│  设计   │  开发   │  测试   │
└─────────┴─────────┴─────────┘
```

- **C1 (设计窗口)**: 需求分析、架构设计、UI 设计
- **C2 (开发窗口)**: 代码实现、功能开发
- **C3 (测试窗口)**: 单元测试、集成测试、质量保证

### 工作流程

```
需求 → C1设计 → C2开发 → C3测试 → 完成
           ↑         ↓
           └── 失败反馈 ─┘
```

---

## 💻 基本命令

### 1. cms 主命令

#### 查看帮助
```batch
python cms --help
```

#### 启动 Claude 实例
```batch
# 启动所有配置的实例
python cms claude

# 启动特定实例
python cms claude:ui,coder,test

# 使用配置文件
python cms claude --config .cms_config/cms.config
```

#### 其他命令
```batch
# 查看版本
python cms version

# 终止会话
python cms kill

# 更新 CMS
python cms update
```

### 2. send 通信命令

#### 基本语法
```batch
bin\send <实例> <消息>
```

#### 示例
```batch
# 发送设计任务
bin\send ui "设计用户注册页面"

# 发送开发任务
bin\send coder "实现用户注册API"

# 发送测试任务
bin\send test "编写注册功能测试用例"
```

#### 支持的实例名称
根据你的 `.cms_config/cms.config` 配置：
- `default` - 默认实例
- `ui` - 设计实例
- `coder` - 开发实例
- `test` - 测试实例
- 或你自定义的实例名称

### 3. 状态监控命令

#### 查看实时状态
```batch
show-status.bat
```

#### 查看特定文件
```batch
# 查看自动化状态
type task-comms\automation-state.md

# 查看设计输出
type task-comms\from-c1-design.md

# 查看开发输出
type task-comms\from-c2-main.md

# 查看测试输出
type task-comms\from-c3-test.md
```

---

## 🤖 自动化模式

### 启动自动化

#### 方法 1: 使用启动器
```batch
test-automation.bat
```

#### 方法 2: 手动初始化

**在 C1 窗格 (WezTerm 窗格 1)**:
```
我是 C1 窗口。启动自动化模式。
```

**在 C2 窗格 (WezTerm 窗格 2)**:
```
我是 C2 窗口。启动自动化模式。
```

**在 C3 窗格 (WezTerm 窗格 3)**:
```
我是 C3 窗口。启动自动化模式。
```

### 自动化流程

#### 1. C1 执行设计任务
- 读取 `automation-state.md`
- 分析需求
- 创建设计方案
- 输出到 `from-c1-design.md`
- 提示: "请切换到 C2 窗口"

#### 2. C2 执行开发任务
- 读取 `from-c1-design.md`
- 实现代码
- 输出到项目文件
- 记录到 `from-c2-main.md`
- 提示: "请切换到 C3 窗口"

#### 3. C3 执行测试任务
- 读取项目文件
- 编写测试
- 输出到 `from-c3-test.md`
- 更新 `automation-state.md`
- 如果通过: 任务完成
- 如果失败: 回到 C2 修复

### 手动切换窗口

当看到提示时：
1. **点击 WezTerm 中的目标窗格**
2. **输入**: `继续`
3. **回车**

---

## 🎯 实战示例

### 示例 1: 创建登录功能

#### 步骤 1: 定义任务
```batch
# 编辑 automation-state.md
Current Step: STEP_INIT
Current Task: 创建用户登录功能
```

#### 步骤 2: 启动自动化
```batch
# 在 C1 窗格
我是 C1 窗口。启动自动化模式。
```

#### 步骤 3: 观察执行
- C1 设计登录界面和API
- C2 实现登录功能
- C3 编写测试用例

#### 步骤 4: 验证结果
```batch
# 检查输出文件
show-status.bat
```

### 示例 2: 使用 send 命令手动协作

#### 场景: 快速修复 Bug

```batch
# 1. 发送 bug 描述
bin\send coder "登录页面有 bug：点击登录按钮没有反应"

# 2. 发送修复建议
bin\send coder "请检查 JavaScript 的事件监听器"

# 3. 要求测试
bin\send test "请重新测试登录功能，特别是按钮点击事件"

# 4. 查看进度
type task-comms\from-c2-main.md
type task-comms\from-c3-test.md
```

### 示例 3: 创建完整功能模块

#### 功能: 用户个人中心

```batch
# 1. 设置任务
cat > task-comms\automation-state.md << EOF
Current Step: STEP_INIT
Current Window: C1
Current Task: 创建用户个人中心页面
功能需求:
- 显示用户信息
- 编辑个人资料
- 修改密码
EOF

# 2. 启动自动化（在 C1）
我是 C1 窗口。启动自动化模式。

# 3. 等待完成，检查结果
show-status.bat
```

---

## 🔧 配置文件

### cms.config 结构

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
      {
        "id": "default",
        "role": "general coordinator",
        "autostart": true
      },
      {
        "id": "ui",
        "role": "UI/UX designer",
        "autostart": true
      },
      {
        "id": "coder",
        "role": "developer",
        "autostart": true
      },
      {
        "id": "test",
        "role": "QA engineer",
        "autostart": true
      }
    ]
  }
}
```

### 添加新实例

```json
{
  "id": "reviewer",
  "role": "code reviewer",
  "autostart": false
}
```

然后使用:
```batch
bin\send reviewer "请审查 login.py 代码"
```

---

## 🛠️ 故障排除

### 问题 1: Claude 实例没有响应

**症状**: send 命令发送后没有反应

**解决**:
```batch
# 1. 检查实例是否运行
python cms claude

# 2. 检查窗格映射
type .cms_config\pane_mapping.json

# 3. 重新生成映射
python cms claude --remap
```

### 问题 2: 自动化模式不工作

**症状**: 输入"我是 C1 窗口"后没有反应

**解决**:
```batch
# 1. 检查状态文件
type task-comms\automation-state.md

# 2. 确认 Current Window 是 C1
# 如果不是，编辑文件改为:
Current Window: C1

# 3. 重新启动
我是 C1 窗口。启动自动化模式。
```

### 问题 3: WezTerm 窗格没有创建

**症状**: 运行 cms 后什么都没发生

**解决**:
```batch
# 1. 检查 WezTerm 是否安装
wezterm --version

# 2. 检查 WezTerm CLI
wezterm cli --help

# 3. 手动创建窗格
# 在 WezTerm 中按 Ctrl+Shift+T
```

### 问题 4: 找不到配置文件

**症状**: 提示找不到 cms.config

**解决**:
```batch
# 1. 检查配置文件
dir .cms_config

# 2. 如果不存在，创建默认配置
python cms init

# 3. 或手动创建
mkdir .cms_config
# 复制示例配置到该目录
```

### 问题 5: send 命令失败

**症状**: `bin\send coder "test"` 报错

**解决**:
```batch
# 1. 检查实例名称
type .cms_config\cms.config | findstr "id"

# 2. 使用正确的实例名称
bin\send <正确的实例名> "消息"

# 3. 检查 Python 路径
python --version
python bin\send coder "test"
```

---

## 💡 最佳实践

### 1. 任务管理

#### 使用清晰的任务描述
```batch
# ✅ 好的描述
bin\send coder "实现用户登录 API，包括邮箱验证和密码加密"

# ❌ 不好的描述
bin\send coder "做登录"
```

#### 分阶段发送任务
```batch
# 1. 先发送设计
bin\send ui "设计登录页面，包含邮箱和密码字段"

# 2. 等设计完成，发送开发
bin\send coder "根据 from-c1-design.md 实现登录功能"

# 3. 等开发完成，发送测试
bin\send test "测试登录功能的所有用例"
```

### 2. 状态追踪

#### 定期检查状态
```batch
# 每次切换窗口前
show-status.bat

# 或查看特定文件
type task-comms\automation-state.md
```

#### 保持状态文件更新
```batch
# 确保每个窗口都正确更新状态
Current Step: STEP_DEVELOP
Current Window: C2
```

### 3. 文档管理

#### 保存重要输出
```batch
# 定期备份通信文件
copy task-comms\from-*.md backup\
```

#### 使用版本控制
```batch
git add task-comms\*.md
git commit -m "完成任务 0: 计算器功能"
```

### 4. 效率优化

#### 使用快捷键
```
WezTerm:
  Ctrl+Shift+T  新建窗格
  Ctrl+Shift+X  关闭窗格
  Ctrl+Tab      切换窗格

Claude:
  Enter         发送消息
  Ctrl+C        中断生成
```

#### 批量操作
```batch
# 创建批量发送脚本
@echo off
bin\send ui "设计用户中心页面"
timeout /t 2 > nul
bin\send coder "实现用户中心功能"
timeout /t 2 > nul
bin\send test "测试用户中心"
```

---

## 📚 高级用法

### 1. 自定义工作流

#### 修改自动化步骤

编辑 `automation-state.md`:
```yaml
Step Definitions:
  STEP_ANALYZE: C1 分析需求
  STEP_DESIGN:  C1 设计方案
  STEP_REVIEW:  C2 评审设计
  STEP_DEVELOP: C2 实现功能
  STEP_TEST:    C3 测试功能
  STEP_DEPLOY:   C3 部署上线
```

### 2. 集成外部工具

#### 使用 Git 钩子
```batch
# .git/hooks/pre-commit
bin\send test "运行所有测试"
```

#### CI/CD 集成
```yaml
# .github/workflows/cms.yml
- name: Send to C3
  run: |
    bin/send test "运行 CI 测试"
```

### 3. 多项目管理

#### 项目特定配置
```batch
project1/
  .cms_config/cms.config
project2/
  .cms_config/cms.config
```

#### 切换项目
```batch
cd project1
python cms claude

cd project2
python cms claude
```

---

## 🎓 学习资源

### 文档
- `QUICK_START.md` - 快速开始
- `START_TEST.md` - 测试指南
- `TEST_REPORT.md` - 测试报告示例
- `project-guide/AUTOMATION_GUIDE.md` - 自动化详细指南

### 示例项目
- `calculator.html` - 完整的计算器实现
- `task-comms/from-*.md` - 各窗口输出示例

### 实用命令
```batch
# 测试安装
test-automation.bat

# 查看状态
show-status.bat

# 查看帮助
python cms --help
```

---

## 🆘 获取帮助

### 常见问题
查看本文档的 [故障排除](#故障排除) 部分

### 社区支持
- GitHub Issues
- 文档评论

### 更新日志
```batch
python cms version
```

---

## 🎉 总结

CMS 是一个强大的多实例协作工具，掌握以下要点即可高效使用：

1. **三个窗口**: C1设计 → C2开发 → C3测试
2. **send 命令**: 在窗口间传递任务
3. **自动化模式**: 无需手动切换，自动执行
4. **状态追踪**: 实时查看进度
5. **文档完整**: 每步都有记录

**开始使用**: `test-automation.bat`

**快速参考**: `QUICK_START.md`

**状态监控**: `show-status.bat`

---

*文档版本: CMS v5.1.0*
*更新日期: 2025-01-27*
