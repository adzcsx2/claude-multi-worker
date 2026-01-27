# CMS 系统验证清单

## 📋 验证步骤

### 阶段 1: 环境检查

- [ ] WezTerm 已安装
  ```bash
  wezterm --version
  ```

- [ ] Python 已安装
  ```bash
  python --version
  ```

- [ ] Claude CLI 已安装
  ```bash
  claude --version
  ```

- [ ] 在项目目录中
  ```bash
  cd E:\ai_project\claude-multi-starter
  ```

---

### 阶段 2: 配置文件检查

- [ ] `.cms_config` 目录存在
  ```bash
  ls .cms_config
  ```

- [ ] `cms.config` 文件存在
  ```bash
  ls .cms_config/cms.config
  ```

- [ ] 配置文件可读取
  ```bash
  python -c "from lib.cms_start_config import load_start_config; print('OK')"
  ```

- [ ] 实例配置正确
  ```bash
  # 应该显示: 5 instances found
  ```

---

### 阶段 3: 模块导入检查

- [ ] cms_config 模块
  ```bash
  python -c "from lib.cms_config import *; print('OK')"
  ```

- [ ] cms_protocol 模块
  ```bash
  python -c "from lib.cms_protocol import *; print('OK')"
  ```

- [ ] cms_start_config 模块
  ```bash
  python -c "from lib.cms_start_config import *; print('OK')"
  ```

- [ ] providers 模块
  ```bash
  python -c "from lib.providers import *; print('OK')"
  ```

---

### 阶段 4: 启动器检查

- [ ] START_MULTI_PANE.py 存在
  ```bash
  ls START_MULTI_PANE.py
  ```

- [ ] 启动器可以运行
  ```bash
  python START_MULTI_PANE.py --help
  ```

- [ ] WezTerm 环境检测正常
  ```bash
  # 在 WezTerm 中运行
  python START_MULTI_PANE.py ui,coder
  # 应该显示: [+] WezTerm: ...
  ```

---

### 阶段 5: 多实例启动测试

在 WezTerm 中执行:

- [ ] 打开 WezTerm
  ```bash
  wezterm
  ```

- [ ] 进入项目目录
  ```bash
  cd E:\ai_project\claude-multi-starter
  ```

- [ ] 启动 2 个实例
  ```bash
  python START_MULTI_PANE.py ui,coder
  ```

- [ ] 确认继续
  ```
  Continue? (y/n): y
  ```

- [ ] 验证结果:
  - [ ] 只有一个 WezTerm 窗口
  - [ ] 窗口内有 2 个子窗格
  - [ ] 左边窗格显示: ui
  - [ ] 右边窗格显示: coder
  - [ ] 每个窗格显示 `claude>` 提示符

---

### 阶段 6: 通信功能测试

- [ ] pane_mapping.json 已创建
  ```bash
  ls .cms_config/pane_mapping.json
  ```

- [ ] send 命令存在
  ```bash
  ls bin/send
  ```

- [ ] 测试发送消息到 ui
  ```bash
  bin\send ui "测试消息到 ui"
  ```

- [ ] 测试发送消息到 coder
  ```bash
  bin\send coder "测试消息到 coder"
  ```

- [ ] 在 WezTerm 窗格中查看消息
  - 使用 Ctrl+Shift+方向键切换窗格
  - [ ] ui 窗格收到消息
  - [ ] coder 窗格收到消息

---

### 阶段 7: 窗格操作测试

- [ ] 切换到右边窗格
  ```
  Ctrl+Shift+→
  ```

- [ ] 切换到左边窗格
  ```
  Ctrl+Shift+←
  ```

- [ ] 可以在两个窗格间自由切换

---

### 阶段 8: 3 实例测试

- [ ] 启动 3 个实例
  ```bash
  python START_MULTI_PANE.py ui,coder,test
  ```

- [ ] 验证布局:
  - [ ] ui 窗格 (左上)
  - [ ] coder 窗格 (右上)
  - [ ] test 窗格 (下方)

- [ ] 测试通信:
  ```bash
  bin\send ui "测试消息"
  bin\send coder "测试消息"
  bin\send test "测试消息"
  ```

---

### 阶段 9: 自动化工作流测试

- [ ] task-comms 目录存在
  ```bash
  ls task-comms
  ```

- [ ] automation-state.md 存在
  ```bash
  ls task-comms/automation-state.md
  ```

- [ ] 可以读取状态文件
  ```bash
  type task-comms\automation-state.md
  ```

---

### 阶段 10: 工具脚本测试

- [ ] show-status.bat 可以运行
  ```bash
  show-status.bat
  ```

- [ ] test_communication.bat 存在
  ```bash
  ls test_communication.bat
  ```

- [ ] START_HERE.bat 可以运行
  ```bash
  START_HERE.bat
  ```

---

## 🎯 快速验证命令

### 一键测试脚本

```bash
# 环境检查
wezterm --version && python --version && claude --version

# 配置检查
ls .cms_config/cms.config

# 模块测试
python -c "from lib.cms_start_config import load_start_config; print('[+] Config OK')"

# 启动测试 (在 WezTerm 中)
python START_MULTI_PANE.py ui,coder
```

---

## ✅ 成功标志

全部验证完成后，你应该看到:

1. ✅ WezTerm 正常运行
2. ✅ 可以启动多个实例
3. ✅ 实例在同一个窗口的不同窗格中
4. ✅ 每个窗格运行独立的 Claude
5. ✅ 可以使用 send 命令通信
6. ✅ 可以使用快捷键切换窗格
7. ✅ 状态文件正常工作
8. ✅ 所有工具脚本可运行

---

## 🆘 常见问题

### 问题: "Not running in WezTerm"

**解决**: 确保在 WezTerm 中运行，不是普通命令行

### 问题: "找不到配置文件"

**解决**: 检查 `.cms_config/cms.config` 是否存在

### 问题: "无法发送消息"

**解决**: 检查 `.cms_config/pane_mapping.json` 是否已创建

### 问题: "窗格无法切换"

**解决**: 确保使用 Ctrl+Shift+方向键 (不是 Ctrl+方向键)

---

## 📞 获取帮助

如果遇到问题:

1. 查看 `README_USAGE.md` - 完整使用指南
2. 查看 `APPROACH_COMPARISON.md` - 理解多实例方式
3. 运行 `START_HERE.bat` - 快速开始向导
4. 查看 `IMPLEMENTATION_SUMMARY.md` - 实施总结

---

**验证完成后，系统就可以正常使用了！** 🎉
