# Schema 使用指南

## 🎯 核心原则

**函数在哪个schema创建，就必须用哪个schema调用**

## 📝 详细说明

### 1. 创建函数时指定Schema

```sql
-- 示例1：在 public schema 创建函数
CREATE EXTERNAL FUNCTION public.ai_text_summarize ...

-- 示例2：在 my_schema 创建函数
CREATE EXTERNAL FUNCTION my_schema.ai_text_summarize ...

-- 示例3：在当前默认schema创建函数（不推荐）
CREATE EXTERNAL FUNCTION ai_text_summarize ...
```

### 2. 调用函数时必须匹配Schema

```sql
-- 如果函数创建在 public schema
SELECT public.ai_text_summarize(content, 'api-key') FROM articles;

-- 如果函数创建在 my_schema
SELECT my_schema.ai_text_summarize(content, 'api-key') FROM articles;

-- 如果函数创建在 analytics schema
SELECT analytics.ai_text_summarize(content, 'api-key') FROM articles;
```

### 3. 查看函数所在的Schema

```sql
-- 查看所有AI函数及其schema
SHOW FUNCTIONS LIKE '%ai_%';

-- 查看特定schema中的函数
SHOW FUNCTIONS IN SCHEMA public LIKE '%ai_%';
SHOW FUNCTIONS IN SCHEMA my_schema LIKE '%ai_%';
```

## ⚠️ 常见错误

### 错误1：函数未找到
```sql
-- 错误：直接调用不带schema
SELECT ai_text_summarize(...);  -- ❌ 可能报错：函数未找到

-- 正确：带上schema名称
SELECT public.ai_text_summarize(...);  -- ✅
```

### 错误2：Schema不匹配
```sql
-- 函数创建在 schema_a
CREATE EXTERNAL FUNCTION schema_a.ai_text_summarize ...

-- 错误：使用了错误的schema
SELECT schema_b.ai_text_summarize(...);  -- ❌ 函数未找到

-- 正确：使用创建时的schema
SELECT schema_a.ai_text_summarize(...);  -- ✅
```

## 🔧 最佳实践

### 1. 统一Schema管理
建议在组织内统一规定AI函数的schema，例如：
- 所有AI函数都创建在 `ai_functions` schema
- 或者按照环境区分：`dev_ai`、`prod_ai`

### 2. 修改部署脚本
在 `AI_FUNCTIONS_DEPLOYMENT_WITH_COMMENTS.sql` 中，将所有的 `public` 替换为您的目标schema：

```bash
# 使用sed命令批量替换（Linux/macOS）
sed -i 's/public\./your_schema\./g' AI_FUNCTIONS_DEPLOYMENT_WITH_COMMENTS.sql

# 或手动在编辑器中查找替换
# 查找: public.
# 替换: your_schema.
```

### 3. 文档化Schema选择
在项目文档中明确记录：
- 使用的schema名称
- 选择该schema的原因
- 相关的权限配置

## 📋 快速检查清单

- [ ] 确定要使用的schema名称
- [ ] 修改部署脚本中的schema引用
- [ ] 创建函数时使用完整的 `schema.function_name` 格式
- [ ] 调用函数时使用相同的schema前缀
- [ ] 在文档中记录schema选择

## 💡 示例场景

### 场景1：多租户环境
```sql
-- 租户A的函数
CREATE EXTERNAL FUNCTION tenant_a.ai_text_summarize ...
SELECT tenant_a.ai_text_summarize(...) FROM tenant_a.documents;

-- 租户B的函数
CREATE EXTERNAL FUNCTION tenant_b.ai_text_summarize ...
SELECT tenant_b.ai_text_summarize(...) FROM tenant_b.documents;
```

### 场景2：环境隔离
```sql
-- 开发环境
CREATE EXTERNAL FUNCTION dev.ai_text_summarize ...
SELECT dev.ai_text_summarize(...) FROM dev.test_data;

-- 生产环境
CREATE EXTERNAL FUNCTION prod.ai_text_summarize ...
SELECT prod.ai_text_summarize(...) FROM prod.real_data;
```

---

记住：**Schema一致性是关键！**