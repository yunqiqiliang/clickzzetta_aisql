# ClickZetta AI SQL Functions 开发指南

## 📋 目录

1. [项目概述](#项目概述)
2. [开发环境设置](#开发环境设置)
3. [项目结构](#项目结构)
4. [函数开发规范](#函数开发规范)
5. [添加新函数指南](#添加新函数指南)
6. [调试技巧](#调试技巧)
7. [性能优化](#性能优化)
8. [常见问题](#常见问题)

## 项目概述

ClickZetta AI SQL Functions 是为云器Lakehouse设计的AI函数集合，提供30个生产级AI函数，涵盖文本处理、向量计算、多模态分析和业务场景应用。

### 技术栈
- **Python 3.8+** - ClickZetta External Function运行时
- **DashScope API** - 阿里云通义千问AI服务
- **装饰器模式** - `@annotate` 用于函数注册
- **JSON格式** - 统一的输入输出格式

## 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/your-org/clickzetta_aisql.git
cd clickzetta_aisql
```

### 2. 创建虚拟环境
```bash
# 使用 venv
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

# 使用 uv（推荐）
uv venv
uv sync
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 获取和配置API密钥

#### 获取通义千问 API Key（必需）

1. **注册阿里云账号**
   - 访问 [阿里云官网](https://www.aliyun.com)
   - 完成实名认证

2. **开通 DashScope 服务**
   - 访问 [DashScope控制台](https://dashscope.console.aliyun.com)
   - 首次访问会提示开通服务
   - 同意服务协议并开通

3. **创建 API Key**
   - 在 DashScope 控制台点击"API-KEY管理"
   - 点击"创建新的API-KEY"
   - 复制生成的 API Key（格式：`sk-xxxxxxxxxxxxxxxx`）
   - ⚠️ **重要**：API Key 只显示一次，请立即保存

4. **配置 API Key**
   ```bash
   # 本地测试
   export DASHSCOPE_API_KEY="sk-xxxxxxx"
   
   # 或添加到 .env 文件
   echo "DASHSCOPE_API_KEY=sk-xxxxxxx" >> .env
   ```

5. **验证 API Key**
   ```python
   # test_api_key.py
   import dashscope
   dashscope.api_key = "sk-xxxxxxx"
   
   from dashscope import Generation
   response = Generation.call(
       model='qwen-turbo',
       prompt='Hello',
       max_tokens=5
   )
   print("API Key 有效！" if response.status_code == 200 else "API Key 无效")
   ```

#### API 配额说明
- **免费额度**：新用户有一定免费额度
- **计费模式**：按 token 使用量计费
- **模型选择**：
  - `qwen-turbo`：最便宜，适合测试
  - `qwen-plus`：平衡性能和成本
  - `qwen-max`：最强能力，成本较高

## 项目结构

```
clickzetta_aisql/
├── src/
│   ├── __init__.py
│   └── ai_functions_complete.py     # 核心实现文件
├── tests/
│   ├── test_complete_coverage.py    # 完整测试套件
│   ├── quick_validation.py          # 快速验证脚本
│   └── smart_analyzer.py            # 智能分析工具
├── scripts/
│   ├── package_with_deps.py         # 打包脚本
│   ├── fix_*.py                     # 修复脚本
│   └── optimize_*.py                # 优化脚本
├── data/
│   ├── test_config.json             # 测试配置
│   └── batch_test_data.json         # 批量测试数据
└── user_docs/                       # 用户文档
```

## 函数开发规范

### 1. 函数签名规范

```python
from clickzetta.external_function.annotate import annotate

@annotate("ai_function_name", 
    [{"name": "param1", "type": "string"},
     {"name": "param2", "type": "string"}, 
     {"name": "api_key", "type": "string"},
     {"name": "optional_param", "type": "string", "optional": True}],
    {"type": "string"})
def ai_function_name_impl(rows):
    """函数说明文档"""
    results = []
    for row in rows:
        try:
            # 处理逻辑
            result = process_with_ai(row[0], row[1], row[2])
            results.append(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            results.append(json.dumps({
                "error": f"处理失败: {str(e)}"
            }, ensure_ascii=False))
    return results
```

### 2. 参数设计原则

1. **必需参数在前**：输入数据 → API密钥 → 可选参数
2. **合理的默认值**：模型名称、温度等参数应有默认值
3. **参数验证**：检查必需参数是否为空
4. **类型一致**：所有参数类型统一为 "string"

### 3. 返回值规范

```python
# 成功返回
{
    "result": "处理结果",
    "metadata": {
        "model": "qwen-plus",
        "tokens": 150,
        "processing_time": 1.23
    }
}

# 错误返回
{
    "error": "错误信息",
    "error_type": "InvalidInput",
    "suggestion": "请检查输入参数"
}
```

## 添加新函数指南

### 步骤1：设计函数接口

```python
# 1. 确定函数名称（遵循 ai_category_action 命名规范）
function_name = "ai_text_classify"

# 2. 定义参数列表
params = [
    {"name": "text", "type": "string"},
    {"name": "categories", "type": "string"},  # JSON数组
    {"name": "api_key", "type": "string"},
    {"name": "model_name", "type": "string", "optional": True}
]

# 3. 定义返回类型
return_type = {"type": "string"}  # JSON格式
```

### 步骤2：实现函数逻辑

```python
@annotate("ai_text_classify", params, return_type)
def ai_text_classify_impl(rows):
    """文本分类函数"""
    results = []
    
    for row in rows:
        try:
            text = row[0]
            categories = json.loads(row[1]) if row[1] else []
            api_key = row[2]
            model_name = row[3] if len(row) > 3 and row[3] else "qwen-plus"
            
            # 参数验证
            if not text or not categories or not api_key:
                raise ValueError("缺少必需参数")
            
            # 调用AI服务
            result = call_dashscope_api(
                text=text,
                categories=categories,
                api_key=api_key,
                model=model_name
            )
            
            results.append(json.dumps(result, ensure_ascii=False))
            
        except Exception as e:
            results.append(json.dumps({
                "error": str(e),
                "error_type": type(e).__name__
            }, ensure_ascii=False))
    
    return results
```

### 步骤3：添加测试用例

在 `test_complete_coverage.py` 中添加：

```python
"ai_text_classify": {
    "params": {
        "text": "这是一条正面的产品评价",
        "categories": '["正面", "负面", "中性"]',
        "model_name": "qwen-plus"
    },
    "category": "文本处理",
    "expected_fields": ["category", "confidence", "reasoning"]
}
```

### 步骤4：文档化

在 `user_docs/07_FUNCTION_REFERENCE.md` 中添加函数说明。

## 调试技巧

### 1. 本地调试

```python
# 创建调试脚本 debug_function.py
import sys
sys.path.insert(0, 'src')
from ai_functions_complete import ai_text_classify_impl

# 模拟ClickZetta调用
test_rows = [
    ["测试文本", '["分类1", "分类2"]', "sk-xxx", "qwen-plus"]
]

results = ai_text_classify_impl(test_rows)
print(results[0])
```

### 2. 日志调试

```python
import logging

# 在函数开始处添加
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 在关键位置添加日志
logger.debug(f"Input parameters: {row}")
logger.info(f"API response: {response}")
```

### 3. 错误处理增强

```python
try:
    # 主要逻辑
    pass
except dashscope.errors.AuthenticationError:
    error_msg = "API密钥无效，请检查密钥是否正确"
except dashscope.errors.RateLimitError:
    error_msg = "API调用频率超限，请稍后重试"
except Exception as e:
    error_msg = f"未知错误: {str(e)}"
    logger.exception("Unexpected error")
```

## 性能优化

### 1. 响应大小优化（JIRA-001 需求）

#### 背景：优化前的问题
在项目初期，许多函数返回了大量冗余内容：
- 重复的解释文本（如"根据您的需求，我为您..."）
- 过度详细的步骤说明
- 不必要的格式化字符
- 平均响应大小：15-20KB
- 某些函数甚至达到 50KB+

#### 🎯 优化目标
- 达到 JIRA-001 要求：67% 的压缩率
- 保持功能完整性
- 提升用户体验

#### 优化策略和实现

**策略1：消除冗余的礼貌用语**
```python
# ❌ 优化前
def process_response_old(text):
    return f"""
    您好！感谢您使用我们的AI服务。
    根据您提供的文本内容，我已经为您完成了处理。
    以下是详细的处理结果：
    
    {actual_result}
    
    希望这个结果对您有所帮助。
    如果您还有其他需求，请随时告诉我。
    """

# ✅ 优化后
def process_response_new(text):
    return actual_result  # 直接返回核心结果
```

**策略2：精简返回结构**
```python
# ❌ 优化前 - 过度嵌套的结构
{
    "status": "success",
    "code": 200,
    "message": "处理成功",
    "data": {
        "result": {
            "content": "实际内容",
            "metadata": {
                "process_time": "2.3s",
                "model_used": "qwen-plus",
                "version": "1.0"
            }
        }
    },
    "timestamp": "2024-01-01T00:00:00Z"
}

# ✅ 优化后 - 扁平化结构
{
    "result": "实际内容",
    "model": "qwen-plus",
    "time": 2.3
}
```

**策略3：动态字段返回**
```python
def optimize_sentiment_response(sentiment_result):
    """根据结果动态决定返回字段"""
    # 基础结果
    response = {
        "sentiment": sentiment_result["label"],
        "score": sentiment_result["score"]
    }
    
    # 只在需要时添加额外信息
    if sentiment_result["score"] < 0.7:  # 置信度低时
        response["confidence"] = "low"
        response["suggestion"] = "结果仅供参考"
    
    # 移除所有null或空字段
    return {k: v for k, v in response.items() if v}
```

**策略4：智能截断长文本**
```python
def smart_truncate(text, max_length=1000):
    """智能截断，保持语义完整"""
    if len(text) <= max_length:
        return text
    
    # 在句号、问号、感叹号处截断
    for sep in ['。', '！', '？', '.', '!', '?']:
        pos = text.rfind(sep, 0, max_length)
        if pos > max_length * 0.8:  # 至少保留80%
            return text[:pos + 1]
    
    # 如果没找到合适的断点，在最后一个逗号处截断
    pos = text.rfind('，', 0, max_length)
    if pos > max_length * 0.8:
        return text[:pos] + "..."
    
    # 最后的选择：硬截断
    return text[:max_length] + "..."
```

**策略5：移除API原始响应的冗余**
```python
def clean_api_response(api_response):
    """清理API响应中的冗余内容"""
    # DashScope API 经常返回这样的内容
    redundant_prefixes = [
        "根据您的要求，",
        "我已经为您",
        "以下是",
        "基于提供的内容，",
        "经过分析，"
    ]
    
    result = api_response
    for prefix in redundant_prefixes:
        if result.startswith(prefix):
            result = result[len(prefix):]
            break
    
    # 移除结尾的冗余
    redundant_suffixes = [
        "希望对您有帮助。",
        "如有其他问题请告诉我。",
        "请问还有什么可以帮助您的吗？"
    ]
    
    for suffix in redundant_suffixes:
        if result.endswith(suffix):
            result = result[:-len(suffix)].rstrip()
            break
    
    return result.strip()
```

#### 实际优化案例

**案例1：文本摘要优化**
```python
# 优化前：平均 8KB
{
    "status": "success",
    "summary": {
        "content": "根据您提供的文章，我为您生成了以下摘要：本文主要讲述了...",
        "key_points": [
            "要点1：详细说明...",
            "要点2：详细说明...",
            "要点3：详细说明..."
        ],
        "metadata": {
            "original_length": 5000,
            "summary_length": 500,
            "compression_ratio": 0.1,
            "processing_time": "2.3s"
        }
    }
}

# 优化后：平均 2KB (75% 压缩)
{
    "summary": "本文主要讲述了...",
    "key_points": ["要点1", "要点2", "要点3"],
    "length": 500
}
```

**案例2：情感分析优化**
```python
# 优化前：3KB
{
    "analysis_result": {
        "sentiment": {
            "label": "正面",
            "score": 0.95,
            "confidence": "high",
            "details": {
                "positive_score": 0.95,
                "negative_score": 0.03,
                "neutral_score": 0.02
            }
        },
        "explanation": "这段文本表达了积极正面的情感..."
    }
}

# 优化后：200B (93% 压缩)
{
    "sentiment": "正面",
    "score": 0.95
}
```

#### 优化结果统计

| 函数类别 | 优化前平均大小 | 优化后平均大小 | 压缩率 |
|---------|--------------|--------------|--------|
| 文本处理 | 8-15 KB | 2-3 KB | 75-80% |
| 情感分析 | 3-5 KB | 200-500 B | 90-93% |
| 实体提取 | 10-20 KB | 3-5 KB | 70-75% |
| 业务场景 | 15-30 KB | 5-8 KB | 67-73% |

#### 特殊处理：向量函数保持不变
```python
# 向量函数不应该优化，因为数据本身就是必需的
def handle_vector_response(vector_data):
    """向量数据保持完整"""
    # 20-30KB 的向量数据是正常的
    return {
        "embedding": vector_data,  # 1536维或1024维浮点数
        "model": "text-embedding-v2",
        "dimensions": len(vector_data)
    }
```

#### 优化后的通用响应处理器
```python
def optimize_response(result, function_type="general", max_size=5000):
    """通用响应优化器"""
    # 向量类函数不优化
    if function_type in ["vector", "embedding"]:
        return json.dumps(result, ensure_ascii=False)
    
    # 第一步：清理冗余文本
    if isinstance(result, dict):
        for key in ["result", "content", "summary", "analysis"]:
            if key in result and isinstance(result[key], str):
                result[key] = clean_api_response(result[key])
    
    # 第二步：移除null和空值
    result = remove_empty_values(result)
    
    # 第三步：智能截断
    result_str = json.dumps(result, ensure_ascii=False)
    if len(result_str) > max_size:
        # 根据函数类型采用不同策略
        if function_type == "summary":
            result = truncate_summary(result, max_size)
        elif function_type == "analysis":
            result = simplify_analysis(result)
        else:
            result = generic_truncate(result, max_size)
    
    return json.dumps(result, ensure_ascii=False)

def remove_empty_values(obj):
    """递归移除空值"""
    if isinstance(obj, dict):
        return {k: remove_empty_values(v) 
                for k, v in obj.items() 
                if v is not None and v != "" and v != []}
    elif isinstance(obj, list):
        return [remove_empty_values(item) 
                for item in obj 
                if item is not None and item != ""]
    return obj
```

#### 优化经验总结

1. **识别真正的价值**：用户需要的是数据，不是客套话
2. **分类处理**：不同类型的函数需要不同的优化策略
3. **保护核心数据**：向量、OCR结果等不应过度优化
4. **测试驱动**：每次优化后都要验证功能完整性
5. **监控效果**：持续跟踪优化后的实际效果

### 2. 批处理优化

```python
# 对于支持批处理的API，合并请求
def process_batch(rows, batch_size=10):
    results = []
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        batch_results = call_batch_api(batch)
        results.extend(batch_results)
    return results
```

### 3. 缓存策略

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_api_call(text_hash, model):
    """缓存相同输入的API调用结果"""
    return call_api(text_hash, model)
```

## 部署故障排查

### 🚨 重要：函数计算服务器找不到函数的问题

这是部署过程中最常见且最难排查的问题。以下是完整的排查和解决方案。

#### 问题现象
- ClickZetta报错：`函数 'ai_text_summarize' 不存在`
- 函数计算服务器日志显示：`No function named 'ai_text_summarize' found`
- ZIP包已上传，但函数无法调用

#### 根本原因
1. **装饰器问题**：`@annotate` 装饰器未正确注册函数
2. **导入问题**：Python模块未正确加载
3. **路径问题**：ZIP包结构不正确

#### 解决方案检查清单

##### 1. 验证函数定义格式
```python
# ✅ 正确格式
@annotate("ai_text_summarize", 
    [{"name": "text", "type": "string"},
     {"name": "api_key", "type": "string"},
     {"name": "model_name", "type": "string", "optional": True},
     {"name": "max_length", "type": "string", "optional": True}],
    {"type": "string"})
def ai_text_summarize_impl(rows):
    # 实现代码
    pass

# ❌ 错误格式
def ai_text_summarize(rows):  # 缺少装饰器
    pass

@annotate("ai_text_summarize")  # 缺少参数定义
def ai_text_summarize_impl(rows):
    pass
```

##### 2. 验证ZIP包结构
```bash
# 检查ZIP包内容
unzip -l clickzetta_ai_functions_full.zip | head -20

# 正确的结构应该是：
# ai_functions_complete.py  （在根目录）
# dashscope/
# requests/
# ...其他依赖
```

##### 3. 验证函数注册
```python
# 在文件末尾添加调试代码（仅用于本地测试）
if __name__ == "__main__":
    # 列出所有注册的函数
    import sys
    from clickzetta.external_function import registry
    
    print("Registered functions:")
    for func_name in registry.get_all_functions():
        print(f"  - {func_name}")
```

##### 4. 验证模块导入
```python
# 确保所有必要的导入都在文件顶部
import json
import logging
from clickzetta.external_function.annotate import annotate
import dashscope
from dashscope import Generation
from http import HTTPStatus

# 设置日志（帮助调试）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

##### 5. 创建最小测试函数
```python
# 用于验证部署环境的最小函数
@annotate("test_echo", 
    [{"name": "input", "type": "string"}],
    {"type": "string"})
def test_echo_impl(rows):
    """简单的回显函数，用于测试部署"""
    results = []
    for row in rows:
        results.append(f"Echo: {row[0]}")
    return results
```

#### 部署验证步骤

1. **本地验证**
```bash
# 创建测试脚本
cat > test_functions.py << 'EOF'
import sys
sys.path.insert(0, '.')
from ai_functions_complete import *

# 测试函数是否可以导入
print("Testing import...")
try:
    test_rows = [["test", "sk-xxx"]]
    result = ai_text_summarize_impl(test_rows)
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
EOF

python test_functions.py
```

2. **打包验证**
```bash
# 创建干净的打包环境
rm -rf temp_package
mkdir temp_package

# 复制主文件
cp src/ai_functions_complete.py temp_package/

# 安装依赖
pip install dashscope --target temp_package/

# 创建ZIP包
cd temp_package
zip -r ../test_package.zip .
cd ..

# 验证ZIP包
unzip -t test_package.zip
```

3. **部署后验证**
```sql
-- 在ClickZetta中测试最简单的函数
SELECT test_echo('Hello World');

-- 如果test_echo工作，再测试其他函数
SELECT ai_text_summarize('测试文本', 'sk-xxx');
```

#### 历史问题总结

在项目初期，我们遇到了以下问题：

1. **问题1：函数名不匹配**
   - 症状：`ai_text_summarize` vs `ai_text_summarize_impl`
   - 解决：确保装饰器中的名称与SQL调用一致

2. **问题2：参数数量不匹配**
   - 症状：期望3个参数，实际传入4个
   - 解决：所有可选参数必须标记 `"optional": True`

3. **问题3：依赖包缺失**
   - 症状：`ModuleNotFoundError: No module named 'dashscope'`
   - 解决：确保所有依赖都打包到ZIP中

4. **问题4：Python版本不兼容**
   - 症状：语法错误或导入错误
   - 解决：使用Python 3.8（ClickZetta运行时版本）

#### 调试建议

1. **启用详细日志**
```python
# 在函数开始处添加
logger.info(f"Function called with {len(rows)} rows")
logger.debug(f"First row: {rows[0] if rows else 'No rows'}")
```

2. **添加错误边界**
```python
try:
    # 主逻辑
    pass
except Exception as e:
    logger.exception("Unexpected error in function")
    return [json.dumps({"error": str(e), "type": type(e).__name__})]
```

3. **分阶段测试（推荐方法）**

这是我们在实际项目中验证最有效的调试方案，通过逐步增加复杂度来定位问题。

**阶段1：验证基础环境**
```python
# step1_basic.py - 最简单的函数，不依赖任何外部库
@annotate("test_basic", 
    [{"name": "input", "type": "string"}],
    {"type": "string"})
def test_basic_impl(rows):
    """验证ClickZetta能找到并执行函数"""
    return [f"Basic test: {row[0]}" for row in rows]
```

**阶段2：验证JSON处理**
```python
# step2_json.py - 测试JSON序列化
import json

@annotate("test_json", 
    [{"name": "input", "type": "string"}],
    {"type": "string"})
def test_json_impl(rows):
    """验证JSON处理能力"""
    results = []
    for row in rows:
        result = {"input": row[0], "processed": True}
        results.append(json.dumps(result, ensure_ascii=False))
    return results
```

**阶段3：验证外部依赖**
```python
# step3_dependencies.py - 测试dashscope导入
import json
import dashscope  # 测试外部依赖

@annotate("test_dependencies", 
    [{"name": "input", "type": "string"}],
    {"type": "string"})
def test_dependencies_impl(rows):
    """验证外部依赖包能正常导入"""
    results = []
    for row in rows:
        result = {
            "input": row[0],
            "dashscope_version": dashscope.__version__,
            "status": "dependencies loaded"
        }
        results.append(json.dumps(result, ensure_ascii=False))
    return results
```

**阶段4：验证API调用（使用真实API密钥）**
```python
# step4_api_call.py - 测试真实API调用
import json
import dashscope
from dashscope import Generation

@annotate("test_api_call", 
    [{"name": "text", "type": "string"},
     {"name": "api_key", "type": "string"}],
    {"type": "string"})
def test_api_call_impl(rows):
    """验证能否调用DashScope API"""
    results = []
    for row in rows:
        try:
            dashscope.api_key = row[1]
            # 最简单的API调用
            response = Generation.call(
                model='qwen-turbo',
                prompt=row[0],
                max_tokens=10  # 限制token节省成本
            )
            result = {
                "status": "success",
                "response": response.output.text[:50]
            }
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            }
        results.append(json.dumps(result, ensure_ascii=False))
    return results
```

**阶段5：部署完整函数**
```python
# 只有前4个阶段都成功后，才部署完整的30个函数
```

**调试流程**：
1. 部署step1_basic.py，测试`SELECT test_basic('hello')`
   - 如果失败：检查handler路径、函数注册
   - 如果成功：继续下一步

2. 部署step2_json.py，测试JSON返回
   - 如果失败：检查JSON序列化问题
   - 如果成功：基础环境正常

3. 部署step3_dependencies.py，测试依赖包
   - 如果失败：检查ZIP包是否包含所有依赖
   - 如果成功：依赖加载正常

4. 部署step4_api_call.py，测试API连接
   - 如果失败：检查网络、API密钥、权限
   - 如果成功：可以部署完整版本

**实际案例**：
在我们的项目中，问题在第3阶段被发现 - dashscope包没有正确打包。通过这种方法，我们避免了在30个函数中逐一排查，大大提高了调试效率。

## 常见问题

### Q1: 函数超时怎么办？

设置合理的超时时间：
```python
response = dashscope.Generation.call(
    model=model_name,
    messages=messages,
    timeout=30  # 30秒超时
)
```

### Q2: 如何处理大文本输入？

```python
def process_large_text(text, max_length=6000):
    if len(text) > max_length:
        # 分段处理
        chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        results = []
        for chunk in chunks:
            result = process_chunk(chunk)
            results.append(result)
        return merge_results(results)
    return process_text(text)
```

### Q3: 如何添加新的AI能力？

1. 确认DashScope API支持
2. 遵循现有函数模式
3. 添加完整的错误处理
4. 编写测试用例
5. 更新文档

### Q4: 部署前检查清单

- [ ] 所有函数都有错误处理
- [ ] 返回值格式统一为JSON
- [ ] 参数验证完整
- [ ] 测试覆盖率达标
- [ ] 文档更新完成
- [ ] 性能测试通过

## CREATE EXTERNAL FUNCTION 关键注意事项

### 🎯 重要：创建函数的完整流程

#### 1. 准备API CONNECTION（必须先创建）
```sql
-- 创建API连接（阿里云示例）
CREATE API CONNECTION IF NOT EXISTS dashscope_api_conn
AS 'http://sls-vpc.aliyun.com/v1'
WITH
    ROLE_ARN = 'acs:ram::xxx:role/AliyunServiceRoleForSLS',
    CODE_BUCKET = 'your-oss-bucket-name';
```

#### 2. 上传ZIP包到Volume
```sql
-- 上传文件到Volume（确保文件路径正确）
PUT 'file:///Users/liangmo/Downloads/clickzetta_ai_functions_full.zip' 
TO 'volume://code_bucket/ai_functions/clickzetta_ai_functions_full.zip';
```

#### 3. 创建外部函数（正确的语法）
```sql
-- ✅ 正确的创建语句
CREATE OR REPLACE EXTERNAL FUNCTION ai_text_summarize(
    text STRING,
    api_key STRING,
    model_name STRING,
    max_length STRING
)
RETURNS STRING
AS 'volume://code_bucket/ai_functions/clickzetta_ai_functions_full.zip'
CONNECTION = dashscope_api_conn
RUNTIME = 'python3.8'
HANDLER = 'ai_functions_complete.ai_text_summarize_impl';

-- ❌ 常见错误
CREATE EXTERNAL FUNCTION ai_text_summarize  -- 缺少参数定义
AS 'oss://bucket/file.zip'  -- 应该使用volume://
HANDLER = 'ai_text_summarize';  -- 应该是模块名.函数名
```

#### 4. 批量创建函数的技巧
```sql
-- 使用事务批量创建
BEGIN;

-- 文本处理函数
CREATE OR REPLACE EXTERNAL FUNCTION ai_text_summarize...
CREATE OR REPLACE EXTERNAL FUNCTION ai_text_translate...
CREATE OR REPLACE EXTERNAL FUNCTION ai_text_sentiment_analyze...

-- 向量处理函数
CREATE OR REPLACE EXTERNAL FUNCTION ai_text_to_embedding...
CREATE OR REPLACE EXTERNAL FUNCTION ai_text_similarity...

COMMIT;
```

#### 5. 验证函数创建成功
```sql
-- 查看所有外部函数
SHOW FUNCTIONS LIKE 'ai_%';

-- 测试函数
SELECT ai_text_summarize(
    '这是一段测试文本',
    'sk-your-api-key',
    'qwen-plus',
    '100'
);
```

### 常见CREATE FUNCTION错误

1. **Handler路径错误**
   ```sql
   -- ❌ 错误
   HANDLER = 'ai_text_summarize_impl'  -- 缺少模块名
   
   -- ✅ 正确
   HANDLER = 'ai_functions_complete.ai_text_summarize_impl'
   ```

2. **参数不匹配**
   ```sql
   -- ❌ 错误：参数数量与Python函数不匹配
   CREATE FUNCTION ai_text_summarize(text STRING, api_key STRING)
   -- 但Python函数期望4个参数
   
   -- ✅ 正确：包含所有参数
   CREATE FUNCTION ai_text_summarize(
       text STRING, 
       api_key STRING,
       model_name STRING,  -- 即使是可选参数也要声明
       max_length STRING
   )
   ```

3. **Volume路径错误**
   ```sql
   -- ❌ 错误
   AS 's3://bucket/file.zip'
   AS 'oss://bucket/file.zip'
   AS '/path/to/file.zip'
   
   -- ✅ 正确
   AS 'volume://code_bucket/path/to/file.zip'
   ```

### 部署检查清单

- [ ] API CONNECTION 已创建
- [ ] ZIP包已上传到Volume
- [ ] CREATE FUNCTION语句参数与Python函数匹配
- [ ] Handler格式为 `模块名.函数名`
- [ ] 使用正确的Volume路径
- [ ] 指定正确的RUNTIME版本
- [ ] 测试每个函数确保可用

## 最佳实践总结

1. **保持一致性**：函数命名、参数顺序、返回格式保持一致
2. **优雅降级**：API失败时返回有意义的错误信息
3. **性能意识**：注意响应大小和处理时间
4. **安全第一**：不要在代码中硬编码API密钥
5. **充分测试**：每个函数至少3个测试用例
6. **文档完整**：代码即文档，注释要清晰
7. **部署验证**：每次部署后立即验证函数可用性

---

*最后更新：2025-06-14*