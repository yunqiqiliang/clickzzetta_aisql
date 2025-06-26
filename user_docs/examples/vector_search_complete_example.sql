-- 云器Lakehouse AI Functions 向量搜索完整示例
-- 展示如何结合AI函数实现向量存储和语义搜索

-- ⚠️ 重要提醒：
-- 本示例中所有AI函数调用都使用 'public' schema前缀
-- 请将 'public' 替换为您实际创建函数时使用的schema名称
-- 例如：public.ai_text_to_embedding → your_schema.ai_text_to_embedding

-- ==================== 准备工作 ====================

-- 1. 确保已执行部署脚本
-- 执行: docs/05_AI_FUNCTIONS_DEPLOYMENT_WITH_COMMENTS.sql

-- 2. 创建演示表
-- 执行: docs/12_CREATE_DEMO_TABLES.sql

-- 3. 准备有效的DashScope API密钥
-- 替换所有 'your-api-key' 为实际的API密钥

-- ==================== 向量表创建（如果尚未创建） ====================

CREATE TABLE IF NOT EXISTS aisql_demo_embeddings (
    id INT,
    content_type VARCHAR(50),
    content_id INT,
    title VARCHAR(500),
    content TEXT,
    embedding vector(float, 1024),  -- 1024维向量
    created_date DATE,
    metadata VARCHAR(1000),
    INDEX embedding_idx (embedding) USING vector PROPERTIES (
        'scalar.type' = 'f32',
        'distance.function' = 'cosine_distance',
        'm' = '32',
        'ef.construction' = '256'
    )
) COMMENT = 'AI函数演示：向量存储表（1024维）';

-- ==================== 步骤1：生成向量数据 ====================

-- 清空表（如果需要重新生成）
-- TRUNCATE TABLE aisql_demo_embeddings;

-- 注意：将 'public' 替换为您创建函数时使用的schema

-- 从文章表生成向量
INSERT INTO aisql_demo_embeddings 
SELECT 
    ROW_NUMBER() OVER() as id,
    'article' as content_type,
    article_id as content_id,
    title,
    content,
    CAST(public.ai_text_to_embedding(
        CONCAT(title, ' ', content), 
        'your-api-key',  -- 替换为实际API密钥
        'text-embedding-v4'  -- 1024维模型
    ) AS vector(1024)) as embedding,
    publish_date as created_date,
    JSON_OBJECT('category', category, 'author', author) as metadata
FROM aisql_demo_articles;

-- 从文档表生成向量
INSERT INTO aisql_demo_embeddings 
SELECT 
    (SELECT COALESCE(MAX(id), 0) FROM aisql_demo_embeddings) + ROW_NUMBER() OVER() as id,
    'document' as content_type,
    doc_id as content_id,
    title,
    content,
    CAST(public.ai_text_to_embedding(
        CONCAT(title, ' ', content), 
        'your-api-key',
        'text-embedding-v4'
    ) AS vector(1024)) as embedding,
    created_date,
    JSON_OBJECT('doc_type', doc_type, 'department', department) as metadata
FROM aisql_demo_documents;

-- 从知识库表生成向量
INSERT INTO aisql_demo_embeddings 
SELECT 
    (SELECT COALESCE(MAX(id), 0) FROM aisql_demo_embeddings) + ROW_NUMBER() OVER() as id,
    'knowledge' as content_type,
    kb_id as content_id,
    title,
    content,
    CAST(public.ai_text_to_embedding(
        CONCAT(title, ' ', content), 
        'your-api-key',
        'text-embedding-v4'
    ) AS vector(1024)) as embedding,
    created_date,
    JSON_OBJECT('category', category, 'tags', tags) as metadata
FROM aisql_demo_knowledge_base;

-- 验证数据插入
SELECT content_type, COUNT(*) as count 
FROM aisql_demo_embeddings 
GROUP BY content_type;

-- ==================== 步骤2：基础向量搜索 ====================

-- 设置搜索参数
SET cz.vector.index.search.ef = 128;

-- 2.1 基于查询文本的语义搜索
WITH query_embedding AS (
    SELECT CAST(public.ai_text_to_embedding(
        '如何创建外部函数', 
        'your-api-key',
        'text-embedding-v4'
    ) AS vector(1024)) as query_vec
)
SELECT 
    e.id,
    e.content_type,
    e.title,
    SUBSTRING(e.content, 1, 100) || '...' as content_preview,
    cosine_distance(e.embedding, q.query_vec) as distance,
    ROUND(1 - cosine_distance(e.embedding, q.query_vec), 4) as similarity_score
FROM aisql_demo_embeddings e, query_embedding q
WHERE cosine_distance(e.embedding, q.query_vec) < 0.5
ORDER BY distance
LIMIT 5;

-- 2.2 基于已有内容查找相似文档
WITH target_doc AS (
    SELECT embedding, title
    FROM aisql_demo_embeddings 
    WHERE id = 1  -- 选择第一个文档作为参考
    LIMIT 1
)
SELECT 
    e.id,
    e.title,
    e.content_type,
    ROUND(cosine_distance(e.embedding, t.embedding), 4) as distance,
    ROUND(1 - cosine_distance(e.embedding, t.embedding), 4) as similarity
FROM aisql_demo_embeddings e, target_doc t
WHERE e.id != 1  -- 排除自己
ORDER BY distance
LIMIT 5;

-- ==================== 步骤3：高级搜索场景 ====================

-- 3.1 多条件过滤的向量搜索
WITH query_embedding AS (
    SELECT CAST(public.ai_text_to_embedding(
        '数据分析', 
        'your-api-key',
        'text-embedding-v4'
    ) AS vector(1024)) as query_vec
)
SELECT 
    e.id,
    e.content_type,
    e.title,
    e.created_date,
    JSON_EXTRACT(e.metadata, '$.category') as category,
    ROUND(1 - cosine_distance(e.embedding, q.query_vec), 4) as similarity
FROM aisql_demo_embeddings e, query_embedding q
WHERE cosine_distance(e.embedding, q.query_vec) < 0.6
  AND e.content_type IN ('article', 'document')
  AND e.created_date >= '2025-06-01'
ORDER BY similarity DESC
LIMIT 10;

-- 3.2 相似度分组统计
WITH query_embedding AS (
    SELECT CAST(public.ai_text_to_embedding(
        'AI和机器学习', 
        'your-api-key',
        'text-embedding-v4'
    ) AS vector(1024)) as query_vec
)
SELECT 
    e.content_type,
    COUNT(*) as doc_count,
    ROUND(AVG(1 - cosine_distance(e.embedding, q.query_vec)), 4) as avg_similarity,
    ROUND(MAX(1 - cosine_distance(e.embedding, q.query_vec)), 4) as max_similarity
FROM aisql_demo_embeddings e, query_embedding q
WHERE cosine_distance(e.embedding, q.query_vec) < 0.7
GROUP BY e.content_type
ORDER BY avg_similarity DESC;

-- ==================== 步骤4：实用应用场景 ====================

-- 4.1 智能问答系统
-- 基于问题找到最相关的文档，然后生成答案
WITH user_question AS (
    SELECT 
        '云器Lakehouse如何处理大规模数据？' as question,
        'your-api-key' as api_key
),
question_embedding AS (
    SELECT 
        q.question,
        q.api_key,
        CAST(public.ai_text_to_embedding(
            q.question, 
            q.api_key,
            'text-embedding-v4'
        ) AS vector(1024)) as query_vec
    FROM user_question q
),
relevant_docs AS (
    SELECT 
        e.content,
        e.title,
        ROUND(1 - cosine_distance(e.embedding, q.query_vec), 4) as relevance
    FROM aisql_demo_embeddings e, question_embedding q
    WHERE cosine_distance(e.embedding, q.query_vec) < 0.4
    ORDER BY relevance DESC
    LIMIT 3
)
SELECT 
    q.question as user_question,
    public.ai_text_summarize(
        '基于以下相关文档回答问题：\n\n' || 
        STRING_AGG(
            '文档：' || title || '\n内容：' || content, 
            '\n\n---\n\n'
        ),
        q.api_key,
        'qwen-plus',
        200
    ) as ai_answer,
    STRING_AGG(title || ' (相关度: ' || relevance || ')', '; ') as source_documents
FROM relevant_docs, question_embedding q
GROUP BY q.question, q.api_key;

-- 4.2 内容推荐系统
-- 基于用户正在阅读的内容推荐相似内容
WITH current_reading AS (
    -- 假设用户正在阅读ID为2的文档
    SELECT id, title, embedding
    FROM aisql_demo_embeddings
    WHERE id = 2
),
recommendations AS (
    SELECT 
        e.id,
        e.title,
        e.content_type,
        SUBSTRING(e.content, 1, 100) || '...' as preview,
        ROUND(1 - cosine_distance(e.embedding, r.embedding), 4) as relevance_score
    FROM aisql_demo_embeddings e, current_reading r
    WHERE e.id != r.id
      AND cosine_distance(e.embedding, r.embedding) < 0.3
    ORDER BY relevance_score DESC
    LIMIT 5
)
SELECT 
    '您正在阅读: ' || r.title as current_article,
    '推荐阅读:' as recommendation_header,
    rec.id,
    rec.title,
    rec.content_type,
    rec.preview,
    rec.relevance_score
FROM current_reading r, recommendations rec;

-- 4.3 内容去重检测
-- 查找可能重复或高度相似的内容
WITH similarity_pairs AS (
    SELECT 
        e1.id as id1,
        e1.title as title1,
        e2.id as id2,
        e2.title as title2,
        ROUND(1 - cosine_distance(e1.embedding, e2.embedding), 4) as similarity
    FROM aisql_demo_embeddings e1
    JOIN aisql_demo_embeddings e2 
        ON e1.id < e2.id  -- 避免重复比较
        AND cosine_distance(e1.embedding, e2.embedding) < 0.1  -- 高相似度阈值
)
SELECT 
    id1,
    title1,
    id2,
    title2,
    similarity,
    CASE 
        WHEN similarity > 0.95 THEN '可能重复'
        WHEN similarity > 0.9 THEN '高度相似'
        ELSE '相似'
    END as duplicate_status
FROM similarity_pairs
ORDER BY similarity DESC;

-- ==================== 步骤5：性能优化技巧 ====================

-- 5.1 批量向量生成（推荐用于大数据量）
-- 使用临时表减少重复计算
CREATE TEMPORARY TABLE temp_embeddings AS
SELECT 
    content_id,
    public.ai_text_to_embedding(content, 'your-api-key', 'text-embedding-v4') as embedding_json
FROM (
    SELECT article_id as content_id, CONCAT(title, ' ', content) as content
    FROM aisql_demo_articles
    UNION ALL
    SELECT doc_id + 1000, CONCAT(title, ' ', content)
    FROM aisql_demo_documents
) t;

-- 批量插入
INSERT INTO aisql_demo_embeddings
SELECT 
    ROW_NUMBER() OVER() + (SELECT COALESCE(MAX(id), 0) FROM aisql_demo_embeddings),
    'batch',
    content_id,
    'Batch Import',
    'Batch imported content',
    CAST(embedding_json AS vector(1024)),
    CURRENT_DATE,
    '{}'
FROM temp_embeddings;

-- 5.2 使用近似搜索提高性能
-- 调整搜索参数平衡精度和速度
SET cz.vector.index.search.ef = 32;  -- 降低以提高速度
-- SET cz.vector.index.search.ef = 256;  -- 提高以增加精度

-- 5.3 预计算常用查询的向量
CREATE TABLE IF NOT EXISTS aisql_demo_query_cache (
    query_text VARCHAR(500) PRIMARY KEY,
    query_embedding vector(float, 1024),
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 缓存常用查询
INSERT INTO aisql_demo_query_cache (query_text, query_embedding)
VALUES 
    ('外部函数', CAST(public.ai_text_to_embedding('外部函数', 'your-api-key', 'text-embedding-v4') AS vector(1024))),
    ('数据分析', CAST(public.ai_text_to_embedding('数据分析', 'your-api-key', 'text-embedding-v4') AS vector(1024))),
    ('AI应用', CAST(public.ai_text_to_embedding('AI应用', 'your-api-key', 'text-embedding-v4') AS vector(1024)));

-- 使用缓存的查询向量
SELECT 
    e.id,
    e.title,
    ROUND(1 - cosine_distance(e.embedding, c.query_embedding), 4) as similarity
FROM aisql_demo_embeddings e
JOIN aisql_demo_query_cache c ON c.query_text = '外部函数'
WHERE cosine_distance(e.embedding, c.query_embedding) < 0.5
ORDER BY similarity DESC
LIMIT 10;

-- ==================== 清理（可选） ====================

-- DROP TABLE IF EXISTS aisql_demo_embeddings;
-- DROP TABLE IF EXISTS aisql_demo_query_cache;
-- DROP TABLE IF EXISTS temp_embeddings;