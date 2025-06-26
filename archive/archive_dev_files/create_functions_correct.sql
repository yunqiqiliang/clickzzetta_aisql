-- ClickZetta AI SQL Functions - 正确的创建语法
-- 注意：HANDLER 必须是 '模块名.类名' 格式

-- 1. 文本向量化函数
DROP FUNCTION IF EXISTS text_to_embedding;
CREATE EXTERNAL FUNCTION text_to_embedding(
    text STRING, 
    api_key STRING, 
    model_name STRING, 
    dimension STRING
) 
RETURNS STRING
HANDLER = 'vector_functions.text_to_embedding'  -- 正确格式：模块名.类名
PACKAGES = ('volume://user_files/clickzetta_aisql_v1.0.1_fixed.zip');

-- 2. 图像分析函数
DROP FUNCTION IF EXISTS image_analyze;
CREATE EXTERNAL FUNCTION image_analyze(
    image_url STRING, 
    question STRING, 
    api_key STRING, 
    model_name STRING
) 
RETURNS STRING
HANDLER = 'multimodal_functions.image_analyze'  -- 正确格式：模块名.类名
PACKAGES = ('volume://user_files/clickzetta_aisql_v1.0.1_fixed.zip');

-- 3. 客户意图分析函数
DROP FUNCTION IF EXISTS customer_intent_analyze;
CREATE EXTERNAL FUNCTION customer_intent_analyze(
    customer_text STRING, 
    business_context STRING, 
    api_key STRING, 
    model_name STRING
)
RETURNS STRING
HANDLER = 'business_functions.customer_intent_analyze'  -- 正确格式：模块名.类名
PACKAGES = ('volume://user_files/clickzetta_aisql_v1.0.1_fixed.zip');

-- 4. 行业分类函数
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
HANDLER = 'bailian_llm.get_industry_classification'  -- 正确格式：模块名.类名
PACKAGES = ('volume://user_files/clickzetta_aisql_v1.0.1_fixed.zip');

-- 5. 文本摘要函数
DROP FUNCTION IF EXISTS text_summarize;
CREATE EXTERNAL FUNCTION text_summarize(
    text STRING,
    api_key STRING,
    model_name STRING,
    max_length INT
)
RETURNS STRING
HANDLER = 'text_functions.text_summarize'  -- 正确格式：模块名.类名
PACKAGES = ('volume://user_files/clickzetta_aisql_v1.0.1_fixed.zip');

-- 测试函数
-- SELECT text_to_embedding('测试文本', 'your_api_key', 'text-embedding-v4', 'auto');