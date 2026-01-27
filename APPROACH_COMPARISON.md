# 多实例启动方式对比

## 方式 1: 多个独立窗口 (MULTI_INSTANCE_FIX.py) ❌

```
┌─────────────────┐  ┌─────────────────┐
│ WezTerm 窗口 1  │  │ WezTerm 窗口 2  │
│                 │  │                 │
│ claude> ui      │  │ claude> coder   │
└─────────────────┘  └─────────────────┘
```

**问题:**
- ❌ 多个独立的 WezTerm 窗口
- ❌ 窗口之间无法通信
- ❌ `send` 命令不工作

**创建方式:**
```python
wezterm start -- claude --dangerously-skip-permissions
```

---

## 方式 2: 多个窗格在一个窗口 (START_MULTI_PANE.py) ✅

```
┌─────────────────────────────────────────┐
│ WezTerm 窗口                            │
├─────────────┬──────────────────────────────┤
│ Pane 1      │ Pane 2                       │
│ ui          │ coder                       │
│             │                              │
│ claude>     │ claude>                     │
└─────────────┴──────────────────────────────┘
```

**优点:**
- ✅ 一个 WezTerm 窗口
- ✅ 多个子窗格 (pane/sub-window)
- ✅ 窗格之间可以通信
- ✅ `send` 命令可以工作
- ✅ 每个窗格显示不同的实例

**创建方式:**
```python
wezterm cli split-pane --right --percent 50 -- claude --dangerously-skip-permissions
```

**术语说明:**
- **窗格 (Pane)** = 子窗口 (Sub-window)
- **窗口 (Window)** = WezTerm 主窗口

所以 START_MULTI_PANE.py 创建的 "多个窗格" 就是 "多个子窗口"

---

## 使用步骤

### 1. 打开 WezTerm

从开始菜单启动 WezTerm 或运行:
```bash
wezterm
```

### 2. 进入项目目录

```bash
cd E:\ai_project\claude-multi-starter
```

### 3. 启动多实例

```bash
python START_MULTI_PANE.py ui,coder
```

### 4. 确认继续

```
Continue? (y/n): y
```

### 5. 查看结果

你会看到:
- 一个 WezTerm 窗口
- 两个子窗格 (左右分割)
- 左边: ui 实例
- 右边: coder 实例

### 6. 测试通信

在 Windows 命令行 (新窗口) 中:
```bash
bin\send ui "设计登录页面"
bin\send coder "实现登录功能"
```

然后在 WezTerm 的对应窗格中查看结果

---

## 窗格切换

使用快捷键在不同窗格间切换:

```
Ctrl+Shift+→  切换到右边窗格
Ctrl+Shift+←  切换到左边窗格
Ctrl+Shift+↑  切换到上方窗格
Ctrl+Shift+↓  切换到下方窗格
```

---

## 验证成功

执行后检查:

- [ ] WezTerm 打开
- [ ] 只有一个 WezTerm 窗口
- [ ] 窗口内有多个子窗格
- [ ] 每个子窗格显示 "claude>"
- [ ] 子窗格标题显示实例名
- [ ] `bin\send ui "测试"` 可以发送消息
- [ ] `show-status.bat` 可以查看状态

---

## 总结

**START_MULTI_PANE.py 创建的 "窗格" 就是 "子窗口"**

这是正确的方式，因为:
1. ✅ 多个子窗格 = 多个子窗口
2. ✅ 它们可以互相通信
3. ✅ `send` 命令可以工作
4. ✅ 每个窗格运行独立的 Claude 实例

如果你想要多个独立的窗口（方式1），它们将无法通信。
