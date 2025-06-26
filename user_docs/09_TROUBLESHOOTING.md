# 故障排查：模拟模式问题

## 🔍 问题现象
函数返回"模拟模式"而不是真实的AI处理结果。

## 🎯 根本原因
部署的函数仍在使用旧版本的代码。

## ✅ 解决步骤

### 1. 验证本地代码（已完成）
```bash
# 检查ai_functions_complete.py中是否还有"模拟模式"
grep -n "模拟模式" ai_functions_complete.py
# 应该返回空（已经全部替换）
```

### 2. 重新生成部署包
```bash
# 确保使用最新代码重新打包
python3 package_with_deps.py

# 验证包的时间戳
ls -lh clickzetta_ai_functions_full.zip
# 应该显示最新时间（2025-06-14 15:27或之后）
```

### 3. 完全重新部署

#### 步骤1：删除旧函数
```sql
-- 删除所有现有函数
-- 注意：将 'public' 替换为您实际创建函数的schema名称
DROP FUNCTION IF EXISTS public.ai_text_summarize;
DROP FUNCTION IF EXISTS public.ai_text_translate;
-- ... 对所有30个函数执行
```

#### 步骤2：清理Volume中的旧文件
```sql
-- 删除旧的ZIP文件（如果存在）
REMOVE @volume://external_functions_prod/clickzetta_ai_functions_full.zip;

-- 确认清理完成
LIST @volume://external_functions_prod/;
```

#### 步骤3：上传新文件
```sql
-- 上传最新的包（2.5MB）
PUT file://clickzetta_ai_functions_full.zip TO volume://external_functions_prod/;

-- 验证上传
LIST @volume://external_functions_prod;
```

#### 步骤4：重新创建函数
```sql
-- 执行 docs/05_AI_FUNCTIONS_DEPLOYMENT_WITH_COMMENTS.sql
-- 确保使用的是 clickzetta_ai_functions_full.zip
```

### 4. 验证部署

#### 测试1：检查错误处理
```sql
-- 使用无效API密钥，应该看到新的错误信息
SELECT public.ai_text_summarize('test', 'invalid-key');

-- 期望结果：
-- {"error": true, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}

-- 不应该看到：
-- {"error": false, "summary": "...", "note": "模拟模式"}
```

#### 测试2：使用有效API密钥
```sql
-- 使用真实的DashScope API密钥
SELECT public.ai_text_summarize(
    '这是一段测试文本，用于验证AI函数是否正常工作。',
    'sk-xxxxxxxxxxxxxxxx',  -- 您的真实API密钥
    'qwen-plus',
    100
);

-- 期望结果：真实的AI生成摘要
```

## 🔧 其他可能的问题

### 1. 函数缓存
某些系统可能缓存函数定义。尝试：
- 重启连接会话
- 使用新的会话测试

### 2. Python环境问题
确认函数计算环境：
- Python版本是否为3.10+
- 是否能正确加载dashscope库

### 3. 网络连接
确认函数计算服务能访问：
- https://dashscope.aliyuncs.com
- 相关的API端点

## 📝 验证清单

- [ ] 本地代码已更新（无"模拟模式"）
- [ ] 重新打包生成新的ZIP（2.5MB）
- [ ] 删除所有旧函数
- [ ] 清理Volume中的旧文件
- [ ] 上传新的ZIP文件
- [ ] 重新创建所有函数
- [ ] 测试确认无"模拟模式"返回
- [ ] 使用真实API密钥测试成功

如果完成以上所有步骤后仍有问题，可能需要检查云器Lakehouse的函数计算服务配置。