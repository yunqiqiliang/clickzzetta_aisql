-- ClickZetta AI SQL 多模态处理示例

-- 1. 图片分析
SELECT 
    image_id,
    image_url,
    PARSE_JSON(image_analyze(
        image_url,
        '请分析这张图片',  -- 分析问题
        'your_api_key'
    )) as image_analysis
FROM product_images
WHERE analysis_status = 'pending';

-- 2. OCR文字提取
SELECT 
    document_id,
    scan_url,
    PARSE_JSON(image_ocr_extract(
        scan_url,
        'invoice',  -- 提取类型：发票
        'your_api_key'
    )) as ocr_result
FROM scanned_documents
WHERE document_type = 'invoice';

-- 3. 图片向量化和相似度搜索
WITH query_image AS (
    SELECT PARSE_JSON(image_to_embedding(
        'https://example.com/query_image.jpg',
        'your_api_key'
    )) as query_vector
)
SELECT 
    pi.product_id,
    pi.image_url,
    cosine_similarity(
        pi.image_embedding, 
        query_image.query_vector.embedding
    ) as similarity_score
FROM product_images pi, query_image
WHERE cosine_similarity(pi.image_embedding, query_image.query_vector.embedding) > 0.8
ORDER BY similarity_score DESC
LIMIT 10;

-- 4. 商品图片分析
SELECT 
    product_id,
    main_image_url,
    PARSE_JSON(product_image_analyze(
        main_image_url,
        'category,features,quality',  -- 分析方面
        'your_api_key'
    )) as product_analysis
FROM products
WHERE category = 'fashion'
AND main_image_url IS NOT NULL;

-- 5. 图片标题生成
SELECT 
    photo_id,
    photo_url,
    PARSE_JSON(image_caption_generate(
        photo_url,
        'creative',  -- 标题风格
        'medium',    -- 长度
        'your_api_key'
    )) as caption_data
FROM user_photos
WHERE caption IS NULL;

-- 6. 视觉问答
SELECT 
    image_id,
    question,
    PARSE_JSON(visual_question_answer(
        image_url,
        question,
        context_info,  -- 背景信息
        'your_api_key'
    )) as answer_data
FROM image_qa_tasks
WHERE status = 'pending';

-- 7. 多模态内容分析
WITH multimodal_content AS (
    SELECT 
        content_id,
        JSON_OBJECT(
            'images', ARRAY_CONSTRUCT(image_url_1, image_url_2),
            'text', description_text,
            'prompt', '请对比分析这些图片和文本的一致性'
        ) as content_data
    FROM marketing_materials
)
SELECT 
    content_id,
    PARSE_JSON(multimodal_analyze(
        content_data,
        'verify',  -- 任务类型：验证
        'your_api_key'
    )) as analysis_result
FROM multimodal_content;

-- 8. 混合模态检索
WITH hybrid_query AS (
    SELECT JSON_OBJECT(
        'text', '红色连衣裙',
        'image', 'https://example.com/red_dress.jpg',
        'weights', JSON_OBJECT('text', 0.6, 'image', 0.4),
        'table_name', 'fashion_products',
        'text_field', 'description_embedding',
        'image_field', 'image_embedding',
        'threshold', 0.7,
        'top_k', 20
    ) as query_config
)
SELECT 
    PARSE_JSON(hybrid_search(
        query_config,
        'your_api_key'
    )) as search_config
FROM hybrid_query;

-- 9. 批量图片分析
SELECT 
    batch_id,
    image_urls,
    PARSE_JSON(multimodal_analyze(
        JSON_OBJECT(
            'images', SPLIT(image_urls, ','),
            'task', 'compare'
        ),
        'compare',  -- 对比分析
        'your_api_key'
    )) as batch_analysis
FROM image_batches
WHERE processing_status = 'queued';

-- 10. 图文一致性检查
SELECT 
    ad_id,
    ad_text,
    ad_image_url,
    PARSE_JSON(visual_question_answer(
        ad_image_url,
        CONCAT('这张图片是否与以下文本描述一致？文本：', ad_text),
        '广告内容审核',
        'your_api_key'
    )) as consistency_check
FROM advertisements
WHERE review_status = 'pending';