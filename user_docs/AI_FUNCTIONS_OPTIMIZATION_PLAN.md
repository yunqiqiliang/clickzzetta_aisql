# AI外部函数文本重复问题优化方案

## 问题诊断

### 根本原因分析

经过代码审查，发现问题的根本原因是：

1. **流式API调用的副作用**：DashScope API在流式调用模式下，可能会返回累积的响应内容，而不是增量内容。

2. **缺少输出验证**：原代码没有对AI生成的内容进行长度和质量验证。

3. **缺少重复检测机制**：没有检测和处理异常的重复内容。

### 关键问题代码
```python
# 原代码中的流式调用
responses = dashscope.Generation.call(
    model=model_name, 
    messages=messages, 
    stream=True,  # 这里使用了流式调用
    result_format='message'
)

# 累积响应
full_content = ""
for response in responses:
    content = response.output.choices[0].message.content
    if content: full_content += content  # 可能累积了重复内容
```

## 优化方案

### 1. 立即修复措施

#### 1.1 切换到非流式调用
```python
# 修改为非流式调用
response = dashscope.Generation.call(
    model=model_name, 
    messages=messages, 
    stream=False,  # 关键修改
    result_format='message',
    max_tokens=500  # 添加输出长度限制
)
```

#### 1.2 添加输出验证
```python
def validate_output(output, input_text, max_ratio=2.0):
    """验证输出是否合理"""
    # 检查输出长度
    if len(output) > len(input_text) * max_ratio:
        return False, "Output too long"
    
    # 检查重复内容
    if detect_repetition(output):
        return False, "Repetitive content detected"
    
    return True, "Valid"
```

#### 1.3 实现重复检测
```python
def detect_repetition(text, threshold=0.5):
    """检测文本中的重复模式"""
    if len(text) < 50:
        return False
    
    # 检查子串重复
    quarter_len = len(text) // 4
    prefix = text[:quarter_len]
    
    # 如果前1/4在全文中出现超过2次，认为有重复
    if text.count(prefix) > 2:
        return True
    
    # 检查连续重复词
    words = text.split()
    for i in range(len(words) - 10):
        pattern = ' '.join(words[i:i+5])
        if text.count(pattern) > 2:
            return True
    
    return False
```

### 2. 保护机制

#### 2.1 输入保护
```python
# 限制输入长度
MAX_INPUT_LENGTH = 10000
if len(text) > MAX_INPUT_LENGTH:
    text = text[:MAX_INPUT_LENGTH]

# 输入验证
if not text or not isinstance(text, str):
    return error_response("Invalid input")
```

#### 2.2 输出保护
```python
# 输出长度限制
MAX_OUTPUT_RATIO = 2.0  # 输出不超过输入的2倍
if len(output) > len(input_text) * MAX_OUTPUT_RATIO:
    output = output[:int(len(input_text) * MAX_OUTPUT_RATIO)]

# 智能截断
def smart_truncate(text, max_length):
    """在句子边界截断文本"""
    if len(text) <= max_length:
        return text
    
    # 找到最后一个完整句子
    for sep in ['。', '！', '？', '.', '!', '?']:
        pos = text[:max_length].rfind(sep)
        if pos > 0:
            return text[:pos + 1]
    
    return text[:max_length] + "..."
```

#### 2.3 错误恢复机制
```python
def safe_ai_call(func, *args, max_retries=3):
    """带重试和降级的安全调用"""
    for attempt in range(max_retries):
        try:
            result = func(*args)
            
            # 验证结果
            if validate_result(result):
                return result
            
            # 如果结果无效，尝试修复
            if attempt < max_retries - 1:
                args = modify_parameters(args)  # 调整参数
                continue
            
        except Exception as e:
            if attempt == max_retries - 1:
                return fallback_response(e)
    
    return error_response("Max retries exceeded")
```

### 3. 配置优化

#### 3.1 模型参数调整
```python
# 为不同任务优化参数
TASK_CONFIGS = {
    "summarize": {
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9
    },
    "sentiment": {
        "temperature": 0.1,  # 更低的温度，更确定的输出
        "max_tokens": 200,
        "top_p": 0.95
    }
}
```

#### 3.2 Prompt优化
```python
# 更明确的指令，避免重复
OPTIMIZED_PROMPTS = {
    "summarize": "请提供一个简洁的摘要，不要重复原文内容。摘要应该：\n1. 不超过{max_length}字\n2. 包含主要观点\n3. 使用原创表述",
    
    "sentiment": "分析情感并返回JSON格式。要求：\n1. 只返回JSON，无额外内容\n2. 不要重复输入文本\n3. 格式：{sentiment, confidence, emotions}"
}
```

### 4. 监控和日志

#### 4.1 性能监控
```python
import time
import logging

def monitor_performance(func):
    """监控函数性能"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        input_length = len(str(args[0])) if args else 0
        
        try:
            result = func(*args, **kwargs)
            output_length = len(str(result))
            
            # 记录性能指标
            metrics = {
                "function": func.__name__,
                "input_length": input_length,
                "output_length": output_length,
                "ratio": output_length / input_length if input_length > 0 else 0,
                "duration": time.time() - start_time,
                "status": "success"
            }
            
            # 异常检测
            if metrics["ratio"] > 5:
                logging.warning(f"Abnormal output ratio: {metrics}")
            
            return result
            
        except Exception as e:
            logging.error(f"Function failed: {func.__name__}, error: {e}")
            raise
    
    return wrapper
```

#### 4.2 质量检查
```python
def quality_check(text):
    """检查生成文本的质量"""
    checks = {
        "no_repetition": not detect_repetition(text),
        "reasonable_length": len(text) < 10000,
        "valid_json": is_valid_json(text) if text.startswith('{') else True,
        "no_garbage": not contains_garbage(text)
    }
    
    return all(checks.values()), checks
```

### 5. 部署计划

#### 第一阶段：紧急修复（1-2天）
1. 将`stream=True`改为`stream=False`
2. 添加基本的输出长度限制
3. 部署`ai_functions_fixed.py`

#### 第二阶段：增强保护（3-5天）
1. 实现完整的重复检测算法
2. 添加智能截断功能
3. 优化prompt模板

#### 第三阶段：长期优化（1-2周）
1. 建立性能监控系统
2. 收集异常案例库
3. 持续优化模型参数

### 6. 测试验证

#### 6.1 单元测试
```python
def test_no_repetition():
    """测试无重复输出"""
    test_cases = [
        "简短文本",
        "这是一段较长的测试文本，包含多个句子。用于验证摘要功能。",
        "A" * 1000  # 极端情况
    ]
    
    for text in test_cases:
        result = ai_text_summarize().evaluate(text, api_key)
        data = json.loads(result)
        
        # 验证无重复
        assert not detect_repetition(data.get("summary", ""))
        
        # 验证长度合理
        assert len(data.get("summary", "")) <= len(text) * 2
```

#### 6.2 集成测试
```sql
-- 批量测试验证
WITH test_data AS (
    SELECT 
        text,
        mcp_demo.ai_text_summarize(text, 'api-key') as result
    FROM test_texts
)
SELECT 
    text,
    result,
    LENGTH(text) as input_len,
    LENGTH(JSON_EXTRACT(result, '$.summary')) as output_len,
    LENGTH(JSON_EXTRACT(result, '$.summary')) / LENGTH(text) as ratio
FROM test_data
WHERE LENGTH(JSON_EXTRACT(result, '$.summary')) / LENGTH(text) > 2;
```

### 7. 回滚方案

如果新版本出现问题，可以快速回滚：

1. 保留原始`ai_functions_complete.py`作为备份
2. 准备回滚脚本
3. 建立版本切换机制

```bash
# 回滚命令
cp ai_functions_complete.py.backup ai_functions_complete.py
zip -r clickzetta_ai_functions_full.zip ai_functions_complete.py
# 重新部署
```

## 总结

这个优化方案通过以下措施解决文本重复问题：

1. **根本解决**：从流式调用改为非流式调用
2. **防御措施**：添加多层输出验证和保护
3. **智能处理**：实现重复检测和智能截断
4. **持续改进**：建立监控和优化机制

预期效果：
- 完全消除文本重复现象
- 输出质量显著提升
- 系统稳定性增强
- 用户体验改善