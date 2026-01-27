# C1 设计任务输出

## 📊 任务分析：简单计算器

### 需求理解
创建一个支持加减乘除的简单计算器，要求：
- 用户友好的界面
- 完整的错误处理
- 清晰的结果展示

### 🎨 界面设计

#### 布局方案
```
┌─────────────────────────────┐
│      简单计算器              │
├─────────────────────────────┤
│  第一个数字: [_______]       │
│                             │
│  操作符: [+] ▼               │
│           [-]                │
│           [*]                │
│           [/]                │
│                             │
│  第二个数字: [_______]       │
│                             │
│  [ 计算 ]  [ 清除 ]          │
│                             │
│  结果: [_______________]     │
└─────────────────────────────┘
```

### 🏗️ 技术架构

#### 文件结构
```
calculator.html
├── HTML 结构 (表单元素)
├── CSS 样式 (内嵌)
└── JavaScript 逻辑 (内嵌)
```

#### 核心功能
1. **输入验证**
   - 检查输入是否为有效数字
   - 防止空值输入

2. **计算逻辑**
   ```javascript
   function calculate() {
       const num1 = parseFloat(document.getElementById('num1').value);
       const num2 = parseFloat(document.getElementById('num2').value);
       const operator = document.getElementById('operator').value;
       let result;
       
       switch(operator) {
           case '+': result = num1 + num2; break;
           case '-': result = num1 - num2; break;
           case '*': result = num1 * num2; break;
           case '/': 
               if(num2 === 0) {
                   document.getElementById('result').value = '错误：不能除以零';
                   return;
               }
               result = num1 / num2; 
               break;
       }
       
       document.getElementById('result').value = result;
   }
   ```

3. **错误处理**
   - 除零错误
   - 无效输入（非数字）
   - 空值检查

### 📝 详细设计文档

#### HTML 元素
```html
<div class="calculator">
    <h2>简单计算器</h2>
    
    <div class="input-group">
        <label>第一个数字:</label>
        <input type="number" id="num1" placeholder="请输入数字" step="any">
    </div>
    
    <div class="input-group">
        <label>操作符:</label>
        <select id="operator">
            <option value="+">加 (+)</option>
            <option value="-">减 (-)</option>
            <option value="*">乘 (×)</option>
            <option value="/">除 (÷)</option>
        </select>
    </div>
    
    <div class="input-group">
        <label>第二个数字:</label>
        <input type="number" id="num2" placeholder="请输入数字" step="any">
    </div>
    
    <div class="button-group">
        <button onclick="calculate()">计算</button>
        <button onclick="clearAll()">清除</button>
    </div>
    
    <div class="result-group">
        <label>结果:</label>
        <input type="text" id="result" readonly>
    </div>
</div>
```

#### CSS 样式要点
- 居中布局
- 卡片式设计
- 响应式间距
- 清晰的视觉层次

### ✅ 设计完成

**下一步**: C2 (开发窗口) 请根据此设计实现代码

**设计文件**: `calculator.html`
**预计复杂度**: 简单
**预计时间**: 10-15 分钟

---
**设计完成时间**: 2025-01-27 20:40
**设计窗口**: C1
