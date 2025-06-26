# Volume 配置指南

本指南详细说明如何在云器Lakehouse中创建和配置Volume用于存储AI函数部署包。

## 📋 Volume类型选择

### 内部Volume vs 外部Volume

| 特性 | 内部Volume | 外部Volume |
|------|------------|------------|
| 存储位置 | Lakehouse内部管理 | 云存储（OSS/COS/S3） |
| 成本 | 计入Lakehouse存储费用 | 由云存储服务商计费 |
| 适用场景 | 测试、小规模部署 | 生产环境、大规模部署 |
| 跨区域访问 | 受限 | 灵活（需同云服务商） |
| 配置复杂度 | 简单 | 需要存储连接配置 |

## 🔧 创建内部Volume

### 简单创建
```sql
CREATE VOLUME external_functions_prod
    DIRECTORY = (ENABLE = true)
    COMMENT = 'AI函数部署包存储';
```

### 完整选项
```sql
CREATE VOLUME IF NOT EXISTS external_functions_prod
    DIRECTORY = (
        ENABLE = true,
        AUTO_REFRESH = true
    )
    RECURSIVE = true
    COMMENT = 'AI函数部署包存储（内部）';
```

## 🔧 创建外部Volume

### 步骤1：创建存储连接

#### 阿里云OSS
```sql
CREATE STORAGE CONNECTION aliyun_oss_conn
    TYPE oss
    ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'
    ACCESS_ID = 'LTAI5txxxxxxxxxxxxxx'
    ACCESS_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYxxxxxx';
```

**Endpoint选择**：
- 华东1（杭州）：`oss-cn-hangzhou.aliyuncs.com`
- 华东2（上海）：`oss-cn-shanghai.aliyuncs.com`
- 华北2（北京）：`oss-cn-beijing.aliyuncs.com`
- 华南1（深圳）：`oss-cn-shenzhen.aliyuncs.com`
- 新加坡：`oss-ap-southeast-1.aliyuncs.com`

#### 腾讯云COS
```sql
CREATE STORAGE CONNECTION tencent_cos_conn
    TYPE COS
    ACCESS_KEY = 'AKIDxxxxxxxxxxxxxx'
    SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxx'
    REGION = 'ap-shanghai'
    APP_ID = '1310000503';
```

**Region选择**：
- 上海：`ap-shanghai`
- 北京：`ap-beijing`
- 广州：`ap-guangzhou`
- 成都：`ap-chengdu`
- 新加坡：`ap-singapore`

#### AWS S3
```sql
CREATE STORAGE CONNECTION aws_s3_conn
    TYPE S3
    ACCESS_KEY = 'AKIAxxxxxxxxxxxxxx'
    SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    ENDPOINT = 's3.cn-north-1.amazonaws.com.cn'
    REGION = 'cn-north-1';
```

**中国区Endpoint**：
- 北京：`s3.cn-north-1.amazonaws.com.cn`
- 宁夏：`s3.cn-northwest-1.amazonaws.com.cn`

**国际区Endpoint**：
- 新加坡：`s3.ap-southeast-1.amazonaws.com`
- 东京：`s3.ap-northeast-1.amazonaws.com`

### 步骤2：创建外部Volume

#### 基础创建
```sql
CREATE EXTERNAL VOLUME external_functions_prod
    LOCATION 'oss://ai-functions-bucket/deployment/'
    USING CONNECTION aliyun_oss_conn;
```

#### 完整选项
```sql
CREATE EXTERNAL VOLUME IF NOT EXISTS external_functions_prod
    LOCATION 'oss://ai-functions-bucket/deployment/'
    USING CONNECTION aliyun_oss_conn
    DIRECTORY = (
        ENABLE = true,        -- 启用目录功能
        AUTO_REFRESH = true   -- 自动刷新目录
    )
    RECURSIVE = true          -- 递归扫描子目录
    COMMENT = 'AI函数部署包存储（阿里云OSS）';
```

## 📁 Volume路径规范

### 云存储路径格式

| 云服务商 | 路径格式 | 示例 |
|----------|----------|------|
| 阿里云OSS | `oss://bucket-name/path/` | `oss://ai-functions/prod/` |
| 腾讯云COS | `cos://bucket-appid/path/` | `cos://ai-func-1310000503/prod/` |
| AWS S3 | `s3://bucket-name/path/` | `s3://ai-functions/deployment/` |
| Google GCS | `gs://bucket-name/path/` | `gs://ai-functions/prod/` |

### 注意事项
1. 路径必须以 `/` 结尾
2. Bucket名称必须全局唯一
3. 腾讯云COS需要包含APP_ID
4. 避免使用特殊字符和中文

## 🔐 权限配置

### Volume权限类型
- **CREATE VOLUME**：创建Volume权限
- **READ VOLUME**：读取文件和列出目录
- **WRITE VOLUME**：上传和删除文件
- **ALTER VOLUME**：修改Volume配置

### 授权示例
```sql
-- 授予用户创建Volume权限
GRANT CREATE VOLUME ON SCHEMA public TO USER 'deploy_user';

-- 授予读写权限
GRANT READ, WRITE ON VOLUME external_functions_prod TO USER 'app_user';

-- 授予角色完整权限
GRANT ALL ON VOLUME external_functions_prod TO ROLE 'admin_role';
```

## 📋 Volume操作

### 查看Volume信息
```sql
-- 查看Volume详情
DESC VOLUME external_functions_prod;

-- 列出所有Volume
SHOW VOLUMES;

-- 列出Volume中的文件
LIST @volume://external_functions_prod/;
```

### 文件操作
```sql
-- 上传文件
PUT file://local_file.zip TO volume://external_functions_prod/;

-- 下载文件
GET volume://external_functions_prod/file.zip TO file://local_path/;

-- 删除文件
REMOVE @volume://external_functions_prod/old_file.zip;
```

### Volume维护
```sql
-- 刷新目录元数据
ALTER VOLUME external_functions_prod REFRESH;

-- 修改注释
ALTER VOLUME external_functions_prod SET COMMENT = '新的描述';

-- 删除Volume（谨慎操作）
DROP VOLUME external_functions_prod;
```

## ⚡ 最佳实践

### 1. 命名规范
- 使用有意义的名称：`external_functions_prod`、`ai_models_dev`
- 避免使用特殊字符和空格
- 使用下划线分隔单词

### 2. 安全建议
- 定期轮换存储连接的Access Key
- 使用最小权限原则
- 避免在SQL中硬编码敏感信息

### 3. 性能优化
- 外部Volume适合大文件存储
- 启用AUTO_REFRESH提高目录访问速度
- 合理设置RECURSIVE避免不必要的扫描

### 4. 成本控制
- 生产环境使用外部Volume降低成本
- 定期清理不需要的文件
- 选择合适的存储类型（标准/低频/归档）

## 🚨 常见问题

### Q: 跨云访问失败
A: 云器Lakehouse实例与存储必须在同一云服务商。例如，阿里云上的Lakehouse实例无法访问腾讯云COS。

### Q: 文件上传大小限制
A: 单个文件上传限制为5GB。超过此限制需要使用分片上传或其他工具。

### Q: Volume创建失败
A: 检查：
1. 存储连接是否正确创建
2. Access Key是否有效
3. Bucket是否存在
4. 网络是否可达

### Q: 权限不足错误
A: 确保：
1. 用户有CREATE VOLUME权限
2. 存储连接的密钥有相应bucket权限
3. Volume路径正确

## 📚 相关文档

- [云器Lakehouse Volume管理](https://www.yunqi.tech/documents)
- [CREATE STORAGE CONNECTION语法](../docs/clickzetta_product_doc/create-storage-connection.md)
- [CREATE EXTERNAL VOLUME语法](../docs/clickzetta_product_doc/external-Volume.md)
- [Volume权限管理](../docs/clickzetta_product_doc/datalake_privilege.md)