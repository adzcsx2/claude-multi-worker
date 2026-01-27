# 🎉 新功能:标签页模式

## 现在支持三种启动模式!

### 1. 标签页模式 (🏆 推荐)

在一个 WezTerm 窗口中创建多个标签页

```bash
python cms.bat tab ui,coder,test
```

**优点:**

- ✅ 紧凑,节省空间
- ✅ 快速切换 (Ctrl+Tab)
- ✅ 更符合使用习惯

### 2. 窗格模式

在一个窗口中分割多个窗格

```bash
python cms.bat pane ui,coder,test
```

**优点:**

- ✅ 可同时看到多个实例
- ✅ 适合大显示器

### 3. 多窗口模式

创建多个独立窗口

```bash
python cms.bat window ui,coder,test
```

**优点:**

- ✅ 完全独立
- ✅ 适合多显示器

---

## 📡 实例间通信

所有模式都支持 `send` 命令:

```bash
bin\send ui "设计登录页面"
bin\send coder "实现登录功能"
bin\send test "测试登录功能"
```

**关键特性:**

- ✅ 消息自动发送到对应的 Claude 实例
- ✅ **自动提交** (就像按了回车)
- ✅ Claude 立即处理消息

---

## 🚀 快速开始

### 最简单的方式

```bash
# 1. 启动标签页模式 (推荐)
python cms.bat tab

# 2. 使用 send 命令通信
bin\send ui "你好,请设计一个登录页面"
bin\send coder "请实现用户认证功能"
bin\send test "请测试登录流程"
```

---

## 📚 详细文档

- **快速开始:** [QUICK_START_TAB.md](QUICK_START_TAB.md)
- **实现总结:** [IMPLEMENTATION_SUMMARY_TAB.md](IMPLEMENTATION_SUMMARY_TAB.md)
- **完整指南:** [USER_GUIDE.md](USER_GUIDE.md)

---

## 💡 工作流示例

开发一个用户登录功能:

```bash
# 1. 启动
python cms.bat tab ui,coder,test

# 2. 分配任务
bin\send ui "设计现代化的登录页面"
bin\send coder "实现JWT认证登录API"
bin\send test "编写登录功能测试用例"

# 3. 协作
bin\send coder "UI已完成,查看 designs/login.html"
bin\send test "API已完成,开始测试"
bin\send coder "测试发现问题:密码验证缺失"
```

---

**开始使用吧! 🎉**
