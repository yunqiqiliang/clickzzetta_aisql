-- ClickZetta AI SQL Functions - 基于原始可工作版本的正确语法
-- 使用 clickzetta_aisql_working.zip

-- 1. 行业分类函数（原始版本）
DROP FUNCTION IF EXISTS get_industry_classification;
CREATE EXTERNAL FUNCTION get_industry_classification(
    text STRING,
    prompt STRING,
    api_key STRING,
    model_name STRING,
    temperature DOUBLE,
    enable_search BOOLEAN
)
RETURNS STRING
HANDLER = 'bailian_llm.get_industry_classification'
PACKAGES = ('volume://user_files/clickzetta_aisql_working.zip');

-- 2. 文本向量化函数
DROP FUNCTION IF EXISTS text_to_embedding;
CREATE EXTERNAL FUNCTION text_to_embedding(
    text STRING, 
    api_key STRING, 
    model_name STRING, 
    dimension STRING
) 
RETURNS STRING
HANDLER = 'vector_functions.text_to_embedding'
PACKAGES = ('volume://user_files/clickzetta_aisql_working.zip');

-- 3. 图像分析函数
DROP FUNCTION IF EXISTS image_analyze;
CREATE EXTERNAL FUNCTION image_analyze(
    image_url STRING, 
    question STRING, 
    api_key STRING, 
    model_name STRING
) 
RETURNS STRING
HANDLER = 'multimodal_functions.image_analyze'
PACKAGES = ('volume://user_files/clickzetta_aisql_working.zip');

-- 4. 客户意图分析函数
DROP FUNCTION IF EXISTS customer_intent_analyze;
CREATE EXTERNAL FUNCTION customer_intent_analyze(
    customer_text STRING, 
    business_context STRING, 
    api_key STRING, 
    model_name STRING
)
RETURNS STRING
HANDLER = 'business_functions.customer_intent_analyze'
PACKAGES = ('volume://user_files/clickzetta_aisql_working.zip');

-- 5. 文本摘要函数
DROP FUNCTION IF EXISTS text_summarize;
CREATE EXTERNAL FUNCTION text_summarize(
    text STRING,
    api_key STRING,
    model_name STRING,
    max_length INT
)
RETURNS STRING
HANDLER = 'text_functions.text_summarize'
PACKAGES = ('volume://user_files/clickzetta_aisql_working.zip');

-- 测试语句
/*
-- 测试行业分类
SELECT get_industry_classification(
    '云器科技是一家专注于云原生数据湖仓的创新企业',
    '请对这段描述进行行业分类，返回JSON格式：{"一级行业": "xxx", "二级行业": "xxx"}',
    'your_api_key',
    'qwen-plus',
    0.7,
    false
);

-- 测试文本向量化
SELECT text_to_embedding(
    'ClickZetta是新一代云原生数据湖仓', 
    'your_api_key',
    'text-embedding-v4',
    'auto'
);
*/