# 云器Lakehouse AI Functions 部署检查清单

## 🚨 重要：确保使用最新版本

如果您看到"模拟模式"提示，说明使用的是旧版本的部署包。

## ✅ 部署前检查

### 1. 云平台资源准备
- [ ] **创建ROLE_ARN**（参考[云平台配置指南](./02_CLOUD_PLATFORM_SETUP.md)）
  - 阿里云：RAM角色 + 权限策略
  - 腾讯云：云函数角色
  - AWS：IAM角色
- [ ] **创建CODE_BUCKET**
  - 在对应云存储服务创建Bucket
  - 确保与Lakehouse实例在同一区域
- [ ] **创建API CONNECTION**
  - 使用正确的provider、region、role_arn和code_bucket

### 2. Volume准备
- [ ] **创建存储连接**（如使用外部Volume）
  - 配置正确的endpoint、access_id和access_key
- [ ] **创建Volume**（参考[Volume配置指南](./03_VOLUME_SETUP_GUIDE.md)）
  - 外部Volume：推荐用于生产环境
  - 内部Volume：适用于测试环境
- [ ] **验证Volume访问**
  ```sql
  LIST @volume://external_functions_prod/;
  ```

### 3. 部署文件准备
- [ ] **使用的部署文件**
  - 文件名: `clickzetta_ai_functions_full.zip`
  - 文件大小: 约2.5MB（包含所有依赖）
- [ ] **验证文件信息**
  ```bash
  # 检查文件修改时间和大小
  ls -lh clickzetta_ai_functions_full.zip
  # 应该显示：
  # - 大小约2.5MB（包含所有依赖）
  # - 最新的打包时间（2025-06-14 15:27之后）
  ```

## 📋 部署步骤

1. **上传ZIP包到Volume**
   ```sql
   PUT file://clickzetta_ai_functions_full.zip TO volume://external_functions_prod/;
   ```

2. **执行部署脚本**
   ```sql
   -- 执行 05_AI_FUNCTIONS_DEPLOYMENT_WITH_COMMENTS.sql
   -- 确保所有函数都使用 clickzetta_ai_functions_full.zip
   ```

## 🧪 部署后验证

1. **运行验证脚本**
   ```sql
   -- 执行 10_verify_deployment.sql
   -- 检查是否有"模拟模式"提示
   ```

2. **检查错误处理**
   使用无效的API密钥测试时，应该看到：
   ```json
   {
     "error": true,
     "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."
   }
   ```
   

3. **测试实际功能**
   使用有效的DashScope API密钥：
   ```sql
   SELECT public.ai_text_summarize(
       '您的测试文本内容',
       'sk-xxxxxxxxxxxxxxxx',  -- 真实的API密钥
       'qwen-plus',
       200
   ) as result;
   ```

## 🔍 常见问题

### 问题1：函数找不到
**解决**：使用完整路径 `SELECT public.ai_text_summarize(...)`

### 问题2：DashScope library not available
**解决**：确保ZIP包大小约2.5MB，包含了所有依赖

## 📞 需要帮助？

如果问题持续存在，请检查：
1. 云器Lakehouse版本是否支持Python 3.10+
2. 函数计算服务是否正确配置
3. API连接是否正确创建

---

最后更新：2025-06-14