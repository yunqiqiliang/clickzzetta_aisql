# ClickZetta AI Functions 部署检查清单

## 📋 部署前准备 Checklist

### 1. 账号和权限准备

#### 云器Lakehouse账号
- [ ] **获取账号**
  - [ ] 访问 [云器官网](https://www.yunqi.tech/) 申请试用
  - [ ] 填写企业信息并提交申请
  - [ ] 等待云器团队联系（1个工作日内）
  - [ ] 获得账号信息和登录地址

- [ ] **账号权限确认**
  - [ ] 可以登录 Lakehouse Studio
  - [ ] 有创建外部函数的权限
  - [ ] 有创建 API Connection 的权限
  - [ ] 有 Volume 操作权限
  - [ ] 有创建 Workspace 的权限（如需要）

- [ ] **试用账号限制了解**
  - [ ] 200元代金券额度
  - [ ] 30天试用期限
  - [ ] 最多28 CRU计算资源
  - [ ] 最多1000个数据对象

#### 通义千问 API 账号
- [ ] **阿里云账号**
  - [ ] 已注册并完成实名认证
  - [ ] 已开通 DashScope 服务（免费）
  - [ ] 已创建并保存 API Key（sk-xxxxx）
  - [ ] 已确认 API 额度充足

### 2. 云平台资源准备

#### 阿里云部署
- [ ] **创建 RAM 角色**
  ```
  角色名称：AliyunFCInvocationRole
  信任策略：允许函数计算服务
  ```
- [ ] **创建 OSS Bucket**
  ```
  Bucket名称：your-function-code-bucket
  权限：私有
  地域：与 Lakehouse 相同
  ```
- [ ] **获取必要信息**
  - [ ] ROLE_ARN：`acs:ram::xxxxx:role/AliyunFCInvocationRole`
  - [ ] CODE_BUCKET：`your-function-code-bucket`

#### 腾讯云部署
- [ ] **创建云函数角色**
- [ ] **创建 COS 存储桶**
- [ ] **配置 VPC（如需要）**

#### AWS 部署
- [ ] **创建 Lambda 执行角色**
- [ ] **创建 S3 存储桶**
- [ ] **配置安全组**

### 3. 本地环境准备
- [ ] **Python 环境**
  - [ ] Python 3.8 已安装（与 ClickZetta 运行时一致）
  - [ ] pip 或 uv 包管理器可用
  
- [ ] **项目文件**
  - [ ] 克隆项目代码
  - [ ] requirements.txt 存在
  - [ ] ai_functions_complete.py 完整（30个函数）

### 4. 打包准备
- [ ] **依赖检查**
  ```bash
  # 检查主要依赖
  pip list | grep dashscope
  ```
  
- [ ] **打包测试**
  ```bash
  # 运行打包脚本
  python3 package_and_copy.py --rebuild
  ```
  
- [ ] **验证 ZIP 包**
  ```bash
  # 检查包内容
  unzip -l dist/clickzetta_ai_functions_full.zip | head -20
  # 应该看到：
  # - ai_functions_complete.py
  # - dashscope/
  # - 其他依赖包
  ```

## 🚀 部署步骤 Checklist

### 步骤 1：创建 API Connection
- [ ] **执行创建语句**
  ```sql
  CREATE API CONNECTION IF NOT EXISTS ai_function_conn
  AS 'acs:fc:cn-beijing:xxxxx:services/ai-service'
  WITH
      ROLE_ARN = 'acs:ram::xxxxx:role/AliyunFCInvocationRole',
      CODE_BUCKET = 'your-function-code-bucket';
  ```
  
- [ ] **验证创建成功**
  ```sql
  SHOW CONNECTIONS;
  -- 应该看到 ai_function_conn
  ```

### 步骤 2：上传代码包
- [ ] **上传到 Volume**
  ```sql
  -- 方式1：从本地上传
  PUT 'file:///path/to/clickzetta_ai_functions_full.zip' 
  TO 'volume://code_bucket/ai_functions/v1.0/clickzetta_ai_functions_full.zip';
  
  -- 方式2：从 OSS 复制（如果已上传到 OSS）
  COPY 'oss://your-bucket/clickzetta_ai_functions_full.zip'
  TO 'volume://code_bucket/ai_functions/v1.0/clickzetta_ai_functions_full.zip';
  ```
  
- [ ] **验证上传成功**
  ```sql
  LIST 'volume://code_bucket/ai_functions/';
  -- 应该看到上传的 zip 文件
  ```

### 步骤 3：创建外部函数（分阶段）

#### 阶段 1：测试基础函数
- [ ] **创建测试函数**
  ```sql
  CREATE OR REPLACE EXTERNAL FUNCTION test_echo(message STRING)
  RETURNS STRING
  AS 'volume://code_bucket/ai_functions/v1.0/clickzetta_ai_functions_full.zip'
  CONNECTION = ai_function_conn
  RUNTIME = 'python3.8'
  HANDLER = 'ai_functions_complete.test_echo_impl';
  ```
  
- [ ] **测试函数**
  ```sql
  SELECT test_echo('Hello ClickZetta');
  -- 预期：返回 "Echo: Hello ClickZetta"
  ```

#### 阶段 2：创建核心函数
- [ ] **文本摘要**
  ```sql
  CREATE OR REPLACE EXTERNAL FUNCTION ai_text_summarize(
      text STRING,
      api_key STRING,
      model_name STRING,
      max_length STRING
  )
  RETURNS STRING
  AS 'volume://code_bucket/ai_functions/v1.0/clickzetta_ai_functions_full.zip'
  CONNECTION = ai_function_conn
  RUNTIME = 'python3.8'
  HANDLER = 'ai_functions_complete.ai_text_summarize_impl';
  ```

- [ ] **情感分析**
- [ ] **实体提取**
- [ ] **关键词提取**
- [ ] **文本翻译**

#### 阶段 3：创建所有函数
- [ ] 执行完整的 CREATE FUNCTION 脚本（30个函数）
- [ ] 验证所有函数创建成功
  ```sql
  SHOW FUNCTIONS LIKE 'ai_%';
  -- 应该看到 30 个函数
  ```

### 步骤 4：功能验证

#### 基础验证
- [ ] **测试文本处理函数**
  ```sql
  SELECT ai_text_summarize(
      '这是一段测试文本，用于验证函数是否正常工作。',
      'sk-your-api-key',
      'qwen-turbo',
      '50'
  );
  ```

- [ ] **测试错误处理**
  ```sql
  -- 测试无效 API Key
  SELECT ai_text_summarize('test', 'invalid-key', 'qwen-turbo', '50');
  -- 应该返回错误信息，而不是崩溃
  ```

#### 性能验证
- [ ] **响应时间测试**
  - [ ] 单次调用 < 5 秒
  - [ ] 批量调用正常

- [ ] **数据大小验证**
  - [ ] 一般函数返回 < 5KB
  - [ ] 向量函数返回 20-30KB（正常）

## 🔍 故障排查 Checklist

### 如果函数找不到
- [ ] 检查 Handler 路径是否正确：`模块名.函数名`
- [ ] 检查 ZIP 包是否包含所有文件
- [ ] 检查 Python 版本是否为 3.8
- [ ] 尝试创建简单的 echo 函数测试环境

### 如果 API 调用失败
- [ ] 验证 API Key 是否有效
- [ ] 检查网络连接（VPC、安全组）
- [ ] 确认 API 额度是否充足
- [ ] 查看函数日志获取详细错误

### 如果性能不佳
- [ ] 检查是否在同一地域部署
- [ ] 验证是否有网络延迟
- [ ] 考虑使用更快的模型（qwen-turbo）
- [ ] 检查并发限制设置

## 📊 部署后验证

### 功能完整性测试
- [ ] 运行完整测试套件
  ```bash
  python tests/test_complete_coverage.py $API_KEY
  ```
  
- [ ] 检查测试报告
  - [ ] 成功率 > 90%
  - [ ] 核心功能全部通过

### 生产环境监控
- [ ] 设置函数调用监控
- [ ] 配置错误告警
- [ ] 建立性能基准线
- [ ] 制定回滚方案

## 🎯 最终确认

### 交付物确认
- [ ] 所有 30 个函数可正常调用
- [ ] 文档已更新（包含 Schema 说明）
- [ ] 测试报告已生成
- [ ] 用户指南已提供

### 用户培训
- [ ] 提供 SQL 调用示例
- [ ] 说明 API Key 管理方法
- [ ] 演示常见使用场景
- [ ] 提供故障排查指南

---

## 🚨 重要提醒

1. **API Key 安全**
   - 不要在代码中硬编码 API Key
   - 使用参数传递或安全存储
   - 定期轮换 API Key

2. **成本控制**
   - 监控 API 使用量
   - 使用合适的模型
   - 实施调用频率限制

3. **版本管理**
   - 保留多个版本的 ZIP 包
   - 使用版本号管理函数
   - 记录每次部署的变更

---

*最后更新：2025-06-14*
*版本：v1.0*