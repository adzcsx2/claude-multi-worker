# Vibe Coding 项目指南

> 本目录包含 Vibe Coding 方法的完整文档，Claude 会优先读取这些文件来理解项目规范。

## 📁 文档结构

```
project-guide/
├── README.md           # 本文件，文档索引
├── PROJECT_GUIDE.md    # 核心规则与快速开始（必读）
├── TESTING_GUIDE.md    # 测试指南，四层测试验证详解
├── WORKFLOW_GUIDE.md   # 工作流程，详细操作说明
└── TEMPLATES.md        # 文档模板，Memory Bank 模板
```

## 📖 阅读顺序

### 新用户推荐阅读顺序：
1. **PROJECT_GUIDE.md** - 核心规则，了解基本流程
2. **WORKFLOW_GUIDE.md** - 详细操作流程
3. **TESTING_GUIDE.md** - 测试规范
4. **TEMPLATES.md** - 文档模板参考

### 快速查询：
- 需要查找测试规则 → `TESTING_GUIDE.md`
- 需要查找操作流程 → `WORKFLOW_GUIDE.md`
- 需要查找文档模板 → `TEMPLATES.md`
- 需要查找核心规则 → `PROJECT_GUIDE.md`

## 💡 Claude 使用说明

当你在 Claude Code 中打开项目时，Claude 会：

1. **自动检测** `memory-bank/` 目录是否存在
2. **优先读取** `project-guide/*.md` 文件
3. **根据项目状态** 选择对应的工作模式

### 关键规则摘要

```yaml
# 编译和测试强制规则
编译必须通过 → 才能进行下一步
测试必须通过 → 才能进行下一步
失败则自动修复 → 不允许跳过

# Android 四层测试验证
1. 编译验证（第一道关卡）
2. 单元测试
3. UI自动化测试
4. UI模拟测试（adb控制模拟器）
```

---

*本文档遵循 Vibe Coding 方法论 V1.2.2*
