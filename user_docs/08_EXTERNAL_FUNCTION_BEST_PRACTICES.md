# 云器Lakehouse External Function Development Best Practices v1.0

**基于实际生产部署经验总结的最佳实践指南**

## 📋 目录

1. [核心原则](#核心原则)
2. [包结构要求](#包结构要求) 
3. [函数实现规范](#函数实现规范)
4. [部署最佳实践](#部署最佳实践)
5. [错误处理](#错误处理)
6. [性能优化](#性能优化)
7. [调试和测试](#调试和测试)
8. [常见陷阱](#常见陷阱)
9. [成功案例](#成功案例)

---

## 核心原则

### ✅ 必须遵循的规则（基于生产验证）

#### 1. **函数模式规范**
```python
# ✅ 正确的函数定义模式
@annotate("*->string")
class ai_your_function(object):  # 必须继承object
    
    def evaluate(self, param1, param2, api_key):  # 标准evaluate方法
        try:
            # 业务逻辑
            result = {"status": "success", "data": "..."}
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)
```

#### 2. **handler路径匹配**
```sql
-- 创建函数时，路径必须与ZIP包中的文件名完全匹配
CREATE EXTERNAL FUNCTION ai_text_summarize
AS 'ai_functions_complete.ai_text_summarize'  -- 文件名.类名
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_complete.zip'
CONNECTION aliyun_hz_cz_api_conn
WITH PROPERTIES ('remote.udf.api' = 'python3.mc.v0', 'remote.udf.protocol' = 'http.arrow.v0');
```

#### 3. **禁用的模式**
```python
# ❌ 错误 - 不要使用相对导入
from .common.base_llm import BaseLLMFunction

# ❌ 错误 - 不要定义handler属性
handler = "evaluate"

# ❌ 错误 - 不要继承其他类
class ai_text_summarize(BaseLLMFunction):

# ❌ 错误 - 不要在ZIP包根目录放__init__.py
```

#### 4. **智能降级机制**
```python
# ✅ 推荐的容错模式
try:
    import dashscope
    HAS_DASHSCOPE = True
except ImportError:
    HAS_DASHSCOPE = False

@annotate("*->string")
class ai_text_summarize(object):
    def evaluate(self, text, api_key):
        if not HAS_DASHSCOPE:
            # 降级模式 - 返回模拟结果
            return json.dumps({"summary": f"摘要：{text[:100]}...", "note": "模拟模式"}, ensure_ascii=False)
        
        # 正常模式 - 使用真实API
        dashscope.api_key = api_key
        # ... 实际API调用
```

---

## 包结构要求

### 生产环境推荐结构
```
clickzetta_ai_functions_complete.zip
└── ai_functions_complete.py    # 单文件包含所有30个函数
```

**重要提示**：
- ✅ **单文件模式**：最稳定，所有函数在一个文件中
- ✅ **极小体积**：6.3KB，快速上传和部署
- ✅ **无依赖冲突**：不包含任何第三方库
- ❌ **避免多文件结构**：减少路径匹配问题

### ZIP打包命令
```bash
# 在clickzetta_aisql目录下
zip -j /path/to/clickzetta_ai_functions_complete.zip ai_functions_complete.py

# 验证包内容
unzip -l clickzetta_ai_functions_complete.zip
```

---

## 函数实现规范

### 1. 标准函数模板
```python
from cz.udf import annotate
import json
import sys
from datetime import datetime

# 环境检测
try:
    import dashscope
    from http import HTTPStatus
    HAS_DASHSCOPE = True
except ImportError:
    HAS_DASHSCOPE = False
    class HTTPStatus:
        OK = 200

@annotate("*->string")
class ai_your_function(object):
    
    def evaluate(self, text, api_key, model_name="qwen-plus", **kwargs):
        """
        标准函数实现模板
        
        Args:
            text: 输入文本
            api_key: DashScope API密钥
            model_name: 模型名称
            **kwargs: 其他可选参数
            
        Returns:
            JSON格式的字符串结果
        """
        # 降级处理
        if not HAS_DASHSCOPE:
            result = {
                "processed_text": f"处理结果：{text}",
                "model": model_name,
                "note": "模拟模式 - dashscope库不可用"
            }
            return json.dumps(result, ensure_ascii=False)
        
        # 正常处理流程
        try:
            dashscope.api_key = api_key
            
            # 构建API调用
            messages = [
                {"role": "system", "content": "你是专业的AI助手"},
                {"role": "user", "content": text}
            ]
            
            # 流式调用模式（推荐）
            responses = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=True,
                result_format='message',
                temperature=0.7
            )
            
            # 收集响应
            full_content = ""
            for response in responses:
                if response.status_code == HTTPStatus.OK:
                    if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                        content = response.output.choices[0].message.content
                        if content:
                            full_content += content
                else:
                    return json.dumps({
                        "error": True,
                        "message": f"API调用失败: {response.message}"
                    }, ensure_ascii=False)
            
            # 构造结果
            result = {
                "processed_text": full_content,
                "input_length": len(text),
                "model": model_name,
                "timestamp": datetime.now().isoformat()
            }
            
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                "error": True,
                "message": str(e),
                "function": "ai_your_function"
            }, ensure_ascii=False)
```

### 2. 参数验证模板
```python
def evaluate(self, text, api_key, model_name="qwen-plus"):
    # 参数验证
    if not text or not text.strip():
        return json.dumps({"error": True, "message": "text参数不能为空"}, ensure_ascii=False)
    
    if not api_key:
        return json.dumps({"error": True, "message": "api_key参数不能为空"}, ensure_ascii=False)
    
    # 继续处理...
```

---

## 部署最佳实践

### 1. 环境准备清单
```sql
-- ✅ 检查Volume状态
LIST @external_functions_prod;

-- ✅ 验证API连接
-- SHOW CONNECTIONS LIKE '%api%';

-- ✅ 检查权限
-- SHOW GRANTS;
```

### 2. 标准部署流程
```sql
-- 步骤1: 上传函数包
PUT '/path/to/clickzetta_ai_functions_complete.zip' 
TO VOLUME external_functions_prod FILE 'clickzetta_ai_functions_complete.zip';

-- 步骤2: 验证上传
LIST @external_functions_prod;

-- 步骤3: 创建函数（使用统一模板）
CREATE EXTERNAL FUNCTION ai_function_name
AS 'ai_functions_complete.class_name'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_complete.zip'
CONNECTION aliyun_hz_cz_api_conn
WITH PROPERTIES ('remote.udf.api' = 'python3.mc.v0', 'remote.udf.protocol' = 'http.arrow.v0');

-- 步骤4: 验证创建
SHOW FUNCTIONS LIKE 'ai_function_name';

-- 步骤5: 功能测试
SELECT ai_function_name('测试输入', 'your-api-key') as test_result;
```

### 3. 批量部署策略
```sql
-- 使用事务确保一致性
BEGIN;

-- 创建多个函数...
CREATE EXTERNAL FUNCTION ai_text_summarize AS ...;
CREATE EXTERNAL FUNCTION ai_text_translate AS ...;
-- ... 更多函数

-- 验证所有函数创建成功
SELECT COUNT(*) as created_functions FROM information_schema.functions 
WHERE function_name LIKE 'ai_%';

-- 如果数量正确则提交，否则回滚
COMMIT; -- 或 ROLLBACK;
```

---

## 错误处理

### 1. 完整错误处理模式
```python
def evaluate(self, text, api_key):
    try:
        # 参数验证
        if not text:
            raise ValueError("text参数不能为空")
        if not api_key:
            raise ValueError("api_key参数不能为空")
        
        # API调用
        result = self._call_api(text, api_key)
        
        # 结果验证
        if not result:
            raise RuntimeError("API返回空结果")
        
        return json.dumps({"status": "success", "data": result}, ensure_ascii=False)
        
    except ValueError as e:
        return json.dumps({"error": True, "type": "parameter_error", "message": str(e)}, ensure_ascii=False)
    except ConnectionError as e:
        return json.dumps({"error": True, "type": "network_error", "message": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": True, "type": "unknown_error", "message": str(e)}, ensure_ascii=False)
```

### 2. 用户友好的错误处理
```sql
-- SQL中的错误处理示例
SELECT 
  document_id,
  CASE 
    WHEN JSON_EXTRACT(ai_result, '$.error') = true THEN 
      CASE 
        WHEN JSON_EXTRACT(ai_result, '$.type') = 'parameter_error' THEN '参数错误'
        WHEN JSON_EXTRACT(ai_result, '$.type') = 'network_error' THEN '网络错误'
        ELSE '处理失败'
      END
    WHEN JSON_EXTRACT(ai_result, '$.note') LIKE '%模拟模式%' THEN '模拟模式运行'
    ELSE JSON_EXTRACT(ai_result, '$.data')
  END as processed_result
FROM (
  SELECT 
    document_id,
    ai_text_summarize(content, 'your-api-key') as ai_result
  FROM documents
) t;
```

---

## 性能优化

### 1. API调用优化
```python
# ✅ 使用合适的模型
model_recommendations = {
    "fast": "qwen-turbo",      # 快速响应
    "balanced": "qwen-plus",   # 平衡性能
    "quality": "qwen-max",     # 最高质量
    "long_text": "qwen-long"   # 长文本
}

# ✅ 批量处理
def evaluate(self, texts_json, api_key):
    texts = json.loads(texts_json)
    results = []
    
    for text in texts:
        result = self._process_single(text, api_key)
        results.append(result)
    
    return json.dumps({"batch_results": results}, ensure_ascii=False)
```

### 2. 成本优化
```python
# 智能模型选择
def evaluate(self, text, api_key):
    # 根据文本长度选择模型
    if len(text) > 10000:
        model = "qwen-long"
    elif len(text) > 2000:
        model = "qwen-plus"
    else:
        model = "qwen-turbo"
    
    return self._call_api(text, api_key, model)
```

---

## 调试和测试

### 1. 本地测试模式
```python
if __name__ == '__main__':
    # 本地测试代码
    func = ai_text_summarize()
    result = func.evaluate("测试文本", "test-key")
    print(result)
```

### 2. 调试SQL
```sql
-- 调试函数创建
SHOW FUNCTIONS LIKE 'ai_%';

-- 调试函数调用
SELECT ai_text_summarize('简单测试', 'test-key') as debug_result;

-- 调试错误信息
SELECT 
  JSON_EXTRACT(ai_text_summarize('', ''), '$.error') as has_error,
  JSON_EXTRACT(ai_text_summarize('', ''), '$.message') as error_message;
```

### 3. 性能测试
```sql
-- 响应时间测试
SELECT 
  COUNT(*) as processed_count,
  AVG(LENGTH(ai_text_summarize(content, 'your-api-key'))) as avg_result_length
FROM (
  SELECT content FROM documents LIMIT 10
) t;
```

---

## 常见陷阱

### ❌ 陷阱1: handler路径不匹配
```
错误: no function found for handler text_functions.ai_text_summarize
原因: ZIP包中文件名是ai_functions_complete.py，但handler用的是text_functions
解决: 确保handler路径与实际文件名匹配
```

### ❌ 陷阱2: 依赖库打包
```
错误: 包大小过大，部署缓慢
原因: 将dashscope等库打包到ZIP中
解决: 使用智能降级，依赖环境库或模拟模式
```

### ❌ 陷阱3: 相对导入
```python
# ❌ 错误
from .common import utils

# ✅ 正确
try:
    from common import utils
except ImportError:
    # 降级处理
    pass
```

### ❌ 陷阱4: 不完整的JSON响应
```python
# ❌ 错误
return "处理完成"

# ✅ 正确
return json.dumps({"result": "处理完成"}, ensure_ascii=False)
```

---

## 成功案例

### 案例1: bailian_llm.py 成功模式
```python
# 这是验证有效的成功模式
@annotate("*->string")
class ai_industry_classification(object):
    def evaluate(self, text, prompt, api_key, model_name, temperature=0.7, enable_search=False):
        dashscope.api_key = api_key
        messages = [{"role": "system", "content": prompt}, {"role": "user", "content": text}]
        
        try:
            responses = dashscope.Generation.call(
                model=model_name, messages=messages, stream=True,
                result_format='message', temperature=temperature, enable_search=enable_search
            )
            
            full_content = ""
            for response in responses:
                if response.status_code == HTTPStatus.OK:
                    if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                        content = response.output.choices[0].message.content
                        if content: full_content += content
                else:
                    return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            # JSON解析和结果处理
            try:
                result = json.loads(full_content)
            except:
                result = {"一级行业": "未知", "二级行业": "未知", "原始内容": full_content}
            
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)
```

### 案例2: 成功的部署配置
```sql
-- 经过生产验证的配置
CREATE EXTERNAL VOLUME external_functions_prod
LOCATION 'oss://mcp-data-hangzhou/function_packages'
USING CONNECTION quick_start.aliyun_oss_hangzhou_internal_conn
DIRECTORY = (enable=true, auto_refresh=true)
RECURSIVE=true;

CREATE EXTERNAL FUNCTION ai_text_summarize
AS 'ai_functions_complete.ai_text_summarize'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_complete.zip'
CONNECTION aliyun_hz_cz_api_conn
WITH PROPERTIES ('remote.udf.api' = 'python3.mc.v0', 'remote.udf.protocol' = 'http.arrow.v0');
```

---

## 总结

### 🎯 成功要素
1. ✅ **遵循验证的模式** - 基于bailian_llm.py的成功经验
2. ✅ **保持包结构简单** - 单文件，无依赖
3. ✅ **完整的错误处理** - 降级机制和异常捕获
4. ✅ **精确的路径匹配** - handler路径必须准确
5. ✅ **智能的环境适配** - 模拟模式确保兼容性

### 🚀 快速成功路径
1. 复制成功的函数模板
2. 使用单文件包结构
3. 遵循标准部署流程
4. 进行完整的测试验证

**遵循这些实践，确保你的云器Lakehouse外部函数开发和部署成功！** 🎉