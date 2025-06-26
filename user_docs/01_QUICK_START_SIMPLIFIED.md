# 云器Lakehouse AI Functions 快速开始（简化版）

## ⚡ 30分钟快速部署指南

这个指南帮助您在30分钟内完成AI函数的部署。整个过程包含多个步骤，请按照检查清单逐步完成。

## 📋 部署前检查清单

### 必备条件
- [ ] 有云器Lakehouse账号（见下方获取步骤）
- [ ] 有创建外部函数的权限
- [ ] 准备好通义千问API Key（见下方获取步骤）

### 获取云器Lakehouse账号（5分钟）
1. [ ] 访问 [云器官网](https://www.yunqi.tech/)
2. [ ] 点击"免费试用"或"申请试用"
3. [ ] 填写企业信息和联系方式
4. [ ] 等待云器团队联系（通常1个工作日内）
5. [ ] 获得试用账号后登录 [Lakehouse控制台](https://你的账号.accounts.clickzetta.com)

> 💡 试用账号包含：
> - 200元代金券
> - 30天试用期
> - 最多28 CRU计算资源
> - 完整功能体验（有配额限制）

### 获取通义千问 API Key（5分钟）
1. [ ] 访问 [DashScope控制台](https://dashscope.console.aliyun.com)
2. [ ] 使用阿里云账号登录（需实名认证）
3. [ ] 首次访问时开通DashScope服务（免费）
4. [ ] 点击"API-KEY管理" → "创建新的API-KEY"
5. [ ] **立即复制保存**（格式：`sk-xxxxxxxxxxxxxxxx`）

> ⚠️ API Key只显示一次，请务必保存！

## 🚀 三步部署流程

### 第1步：准备部署文件（2分钟）

下载部署包：
- 文件名：`clickzetta_ai_functions_full.zip`
- 大小：2.5MB
- 下载地址：请联系项目组获取

### 第2步：在Lakehouse中执行部署（20分钟）

#### 2.1 创建API连接（针对阿里云）
```sql
-- 复制并修改以下SQL，替换xxxxx为您的实际值
CREATE API CONNECTION ai_function_connection
TYPE CLOUD_FUNCTION
PROVIDER='aliyun'
REGION='cn-hangzhou'  -- 修改为您的区域
ROLE_ARN='acs:ram::xxxxx:role/AliyunServiceRoleForFC'  -- 使用函数计算默认角色
CODE_BUCKET='your-oss-bucket';  -- 您的OSS bucket名称
```

> 💡 如果没有OSS bucket，可以在[阿里云OSS控制台](https://oss.console.aliyun.com)快速创建一个

#### 2.2 上传部署包
```sql
-- 方式1：从本地上传（推荐）
PUT file:///Users/yourname/Downloads/clickzetta_ai_functions_full.zip 
TO volume://internal/ai_functions/;

-- 方式2：如果已上传到OSS
COPY oss://your-bucket/clickzetta_ai_functions_full.zip
TO volume://internal/ai_functions/;
```

#### 2.3 创建测试函数（先测试一个）
```sql
-- 创建一个简单的测试函数
CREATE OR REPLACE EXTERNAL FUNCTION ai_text_summarize(
    text STRING,
    api_key STRING,
    model_name STRING,
    max_length STRING
)
RETURNS STRING
AS 'volume://internal/ai_functions/clickzetta_ai_functions_full.zip'
CONNECTION = ai_function_connection
RUNTIME = 'python3.8'
HANDLER = 'ai_functions_complete.ai_text_summarize_impl';
```

### 第3步：验证部署（5分钟）

```sql
-- 测试函数是否工作
SELECT ai_text_summarize(
    '人工智能正在改变我们的生活方式。从智能手机到自动驾驶汽车，AI技术无处不在。',
    'sk-您的API密钥',  -- 替换为您的实际API Key
    'qwen-turbo',      -- 使用最便宜的模型测试
    '50'               -- 摘要长度
);
```

**预期结果**：应该返回一段简短的摘要文本

## ✅ 部署成功后的下一步

### 如果测试成功
1. **部署所有30个函数**
   - 执行完整的部署脚本（联系项目组获取）
   - 或参考 [完整部署指南](./02_FULL_DEPLOYMENT_GUIDE.md)

2. **开始使用**
   ```sql
   -- 情感分析示例
   SELECT ai_text_sentiment_analyze(
       '这个产品真的太棒了！',
       'sk-您的API密钥'
   );
   
   -- 文本翻译示例
   SELECT ai_text_translate(
       'Hello World',
       '中文',
       'sk-您的API密钥'
   );
   ```

### 如果测试失败
参考 [故障排查指南](./09_TROUBLESHOOTING.md) 或查看下方常见问题。

## ❓ 常见问题快速解答

### Q1: 提示"函数不存在"
**A**: 检查Handler路径，必须是 `ai_functions_complete.函数名_impl`

### Q2: API调用失败
**A**: 
- 检查API Key是否正确（sk-开头）
- 确认DashScope服务已开通
- 验证是否有剩余额度

### Q3: 网络连接错误
**A**: 
- 检查Lakehouse实例是否能访问外网
- 如在VPC内，需要配置NAT网关

### Q4: 返回结果过大
**A**: 这是正常的，特别是向量函数（20-30KB）

## 📞 需要帮助？

- **技术文档**: 查看 [完整文档目录](./INDEX.md)
- **详细指南**: 阅读 [完整部署指南](./02_FULL_DEPLOYMENT_GUIDE.md)
- **函数说明**: 参考 [函数参考手册](./07_FUNCTION_REFERENCE.md)

---

**提示**: 整个部署过程虽然步骤较多，但每一步都很重要。如果遇到问题，不要跳过，请参考故障排查指南解决后再继续。

*版本: v1.0 | 更新时间: 2025-06-14*