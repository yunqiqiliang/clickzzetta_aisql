# ClickZetta External Function Handler 格式指南

## ⚠️ 重要：Handler 必须包含模块名

### 错误原因分析
您遇到的错误：
```
Invalid handler text_to_embedding
ValueError: substring not found
```

这是因为 ClickZetta 的 UDF 服务器在解析 handler 时，会查找最后一个点（.）来分隔模块名和类名：
```python
last_dot_index = handler.rindex(".")  # 这里会失败如果没有点
```

### ✅ 正确的 Handler 格式

```sql
HANDLER = '模块名.类名'
```

例如：
- `HANDLER = 'vector_functions.text_to_embedding'`
- `HANDLER = 'multimodal_functions.image_analyze'`
- `HANDLER = 'business_functions.customer_intent_analyze'`
- `HANDLER = 'bailian_llm.get_industry_classification'`

### ❌ 错误的 Handler 格式

```sql
HANDLER = '类名'  -- 缺少模块名
```

例如：
- `HANDLER = 'text_to_embedding'` ❌
- `HANDLER = 'image_analyze'` ❌

### 📦 包结构要求

您的 zip 包应该包含以下结构：
```
clickzetta_aisql.zip
├── vector_functions.py      # 包含 text_to_embedding 类
├── multimodal_functions.py  # 包含 image_analyze 等类
├── business_functions.py    # 包含 customer_intent_analyze 等类
├── text_functions.py        # 包含 text_summarize 等类
├── bailian_llm.py          # 包含 get_industry_classification 类
└── [其他依赖文件]
```

### 🔍 如何确定正确的 Handler 路径

1. **查看 Python 文件名**：文件名就是模块名（去掉 .py）
2. **查看类名**：在文件中找到 `class 类名`
3. **组合**：`模块名.类名`

例如，在 `vector_functions.py` 中有：
```python
@annotate("*->string")
class text_to_embedding(BaseLLMFunction):
    handler = "evaluate"
    ...
```

那么 Handler 就是：`vector_functions.text_to_embedding`

### 💡 调试技巧

如果仍然遇到问题，可以：
1. 检查 zip 包内容：`unzip -l your_package.zip`
2. 确认文件在 zip 包的根目录，而不是子目录中
3. 验证类名拼写是否正确（区分大小写）

### 📝 完整示例

```sql
-- 先删除已存在的函数
DROP FUNCTION IF EXISTS text_to_embedding;

-- 创建函数，注意 HANDLER 格式
CREATE EXTERNAL FUNCTION text_to_embedding(
    text STRING, 
    api_key STRING, 
    model_name STRING, 
    dimension STRING
) 
RETURNS STRING
HANDLER = 'vector_functions.text_to_embedding'  -- 必须包含模块名！
PACKAGES = ('volume://user_files/clickzetta_aisql_v1.0.1_fixed.zip');

-- 测试函数
SELECT text_to_embedding(
    'ClickZetta是新一代云原生数据湖仓', 
    'your_api_key',
    'text-embedding-v4',
    'auto'
);
```