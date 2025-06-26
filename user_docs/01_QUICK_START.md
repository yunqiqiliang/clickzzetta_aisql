# 云器Lakehouse AI Functions 快速开始

> 📖 这是文档的第二部分。如果您还没有阅读项目概述，请先查看 [00_README.md](./00_README.md)
> 
> ⚠️ **重要提示**: 部署过程涉及多个步骤，建议预留 **1-2小时** 完成整个流程。如需快速体验，请参考 [简化版快速开始](./01_QUICK_START_SIMPLIFIED.md)。

## 📋 部署检查清单

在开始之前，请确保您已准备好以下内容：

### 必备条件
- [ ] **云器Lakehouse账号**（获取方法见下方）
- [ ] **通义千问 API Key**（获取方法见下方）
- [ ] **云器Lakehouse访问权限**
  - [ ] 可以创建外部函数
  - [ ] 可以创建API Connection
  - [ ] 可以操作Volume
- [ ] **云平台资源**（阿里云/腾讯云/AWS之一）
  - [ ] 已创建存储桶（OSS/COS/S3）
  - [ ] 已配置访问权限
  - [ ] 已获取必要的ARN/角色信息

### 获取云器Lakehouse账号
如果您还没有云器Lakehouse账号，请按以下步骤申请：

1. **申请试用账号**
   - 访问 [云器官网](https://www.yunqi.tech/)
   - 点击"免费试用"或"联系我们"
   - 填写企业信息和联系方式
   - 提交申请

2. **账号开通**
   - 云器团队会在1个工作日内联系您
   - 确认试用需求后，会为您开通试用账号
   - 您将收到账号信息和登录地址

3. **试用账号权益**
   - 200元代金券（自动充值）
   - 30天试用期
   - 最多28 CRU计算资源配额
   - 完整功能体验（部分功能有配额限制）

4. **登录控制台**
   - 使用提供的账号登录：`https://您的账号名.accounts.clickzetta.com`
   - 首次登录需要修改密码
   - 进入Lakehouse Studio开始使用

> ⚠️ **注意**: 试用期结束后，如需继续使用请联系云器商务升级为正式账户

### 获取通义千问 API Key（必需）
1. 访问 [DashScope控制台](https://dashscope.console.aliyun.com)
2. 使用阿里云账号登录（需要实名认证）
3. 首次访问会提示开通服务（免费）
4. 在控制台中：
   - 点击"API-KEY管理"
   - 点击"创建新的API-KEY"
   - **立即复制并保存**（只显示一次）
   - API Key格式：`sk-xxxxxxxxxxxxxxxx`

> 💡 **提示**: 新用户有免费额度，足够测试使用

## 🔧 命令说明
本文档使用 `python3` 命令（适用于 macOS/Linux）。Windows 用户请使用 `python`。

## 📦 部署文件
- **文件**: `clickzetta_ai_functions_full.zip` (2.5MB)
- **内容**: 30个AI函数 + 所有依赖

## 📋 准备工作

在开始部署之前，请完成以下准备工作：

### 1. 云平台资源准备（以阿里云为例）

**A. 创建ROLE_ARN**
1. 登录阿里云RAM控制台
2. 创建权限策略：
   - 添加函数计算权限（AliyunFCFullAccess）
   - 创建OSS访问策略（包含您的bucket权限）
3. 创建角色（如CzUDFRole）：
   - 选择"阿里云账号"类型
   - 信任账号设置为：`1384322691904283`（云器Lakehouse的阿里云账号）
   - 授予上述权限策略
4. 获取Role ARN：`acs:ram::您的账号ID:role/角色名`

**B. 创建CODE_BUCKET**
- 在阿里云OSS中创建一个存储桶，用于存放函数代码包

**支持的云平台**
- **阿里云** (provider='aliyun')：Function Compute + OSS
- **腾讯云** (provider='tencent')：云函数 + COS
- **AWS** (provider='aws')：Lambda + S3

详细配置步骤请参考[云平台配置指南](./02_CLOUD_PLATFORM_SETUP.md)。

### 2. Volume准备

**A. 创建存储连接**（如果使用外部存储）
```sql
-- 以阿里云OSS为例
CREATE STORAGE CONNECTION oss_func_conn
    TYPE oss
    ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'
    ACCESS_ID = 'your_access_id'
    ACCESS_KEY = 'your_access_key';
```

**B. 创建Volume**
```sql
-- 外部Volume（推荐用于生产环境）
CREATE EXTERNAL VOLUME external_functions_prod
    LOCATION 'oss://your-bucket/ai-functions/'
    USING CONNECTION oss_func_conn
    DIRECTORY = (ENABLE = true)
    COMMENT = 'AI函数部署包存储';

-- 或使用内部Volume（适用于测试）
CREATE VOLUME internal_functions_test
    DIRECTORY = (ENABLE = true)
    COMMENT = 'AI函数测试部署';
```

**支持的存储类型**
- **阿里云OSS**：通过CREATE STORAGE CONNECTION配置
- **腾讯云COS**：需要APP_ID参数
- **AWS S3**：需要REGION参数
- **内部存储**：直接CREATE VOLUME即可

详细配置步骤请参考[Volume配置指南](./03_VOLUME_SETUP_GUIDE.md)。

## 🚀 快速部署

### 1. 创建API连接

```sql
CREATE API CONNECTION ai_function_connection
TYPE CLOUD_FUNCTION
PROVIDER='aliyun'
REGION='cn-hangzhou'
ROLE_ARN='acs:ram::xxxxx:role/czudfrole'
CODE_BUCKET='your-bucket-name';
```

### 2. 上传函数包

```sql
PUT file://clickzetta_ai_functions_full.zip TO volume://external_functions_prod/;
```

### 3. 部署函数

```sql
-- 执行 docs/05_AI_FUNCTIONS_DEPLOYMENT_WITH_COMMENTS.sql
-- 该脚本会创建所有30个AI函数
```

## ✅ 验证部署

### Schema说明
- 函数创建在哪个schema，调用时必须使用该schema名称
- 下面示例假设函数创建在 `public` schema
- 如果您使用其他schema（如 `my_schema`），请相应调整

```sql
-- 查看函数列表
SHOW FUNCTIONS LIKE '%ai_%';

-- 测试函数（需要有效的DashScope API密钥）
-- 注意：将 'public' 替换为您实际使用的schema名称
SELECT public.ai_text_summarize(
    '这是一段测试文本',
    'sk-xxxxxxxx',  -- 您的API密钥
    'qwen-plus',
    100
) as result;
```

## 📖 函数使用

所有函数都需要schema前缀：
```sql
-- 文本摘要
SELECT public.ai_text_summarize(content, 'api-key') FROM aisql_demo_articles;

-- 翻译
SELECT public.ai_text_translate(content, '英文', 'api-key') FROM aisql_demo_documents;

-- 情感分析
SELECT public.ai_text_sentiment_analyze(review, 'api-key') FROM aisql_demo_feedback;
```

> 💡 **提示**: 使用 [12_CREATE_DEMO_TABLES.sql](./12_CREATE_DEMO_TABLES.sql) 创建演示表

## 📚 下一步

- **查看函数详情**: [07_FUNCTION_REFERENCE.md](./07_FUNCTION_REFERENCE.md)
- **了解最佳实践**: [08_EXTERNAL_FUNCTION_BEST_PRACTICES.md](./08_EXTERNAL_FUNCTION_BEST_PRACTICES.md)
- **遇到问题**: [09_TROUBLESHOOTING.md](./09_TROUBLESHOOTING.md)
- **返回目录**: [INDEX.md](./INDEX.md)