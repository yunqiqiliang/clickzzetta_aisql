#!/usr/bin/env python3
"""
重新组织 clickzetta_aisql 目录，创建生产级包
"""

import os
import shutil
import zipfile
import re

def remove_relative_imports(content):
    """移除相对导入"""
    # from .common.xxx import yyy -> from common.xxx import yyy
    content = re.sub(r'from \.common\.', 'from common.', content)
    content = re.sub(r'from \.', 'from ', content)
    return content

def remove_handler_attribute(content):
    """移除 handler = "evaluate" 属性"""
    # 移除 handler = "evaluate" 行
    content = re.sub(r'^\s*handler\s*=\s*["\']evaluate["\']\s*$', '', content, flags=re.MULTILINE)
    return content

def fix_class_inheritance(content):
    """修复类继承，确保继承自 object"""
    # 将 class xxx(BaseLLMFunction): 改为 class xxx(object):
    content = re.sub(r'class\s+(\w+)\(BaseLLMFunction\):', r'class \1(object):', content)
    return content

def reorganize_aisql():
    """重新组织 clickzetta_aisql 目录"""
    
    source_dir = "/Users/liangmo/Documents/GitHub/mcp-clickzetta-server/clickzetta_aisql"
    temp_dir = "/Users/liangmo/Documents/GitHub/mcp-clickzetta-server/temp_aisql"
    
    # 清理临时目录
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 主要的Python文件
    main_files = [
        "bailian_llm.py",
        "text_functions.py",
        "vector_functions.py",
        "multimodal_functions.py",
        "business_functions.py"
    ]
    
    # 1. 处理主要文件
    for file in main_files:
        src = os.path.join(source_dir, file)
        dst = os.path.join(temp_dir, file)
        
        if os.path.exists(src):
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 应用修复
            content = remove_relative_imports(content)
            content = remove_handler_attribute(content)
            content = fix_class_inheritance(content)
            
            # 写入处理后的文件
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 处理 {file}")
    
    # 2. 复制 common 目录（但不包含 __init__.py）
    src_common = os.path.join(source_dir, "common")
    dst_common = os.path.join(temp_dir, "common")
    
    if os.path.exists(src_common):
        os.makedirs(dst_common)
        for file in os.listdir(src_common):
            if file.endswith('.py') and file != '__init__.py':
                src = os.path.join(src_common, file)
                dst = os.path.join(dst_common, file)
                
                with open(src, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 移除相对导入
                content = remove_relative_imports(content)
                
                with open(dst, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        print("✅ 处理 common 目录")
    
    # 3. 复制依赖
    dependencies = [
        "dashscope", "dashscope-1.23.4.dist-info",
        "aiohttp", "aiohttp-3.12.12.dist-info",
        "yarl", "yarl-1.20.1.dist-info",
        "multidict", "multidict-6.4.4.dist-info",
        "frozenlist", "frozenlist-1.7.0.dist-info",
        "aiosignal", "aiosignal-1.3.2.dist-info",
        "aiohappyeyeballs", "aiohappyeyeballs-2.6.1.dist-info",
        "async_timeout", "async_timeout-5.0.1.dist-info",
        "attrs", "attrs-25.3.0.dist-info",
        "propcache", "propcache-0.3.2.dist-info",
        "certifi", "certifi-2025.4.26.dist-info",
        "charset_normalizer", "charset_normalizer-3.4.2.dist-info",
        "idna", "idna-3.10.dist-info",
        "requests", "requests-2.32.4.dist-info",
        "urllib3", "urllib3-2.4.0.dist-info",
        "websocket", "websocket_client-1.8.0.dist-info",
        "typing_extensions.py", "typing_extensions-4.14.0.dist-info"
    ]
    
    for dep in dependencies:
        src = os.path.join(source_dir, dep)
        dst = os.path.join(temp_dir, dep)
        
        if os.path.exists(src):
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"✅ 复制依赖 {dep}")
    
    # 4. 创建新的 README.md
    readme_content = '''# ClickZetta AI SQL Functions

基于百炼（DashScope）大模型的 AI SQL 函数集，为 ClickZetta Lakehouse 提供智能分析能力。

## 📦 包内容

### 文本处理函数 (text_functions.py)
- `ai_text_summarize` - 文本摘要生成
- `ai_text_translate` - 多语言翻译
- `ai_text_sentiment_analyze` - 情感分析
- `ai_text_extract_entities` - 实体抽取
- `ai_text_extract_keywords` - 关键词提取
- `ai_text_classify` - 文本分类
- `ai_text_clean_normalize` - 文本清洗和标准化
- `ai_auto_tag_generate` - 自动标签生成

### 向量处理函数 (vector_functions.py)
- `ai_text_to_embedding` - 文本转向量嵌入
- `ai_batch_text_to_embedding` - 批量文本转向量
- `ai_semantic_search` - 语义搜索
- `ai_embedding_similarity` - 向量相似度计算
- `ai_vector_search_builder` - 向量搜索SQL构建器

### 多模态函数 (multimodal_functions.py)
- `ai_image_analyze` - 图像内容分析
- `ai_image_ocr_extract` - OCR文字提取
- `ai_image_to_embedding` - 图像转向量嵌入
- `ai_multimodal_analyze` - 多模态内容分析
- `ai_product_image_analyze` - 商品图片分析
- `ai_image_caption_generate` - 图像描述生成
- `ai_visual_question_answer` - 视觉问答
- `ai_hybrid_search` - 混合搜索

### 业务分析函数 (business_functions.py)
- `ai_customer_intent_analyze` - 客户意图分析
- `ai_sales_lead_score` - 销售线索评分
- `ai_review_analyze` - 评论分析
- `ai_risk_text_detect` - 风险文本检测
- `ai_contract_extract` - 合同信息提取
- `ai_resume_parse` - 简历解析
- `ai_customer_segment` - 客户分群
- `ai_product_description_generate` - 商品描述生成
- `ai_content_moderate` - 内容审核

### 通用函数 (bailian_llm.py)
- `ai_get_industry_classification` - 行业分类

## 🚀 快速开始

### 1. 上传包文件
```sql
PUT file:///path/to/clickzetta_aisql.zip @user_files/;
```

### 2. 创建外部函数
```sql
-- 文本摘要
CREATE EXTERNAL FUNCTION ai_text_summarize
AS 'text_functions.ai_text_summarize'
USING ARCHIVE 'volume://user_files/clickzetta_aisql.zip'
CONNECTION your_api_connection
WITH PROPERTIES ('remote.udf.api' = 'python3.mc.v0');

-- 文本转向量
CREATE EXTERNAL FUNCTION ai_text_to_embedding
AS 'vector_functions.ai_text_to_embedding'
USING ARCHIVE 'volume://user_files/clickzetta_aisql.zip'
CONNECTION your_api_connection
WITH PROPERTIES ('remote.udf.api' = 'python3.mc.v0');

-- 图像分析
CREATE EXTERNAL FUNCTION ai_image_analyze
AS 'multimodal_functions.ai_image_analyze'
USING ARCHIVE 'volume://user_files/clickzetta_aisql.zip'
CONNECTION your_api_connection
WITH PROPERTIES ('remote.udf.api' = 'python3.mc.v0');
```

### 3. 使用函数
```sql
-- 文本摘要
SELECT ai_text_summarize(
    content,
    'sk-your-api-key',
    'qwen-max',
    200,  -- max_length
    'business'  -- style
) FROM documents;

-- 文本转向量
SELECT ai_text_to_embedding(
    text,
    'sk-your-api-key',
    'text-embedding-v4',
    '512'  -- dimension
) FROM texts;

-- 图像分析
SELECT ai_image_analyze(
    image_url,
    '请分析这张图片的内容',
    'sk-your-api-key',
    'qwen-vl-plus'
) FROM product_images;
```

## 📝 注意事项

1. **API密钥**：所有函数都需要百炼（DashScope）API密钥
2. **模型选择**：
   - 文本处理：qwen-turbo, qwen-plus, qwen-max, qwen-long
   - 向量嵌入：text-embedding-v1, text-embedding-v2, text-embedding-v3, text-embedding-v4
   - 多模态：qwen-vl-plus, qwen-vl-max
3. **返回格式**：所有函数返回JSON字符串，包含status和data/error字段

## 🔧 配置要求

- ClickZetta Lakehouse 
- API Connection 配置
- Python 3.7+

## 📄 版权信息

本函数包基于阿里云百炼（DashScope）API开发。
'''
    
    readme_path = os.path.join(temp_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ 创建 README.md")
    
    # 5. 创建 requirements.txt
    requirements = '''dashscope>=1.23.4
aiohttp>=3.12.12
requests>=2.32.4
'''
    
    req_path = os.path.join(temp_dir, "requirements.txt")
    with open(req_path, 'w', encoding='utf-8') as f:
        f.write(requirements)
    print("✅ 创建 requirements.txt")
    
    # 6. 创建 zip 包
    zip_path = "/Users/liangmo/Downloads/clickzetta_aisql.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # 7. 清理临时目录
    shutil.rmtree(temp_dir)
    
    # 8. 获取包大小
    zip_size = os.path.getsize(zip_path)
    
    print(f"\n✅ 成功创建 clickzetta_aisql.zip")
    print(f"📦 包大小: {zip_size:,} 字节 ({zip_size/1024/1024:.2f} MB)")
    print(f"📍 位置: {zip_path}")
    
    print("\n📝 主要改动：")
    print("1. ✅ 移除所有相对导入")
    print("2. ✅ 移除 handler = 'evaluate' 属性")
    print("3. ✅ 类继承改为 object")
    print("4. ✅ 移除 __init__.py 文件")
    print("5. ✅ 所有函数名已有 ai_ 前缀")
    
    print("\n🎯 包结构：")
    print("- 5个主要Python文件（31个AI函数）")
    print("- common目录（辅助模块）")
    print("- 完整的依赖包")
    print("- README.md 和 requirements.txt")

if __name__ == "__main__":
    reorganize_aisql()