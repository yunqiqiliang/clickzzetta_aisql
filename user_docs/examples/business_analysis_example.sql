-- ClickZetta AI SQL 业务分析示例

-- 1. 客户意图分析
SELECT 
    customer_id,
    message,
    PARSE_JSON(customer_intent_analyze(
        message, 
        'e-commerce',  -- 业务场景
        'your_api_key'
    )) as intent_analysis
FROM customer_messages
WHERE created_at >= CURRENT_DATE() - INTERVAL 7 DAY;

-- 2. 销售线索评分
SELECT 
    lead_id,
    company_name,
    contact_info,
    PARSE_JSON(sales_lead_score(
        OBJECT_CONSTRUCT(
            'company', company_name,
            'industry', industry,
            'budget', estimated_budget,
            'urgency', urgency_level,
            'contact_role', contact_role
        ),
        NULL,  -- 使用默认评分标准
        'your_api_key'
    )) as lead_score
FROM sales_leads
ORDER BY PARSE_JSON(sales_lead_score(...)).total_score DESC;

-- 3. 产品评论分析
SELECT 
    product_id,
    review_text,
    PARSE_JSON(review_analyze(
        review_text,
        'electronics',  -- 产品类型
        'your_api_key'
    )) as review_analysis
FROM product_reviews
WHERE created_at >= CURRENT_DATE() - INTERVAL 30 DAY;

-- 4. 文本风险检测
SELECT 
    content_id,
    user_content,
    PARSE_JSON(risk_text_detect(
        user_content,
        'compliance,sensitive_info',  -- 风险类型
        'finance',  -- 行业
        'your_api_key'
    )) as risk_assessment
FROM user_generated_content
WHERE PARSE_JSON(risk_text_detect(...)).risk_level != 'low';

-- 5. 合同信息提取
SELECT 
    contract_id,
    PARSE_JSON(contract_extract(
        contract_text,
        'parties,amount,dates,terms',  -- 提取字段
        'your_api_key'
    )) as extracted_info
FROM legal_contracts
WHERE contract_status = 'pending_review';

-- 6. 简历解析
SELECT 
    applicant_id,
    resume_text,
    PARSE_JSON(resume_parse(
        resume_text,
        'detailed',  -- 解析深度
        'your_api_key'
    )) as parsed_resume
FROM job_applications
WHERE application_date >= CURRENT_DATE() - INTERVAL 7 DAY;

-- 7. 客户细分分析
WITH customer_data AS (
    SELECT 
        customer_id,
        OBJECT_CONSTRUCT(
            'age', age,
            'income', annual_income,
            'purchase_frequency', purchase_count_last_year,
            'total_spent', total_amount_last_year,
            'last_purchase_date', last_purchase_date,
            'preferred_categories', preferred_product_categories
        ) as customer_profile
    FROM customer_profiles
)
SELECT 
    customer_id,
    PARSE_JSON(customer_segment(
        customer_profile,
        'RFM',  -- 细分模型
        'your_api_key'
    )) as segmentation_result
FROM customer_data;

-- 8. 产品描述生成
SELECT 
    product_id,
    PARSE_JSON(product_description_generate(
        OBJECT_CONSTRUCT(
            'name', product_name,
            'category', category,
            'features', key_features,
            'price', price,
            'target_market', target_audience
        ),
        'professional',  -- 风格
        'tech_enthusiasts',  -- 目标受众
        'your_api_key'
    )) as generated_description
FROM products
WHERE description IS NULL OR LENGTH(description) < 100;

-- 9. 内容审核
SELECT 
    post_id,
    content,
    PARSE_JSON(content_moderate(
        content,
        'standard',  -- 审核级别
        'social_media',  -- 平台类型
        'your_api_key'
    )) as moderation_result
FROM user_posts
WHERE moderation_status = 'pending'
AND PARSE_JSON(content_moderate(...)).moderation_result.approved = false;