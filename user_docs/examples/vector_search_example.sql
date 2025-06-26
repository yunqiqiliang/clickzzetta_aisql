-- ClickZetta AI SQL 向量搜索示例

-- 1. 创建包含向量字段的表
CREATE TABLE documents (
    id INT,
    title STRING,
    content STRING,
    content_embedding ARRAY<DOUBLE>,  -- 文本向量字段
    created_at TIMESTAMP
);

-- 2. 使用text_to_embedding函数生成向量并插入数据
INSERT INTO documents VALUES (
    1,
    'ClickZetta产品介绍', 
    'ClickZetta是新一代云原生数据湖仓',
    PARSE_JSON(text_to_embedding('ClickZetta是新一代云原生数据湖仓', 'your_api_key')).embedding,
    CURRENT_TIMESTAMP()
);

-- 3. 语义搜索示例
WITH search_query AS (
    SELECT PARSE_JSON(semantic_search(
        '数据湖仓产品',  -- 查询文本
        'content_embedding',  -- 向量字段名
        'documents',  -- 表名
        10,  -- top_k
        0.7,  -- 相似度阈值
        'your_api_key'
    )) as search_result
)
SELECT 
    d.*,
    cosine_similarity(d.content_embedding, search_query.search_result.query_embedding) as similarity_score
FROM documents d, search_query
WHERE cosine_similarity(d.content_embedding, search_query.search_result.query_embedding) > 0.7
ORDER BY similarity_score DESC
LIMIT 10;

-- 4. 批量向量化示例
WITH batch_texts AS (
    SELECT PARSE_JSON(batch_text_to_embedding(
        '["文本1", "文本2", "文本3"]',
        'your_api_key'
    )) as batch_result
)
SELECT 
    texts.value as original_text,
    embeddings.value as embedding_vector
FROM batch_texts,
LATERAL FLATTEN(input => PARSE_JSON('["文本1", "文本2", "文本3"]'), outer => true) texts,
LATERAL FLATTEN(input => batch_texts.batch_result.embeddings, outer => true) embeddings
WHERE texts.index = embeddings.index;

-- 5. 混合检索示例（向量+关键词）
SELECT 
    d.*,
    (0.7 * cosine_similarity(d.content_embedding, :query_vector) + 
     0.3 * CASE WHEN d.content ILIKE '%数据湖%' OR d.content ILIKE '%仓库%' THEN 1.0 ELSE 0.0 END
    ) as combined_score
FROM documents d
WHERE combined_score > 0.5
ORDER BY combined_score DESC
LIMIT 20;