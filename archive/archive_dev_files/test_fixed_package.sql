-- 测试修复后的包创建外部函数
-- 使用正确的handler路径格式

-- 1. 创建文本向量化函数
CREATE OR REPLACE EXTERNAL FUNCTION text_to_embedding(text STRING, api_key STRING, model_name STRING, dimension STRING)
RETURNS STRING
HANDLER = 'clickzetta_aisql.vector_functions.text_to_embedding'
PACKAGES = ('{你的URL}/clickzetta_aisql_fixed.zip');

-- 2. 测试创建一个业务函数
CREATE OR REPLACE EXTERNAL FUNCTION customer_intent_analyze(customer_text STRING, business_context STRING, api_key STRING, model_name STRING)
RETURNS STRING
HANDLER = 'clickzetta_aisql.business_functions.customer_intent_analyze'
PACKAGES = ('{你的URL}/clickzetta_aisql_fixed.zip');

-- 3. 测试多模态函数
CREATE OR REPLACE EXTERNAL FUNCTION image_analyze(image_url STRING, question STRING, api_key STRING, model_name STRING)
RETURNS STRING
HANDLER = 'clickzetta_aisql.multimodal_functions.image_analyze'
PACKAGES = ('{你的URL}/clickzetta_aisql_fixed.zip');

-- 测试查询
-- SELECT text_to_embedding('测试文本', 'your-api-key', 'text-embedding-v4', 'auto');