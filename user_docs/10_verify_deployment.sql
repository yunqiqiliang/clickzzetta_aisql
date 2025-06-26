-- 云器Lakehouse AI Functions 部署验证脚本
-- 用于检查函数是否正确部署并包含所有依赖

-- 1. 检查函数是否存在
SHOW FUNCTIONS LIKE '%ai_%';

-- 2. 查看函数详情（以ai_text_summarize为例）
DESC FUNCTION public.ai_text_summarize;

-- 3. 测试函数调用（使用测试API密钥）
-- 注意：这里使用'test-key'会触发错误，正常情况下应该看到：
-- {"error": true, "message": "DashScope library not available..."}
-- 如果看到"模拟模式"，说明使用的是旧版本
SELECT public.ai_text_summarize(
    '这是一个测试文本，用于验证函数部署是否正确。', 
    'test-key'
) as test_result;

-- 4. 解析JSON结果
SELECT 
    json_extract(result, '$.error') as has_error,
    json_extract(result, '$.message') as error_message,
    json_extract(result, '$.note') as note  -- 不应该有这个字段
FROM (
    SELECT public.ai_text_summarize('测试文本', 'test-key') as result
);

-- 5. 验证多个函数
WITH function_tests AS (
    SELECT 'ai_text_summarize' as function_name, 
           public.ai_text_summarize('test', 'test-key') as result
    UNION ALL
    SELECT 'ai_text_translate', 
           public.ai_text_translate('test', '英文', 'test-key')
    UNION ALL
    SELECT 'ai_text_sentiment_analyze', 
           public.ai_text_sentiment_analyze('test', 'test-key')
)
SELECT 
    function_name,
    json_extract(result, '$.error') as has_error,
    CASE 
        WHEN json_extract(result, '$.note') IS NOT NULL THEN '❌ 发现模拟模式（使用了旧版本）'
        WHEN json_extract(result, '$.error') = true THEN '✅ 正确的错误处理'
        ELSE '⚠️ 未知状态'
    END as deployment_status
FROM function_tests;

-- 6. 检查实际使用（需要有效的API密钥）
-- 将 'your-actual-api-key' 替换为真实的DashScope API密钥
/*
SELECT 
    public.ai_text_summarize(
        '云器Lakehouse是一个强大的数据湖仓一体化平台，提供了完整的数据处理和分析能力。', 
        'your-actual-api-key',
        'qwen-plus',
        100
    ) as summary_result;
*/