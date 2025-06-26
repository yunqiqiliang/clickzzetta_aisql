-- ClickZetta AI SQL 函数测试脚本
-- 用于验证修复后的handler问题

-- 1. 首先上传修复后的ZIP文件到volume
-- PUT FILE 'file:///Users/liangmo/Downloads/clickzetta_aisql.zip' @volume://user_files/;

-- 2. 创建文本向量化函数（测试基本功能）
CREATE OR REPLACE EXTERNAL FUNCTION text_to_embedding (
    text STRING,
    api_key STRING,
    model_name STRING DEFAULT 'text-embedding-v4',
    dimension STRING DEFAULT 'auto'
) 
RETURNS STRING
HANDLER = 'clickzetta_aisql.vector_functions.text_to_embedding'
IMPORTS = ('@volume://user_files/clickzetta_aisql.zip')
CONNECTION = (CONNECTION_NAME = 'mcp_test_api_conn')
COMMENT = '文本向量化 - 已修复handler属性';

-- 3. 测试调用
SELECT text_to_embedding(
    'ClickZetta是新一代云原生数据湖仓平台',
    'your_api_key_here'
) as embedding_result;

-- 4. 创建更多函数进行测试
-- 文本摘要
CREATE OR REPLACE EXTERNAL FUNCTION text_summarize (
    text STRING,
    max_length INT DEFAULT 200,
    style STRING DEFAULT 'concise',
    api_key STRING,
    model_name STRING DEFAULT 'qwen-plus'
) 
RETURNS STRING
HANDLER = 'clickzetta_aisql.text_functions.text_summarize'
IMPORTS = ('@volume://user_files/clickzetta_aisql.zip')
CONNECTION = (CONNECTION_NAME = 'mcp_test_api_conn')
COMMENT = '文本摘要 - 已修复handler属性';

-- 图像分析
CREATE OR REPLACE EXTERNAL FUNCTION image_analyze (
    image_url STRING,
    question STRING DEFAULT '请分析这张图片',
    api_key STRING,
    model_name STRING DEFAULT 'qwen-vl-plus'
) 
RETURNS STRING
HANDLER = 'clickzetta_aisql.multimodal_functions.image_analyze'
IMPORTS = ('@volume://user_files/clickzetta_aisql.zip')
CONNECTION = (CONNECTION_NAME = 'mcp_test_api_conn')
COMMENT = '图像分析 - 已修复handler属性';

-- 客户意图分析
CREATE OR REPLACE EXTERNAL FUNCTION customer_intent_analyze (
    customer_text STRING,
    business_context STRING DEFAULT 'general',
    api_key STRING,
    model_name STRING DEFAULT 'qwen-plus'
) 
RETURNS STRING
HANDLER = 'clickzetta_aisql.business_functions.customer_intent_analyze'
IMPORTS = ('@volume://user_files/clickzetta_aisql.zip')
CONNECTION = (CONNECTION_NAME = 'mcp_test_api_conn')
COMMENT = '客户意图分析 - 已修复handler属性';

-- 5. 批量测试所有函数类型
-- 测试文本处理
SELECT text_summarize(
    '人工智能正在改变我们的生活方式。从智能家居到自动驾驶，从医疗诊断到金融分析，AI技术已经深入到社会的各个角落。',
    100,
    'concise',
    'your_api_key_here'
) as summary;

-- 测试图像分析（需要提供真实的图片URL）
SELECT image_analyze(
    'https://example.com/product_image.jpg',
    '这是什么产品？请描述它的特征',
    'your_api_key_here'
) as image_analysis;

-- 测试客户意图
SELECT customer_intent_analyze(
    '我想了解你们的产品价格，最近有什么优惠活动吗？',
    'sales',
    'your_api_key_here'
) as intent_analysis;

-- 6. 验证handler是否正确工作
-- 如果函数创建成功且能调用，说明handler问题已解决