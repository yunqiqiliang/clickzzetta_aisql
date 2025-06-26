# ClickZetta外部函数调试解决方案

## 🔍 问题根因分析

根据对成功的`bailian_llm.py`模式的分析，发现了几个关键问题：

### 1. **ZIP包依赖污染问题**
**问题**: 之前的ZIP包包含了大量不必要的依赖库
```
❌ 错误的包结构:
clickzetta_aisql/
├── aiohttp/           # 不需要
├── dashscope/         # 不需要  
├── requests/          # 不需要
├── 其他40+个依赖库/     # 不需要
└── text_functions.py  # 实际需要的文件
```

**解决方案**: 创建最小化ZIP包，只包含必要的Python文件
```
✅ 正确的包结构:
test_function.py       # 单文件，无依赖
```

### 2. **函数定义模式问题**
**问题**: 使用了复杂的helper方法和相对导入

**解决方案**: 遵循成功的`bailian_llm.py`模式:
- ✅ 直接继承`object`
- ✅ 使用`@annotate("*->string")`装饰器
- ✅ 所有API调用逻辑都在`evaluate`方法内
- ✅ 无相对导入，无helper方法

### 3. **依赖处理问题**
**问题**: 尝试在ZIP包中包含完整的dashscope库

**解决方案**: 
- 对于测试：使用模拟API调用
- 对于生产：依赖UDF服务器环境已安装的库

## 🧪 调试测试包

已创建三个不同复杂度的测试ZIP包：

### 测试包1: 纯本地函数 (`test_echo.zip`)
```python
@annotate("*->string")
class ai_simple_echo(object):
    def evaluate(self, text, prefix="回显"):
        result = {
            "input_text": text,
            "output_text": f"{prefix}: {text}",
            "function_name": "ai_simple_echo",
            "success": True
        }
        return json.dumps(result, ensure_ascii=False)
```

**测试命令**:
```sql
-- 上传包
PUT '/Users/liangmo/Downloads/test_echo.zip' TO VOLUME user_files;

-- 创建函数
CREATE EXTERNAL FUNCTION ai_simple_echo AS 'minimal_test.ai_simple_echo' 
USING ARCHIVE 'volume://user_files/test_echo.zip' 
CONNECTION aliyun_hz_cz_api_conn;

-- 测试调用
SELECT ai_simple_echo('测试文本', '前缀');
```

### 测试包2: 模拟DashScope (`test_dashscope_mock.zip`)
```python
@annotate("*->string")
class ai_text_summarize_mock(object):
    def evaluate(self, text, api_key, model_name="qwen-plus", max_length=200):
        # 完全基于bailian_llm.py的成功模式
        # 包含完整的错误处理和响应解析逻辑
        # 但使用模拟的API响应，不需要真实网络调用
```

### 测试包3: 简化版本 (`simple_function_only.zip`)
原始的`simple_text_function.py`，但在清洁的ZIP包中

## 🎯 推荐的调试步骤

### 步骤1: 验证最基础的功能
1. 使用`test_echo.zip`测试ZIP包解析和函数加载机制
2. 如果成功，说明基础架构正常

### 步骤2: 验证复杂函数模式
1. 使用`test_dashscope_mock.zip`测试复杂的函数逻辑
2. 验证流式处理、错误处理等机制

### 步骤3: 迁移到真实API
1. 如果前两步成功，将模拟逻辑替换为真实的dashscope调用
2. 确保UDF服务器环境中有dashscope库

## 🔧 可能的解决方案

### 方案A: 环境依赖方式
```python
# 假设UDF服务器环境已安装dashscope
import dashscope  # 直接导入，不放在ZIP包中

@annotate("*->string")
class ai_text_summarize(object):
    def evaluate(self, text, api_key, model_name="qwen-plus"):
        dashscope.api_key = api_key
        # 使用真实的dashscope调用
```

### 方案B: 自包含模拟方式
```python
# 在ZIP包中包含模拟的dashscope实现
# 用于测试和演示，不需要真实API

class MockDashScope:
    # 模拟实现
    
@annotate("*->string")
class ai_text_summarize(object):
    def evaluate(self, text, api_key):
        # 使用模拟实现
```

### 方案C: HTTP请求方式
```python
import urllib.request
import json

@annotate("*->string") 
class ai_text_summarize(object):
    def evaluate(self, text, api_key):
        # 使用标准库直接发HTTP请求到DashScope API
        # 不依赖dashscope SDK
```

## 📋 调试检查清单

### ✅ ZIP包检查
- [ ] ZIP包大小 < 10MB
- [ ] 只包含必要的.py文件
- [ ] 无__pycache__目录
- [ ] 无.dist-info目录
- [ ] 函数定义符合成功模式

### ✅ 函数定义检查
- [ ] 使用`@annotate("*->string")`
- [ ] 类继承`object`
- [ ] 有`evaluate`方法
- [ ] 返回JSON字符串
- [ ] 无相对导入

### ✅ 错误处理检查
- [ ] 有try-catch包装
- [ ] 返回结构化错误信息
- [ ] 使用`json.dumps(ensure_ascii=False)`

## 🚀 下一步操作建议

1. **立即测试**: 使用`test_echo.zip`验证基础功能
2. **逐步升级**: 如果基础测试通过，再测试复杂版本
3. **环境确认**: 联系运维确认UDF服务器中可用的Python库
4. **文档完善**: 根据测试结果更新最佳实践文档

## 📞 获取帮助

如果测试仍然失败，请提供：
1. 具体的错误消息
2. 使用的ZIP包名称
3. 完整的CREATE EXTERNAL FUNCTION语句
4. ClickZetta版本信息

---
**创建时间**: 2025-06-14  
**版本**: v1.0  
**状态**: 待验证