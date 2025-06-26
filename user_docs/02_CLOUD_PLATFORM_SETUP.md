# 云平台配置指南

本指南详细说明如何在不同云平台上配置创建API CONNECTION所需的资源。

## 🔧 阿里云配置

### 1. 创建ROLE_ARN

#### 步骤1：创建权限策略

**A. 函数计算权限策略**
1. 登录[阿里云RAM控制台](https://ram.console.aliyun.com)
2. 进入 **权限管理** > **权限策略**
3. 搜索并选择 `AliyunFCFullAccess`
4. 如需自定义，可编辑策略文档：

```json
{
    "Version": "1",
    "Statement": [
        {
            "Action": "fc:*",
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Action": "ram:PassRole",
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "acs:Service": "fc.aliyuncs.com"
                }
            }
        }
    ]
}
```

**B. OSS访问权限策略**
1. 创建新的权限策略（如 `CzUdfOssAccess`）
2. 选择"脚本编辑"
3. 替换 `your-bucket-name` 为实际的bucket名称：

```json
{
    "Version": "1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "oss:GetObject",
                "oss:ListObjects",
                "oss:PutObject",
                "oss:DeleteObject"
            ],
            "Resource": [
                "acs:oss:*:*:your-bucket-name",
                "acs:oss:*:*:your-bucket-name/*"
            ]
        }
    ]
}
```

#### 步骤2：创建角色

1. 进入 **身份管理** > **角色**
2. 点击 **创建角色**
3. 选择类型：**阿里云账号**
4. 选择 **其他云账号**
5. 输入云器Lakehouse的阿里云账号ID：`1384322691904283`
6. 角色名称：如 `CzUDFRole`
7. 为角色授权：
   - 系统策略：`AliyunFCFullAccess`
   - 自定义策略：`CzUdfOssAccess`

#### 步骤3：获取Role ARN

创建完成后，在角色详情页可以看到ARN，格式如下：
```
acs:ram::您的账号ID:role/CzUDFRole
```

### 2. 创建CODE_BUCKET

1. 登录[阿里云OSS控制台](https://oss.console.aliyun.com)
2. 创建新的Bucket：
   - Bucket名称：如 `function-compute-prod`
   - 地域：选择与函数计算相同的地域
   - 存储类型：标准存储
   - 读写权限：私有

### 3. 创建API CONNECTION

```sql
CREATE API CONNECTION ai_function_connection
TYPE CLOUD_FUNCTION
PROVIDER='aliyun'
REGION='cn-hangzhou'
ROLE_ARN='acs:ram::您的账号ID:role/CzUDFRole'
CODE_BUCKET='function-compute-prod';
```

### 4. 配置External ID（可选但推荐）

1. 创建连接后，执行：
```sql
DESC CONNECTION ai_function_connection;
```

2. 记录返回的 `external_id`

3. 返回RAM控制台，编辑角色的信任策略，添加External ID条件：
```json
{
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "RAM": [
                    "acs:ram::1384322691904283:root"
                ]
            },
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "您的external_id"
                }
            }
        }
    ],
    "Version": "1"
}
```

## 🔧 腾讯云配置

### 1. 创建云函数权限

1. 登录[腾讯云访问管理控制台](https://console.cloud.tencent.com/cam)
2. 创建角色，选择"腾讯云产品服务"
3. 选择"云函数"作为角色载体
4. 授予所需权限策略

### 2. 配置COS存储桶

1. 登录[腾讯云COS控制台](https://console.cloud.tencent.com/cos)
2. 创建存储桶用于存放函数代码

### 3. 创建API CONNECTION

```sql
CREATE API CONNECTION ai_function_connection
TYPE CLOUD_FUNCTION
PROVIDER='tencent'
REGION='ap-shanghai'
NAMESPACE='default'  -- 腾讯云需要指定命名空间
ROLE_ARN='qcs::cam::uin/您的账号ID:roleName/您的角色名'
CODE_BUCKET='function-code-bucket';
```

## 🔧 AWS配置

### 1. 创建IAM角色

1. 登录[AWS IAM控制台](https://console.aws.amazon.com/iam)
2. 创建角色，选择"AWS服务"
3. 选择"Lambda"作为使用案例
4. 附加以下权限策略：
   - AWSLambdaExecute
   - S3访问权限（自定义）

### 2. 创建S3存储桶

1. 登录[AWS S3控制台](https://console.aws.amazon.com/s3)
2. 创建存储桶用于存放函数代码
3. 确保存储桶与Lambda在同一地域

### 3. 创建API CONNECTION

```sql
CREATE API CONNECTION ai_function_connection
TYPE CLOUD_FUNCTION
PROVIDER='aws'
REGION='ap-southeast-1'
ROLE_ARN='arn:aws:iam::您的账号ID:role/您的角色名'
CODE_BUCKET='lambda-function-code';
```

## 📋 检查清单

无论使用哪个云平台，请确保完成以下检查：

- [ ] 已创建具有必要权限的角色/RAM角色
- [ ] 已创建用于存放代码的存储桶
- [ ] 角色有权访问存储桶
- [ ] 已获取正确的Role ARN格式
- [ ] 已选择正确的地域（Region）
- [ ] （可选）已配置External ID以增强安全性

## 🌐 支持的地域

| 云平台 | 地域 | Region代码 |
|--------|------|------------|
| 阿里云 | 华东2（上海） | cn-shanghai |
| 阿里云 | 新加坡 | ap-southeast-1 |
| 腾讯云 | 华东（上海） | ap-shanghai |
| 腾讯云 | 华北（北京） | ap-beijing |
| 腾讯云 | 华南（广州） | ap-guangzhou |
| AWS | 北京 | cn-north-1 |
| AWS | 新加坡 | ap-southeast-1 |

## ❓ 常见问题

### Q: 为什么需要信任云器Lakehouse的账号？
A: 云器Lakehouse需要通过角色扮演来代表您执行函数，因此需要建立信任关系。

### Q: External ID是什么？
A: External ID是一个额外的安全措施，确保只有知道这个ID的服务才能扮演您的角色。

### Q: 如何验证配置是否正确？
A: 创建连接后，可以通过上传简单的测试函数来验证配置是否正确。

## 📚 更多资源

- [云器Lakehouse官方文档](https://www.yunqi.tech/documents)
- [阿里云函数计算文档](https://help.aliyun.com/product/50980.html)
- [腾讯云云函数文档](https://cloud.tencent.com/document/product/583)
- [AWS Lambda文档](https://docs.aws.amazon.com/lambda/)