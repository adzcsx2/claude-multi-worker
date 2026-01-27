# 🧪 CMS 测试指南

## ❌ 错误用法

```bash
python cms.bat tab    # ❌ 错误! .bat文件不能用python执行
```

## ✅ 正确用法

### 方式 1: 使用批处理文件 (推荐 - Windows)

```bash
cms.bat tab
cms.bat tab ui,coder,test
cms.bat pane ui,coder
cms.bat window ui,coder,test
```

### 方式 2: 直接使用 Python

```bash
python cms.py tab
python cms.py tab ui,coder,test
python cms.py pane ui,coder
python cms.py window ui,coder,test
```

### 方式 3: 直接使用启动脚本

```bash
python START_MULTI_TAB.py ui,coder,test
python START_MULTI_PANE.py ui,coder,test
python START_MULTI_WINDOW.py ui,coder,test
```

---

## 📋 测试步骤

### 前置检查

#### 1. 检查 Python

```bash
python --version
```

期望输出: `Python 3.x.x`

#### 2. 检查 WezTerm

```bash
wezterm --version
```

期望输出: `wezterm x.x.x`

如果 WezTerm 未安装:

- 下载: https://wezfurlong.org/wezterm/installation.html
- Windows: 下载 `.exe` 安装包并安装
- 确保添加到 PATH 环境变量

#### 3. 检查 Claude CLI

```bash
claude --version
```

---

## 🧪 测试 1: 帮助信息

```bash
# 测试 cms.py 帮助
python cms.py
```

**期望输出:**

```
CMS - Claude Multi Starter

Usage:
  python cms tab ui,coder,test       # 启动标签页模式
  python cms pane ui,coder,test      # 启动窗格模式
  python cms window ui,coder,test    # 启动多窗口模式
...
```

---

## 🧪 测试 2: 配置文件检查

```bash
# 检查配置文件是否存在
ls .cms_config\cms.config
```

如果不存在,创建默认配置:

```bash
mkdir .cms_config
```

创建 `.cms_config\cms.config`:

```json
{
  "providers": ["claude"],
  "claude": {
    "enabled": true,
    "instances": [
      { "id": "ui", "role": "UI/UX designer", "autostart": true },
      { "id": "coder", "role": "developer", "autostart": true },
      { "id": "test", "role": "QA engineer", "autostart": true }
    ]
  }
}
```

---

## 🧪 测试 3: 干运行测试 (不需要 WezTerm)

### 测试配置加载

```bash
python -c "import sys; sys.path.insert(0, 'lib'); from cms_start_config import load_start_config; from pathlib import Path; config = load_start_config(Path.cwd()); print('Instances:', [i.id for i in config.claude_config.instances])"
```

**期望输出:**

```
Instances: ['ui', 'coder', 'test', ...]
```

---

## 🧪 测试 4: Send 命令测试 (需要先启动实例)

### 手动创建测试映射文件

```bash
mkdir .cms_config
```

创建 `.cms_config\tab_mapping.json`:

```json
{
  "work_dir": "E:\\ai_project\\claude-multi-starter",
  "tabs": {
    "ui": { "pane_id": "0", "role": "UI designer" },
    "coder": { "pane_id": "1", "role": "developer" },
    "test": { "pane_id": "2", "role": "QA engineer" }
  },
  "created_at": 1706345678.123
}
```

### 测试 send 命令加载配置

```bash
python -c "import sys; sys.path.insert(0, 'bin'); exec(open('bin/send').read().replace('sys.exit(main())', 'config = load_config(); print(\"Loaded config:\", config)'))"
```

---

## 🧪 测试 5: 完整功能测试 (需要 WezTerm)

### 如果已安装 WezTerm:

#### 步骤 1: 打开 WezTerm

```bash
wezterm
```

#### 步骤 2: 在 WezTerm 中导航到项目

```bash
cd E:\ai_project\claude-multi-starter
```

#### 步骤 3: 测试标签页模式

```bash
# 方式 1
cms.bat tab ui,coder

# 方式 2
python cms.py tab ui,coder

# 方式 3
python START_MULTI_TAB.py ui,coder
```

#### 步骤 4: 检查映射文件

```bash
type .cms_config\tab_mapping.json
```

#### 步骤 5: 测试 send 命令

```bash
# 在另一个终端窗口
bin\send ui "你好"
bin\send coder "测试消息"
```

---

## 🧪 测试 6: 模拟测试 (无需 Claude)

创建模拟脚本 `test_mock.py`:

```python
#!/usr/bin/env python3
"""模拟测试 - 不需要实际的 Claude 或 WezTerm"""

import json
from pathlib import Path

# 创建测试配置
test_dir = Path(".cms_config_test")
test_dir.mkdir(exist_ok=True)

# 模拟标签页映射
mapping = {
    "work_dir": str(Path.cwd()),
    "tabs": {
        "ui": {"pane_id": "mock_pane_0", "role": "UI designer"},
        "coder": {"pane_id": "mock_pane_1", "role": "developer"},
        "test": {"pane_id": "mock_pane_2", "role": "QA engineer"}
    },
    "created_at": 1706345678.123
}

mapping_file = test_dir / "tab_mapping.json"
with open(mapping_file, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2)

print(f"✅ Created test mapping: {mapping_file}")
print(f"✅ Instances: {', '.join(mapping['tabs'].keys())}")
print("\n模拟 send 命令:")
for instance in mapping['tabs'].keys():
    print(f"  send {instance} \"测试消息\" -> pane_id: {mapping['tabs'][instance]['pane_id']}")
```

运行:

```bash
python test_mock.py
```

---

## ✅ 测试检查清单

- [ ] Python 已安装 (python --version)
- [ ] WezTerm 已安装 (wezterm --version)
- [ ] cms.py 帮助信息正常显示
- [ ] 配置文件加载正常
- [ ] send 命令能找到映射文件
- [ ] 标签页模式启动成功
- [ ] 映射文件正确生成
- [ ] send 命令能发送消息

---

## 🐛 常见问题

### Q1: "python cms.bat tab" 报语法错误

**A:** `.bat` 文件不能用 `python` 执行，应该:

```bash
cms.bat tab      # 或
python cms.py tab
```

### Q2: WezTerm 未找到

**A:**

1. 下载并安装 WezTerm
2. 确保 WezTerm 在 PATH 中
3. 重启终端

### Q3: send 命令找不到实例

**A:**

1. 确保已运行启动脚本
2. 检查 `.cms_config\tab_mapping.json` 是否存在
3. 检查实例名是否正确

### Q4: Claude 未安装

**A:** 测试功能不依赖 Claude，可以先测试配置和映射功能

---

## 📝 正确命令总结

```bash
# ✅ 正确
cms.bat tab
python cms.py tab
python START_MULTI_TAB.py ui,coder,test

# ❌ 错误
python cms.bat tab          # .bat不能用python执行
cms tab                     # Windows需要.bat后缀
./cms.bat tab               # Windows不需要./
```

---

**开始测试吧! 🧪**
