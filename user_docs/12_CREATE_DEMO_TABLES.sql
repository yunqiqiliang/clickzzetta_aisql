-- 云器Lakehouse AI Functions 演示表创建脚本
-- 创建文档示例中使用的所有演示表
-- 所有表名都带有 aisql_demo_ 前缀，方便识别和清理

-- ⚠️ 使用说明：
-- 1. 本脚本创建的是演示表，用于测试AI函数
-- 2. 请在您的测试schema中执行（如public或test）
-- 3. 完成测试后可以使用 DROP TABLE 批量删除
-- 4. 表中包含了示例数据，可以直接用于函数测试

-- ==================== 第一部分：创建基础演示表 ====================

-- 1. 文章表 (用于文本处理函数测试)
CREATE TABLE IF NOT EXISTS aisql_demo_articles (
    article_id INT,
    title VARCHAR(500),
    content TEXT,
    author VARCHAR(100),
    publish_date DATE,
    category VARCHAR(50),
    tags VARCHAR(200),
    language VARCHAR(20) DEFAULT '中文'
) COMMENT = 'AI函数演示：文章表';

-- 2. 产品表 (用于多语言翻译和标签生成测试)
CREATE TABLE IF NOT EXISTS aisql_demo_products (
    product_id INT,
    name VARCHAR(200),
    description TEXT,
    category VARCHAR(100),
    price DECIMAL(10,2),
    brand VARCHAR(100),
    language VARCHAR(20) DEFAULT '中文',
    status VARCHAR(20)
) COMMENT = 'AI函数演示：产品表';

-- 3. 文档表 (用于文档搜索和相似度计算测试)
CREATE TABLE IF NOT EXISTS aisql_demo_documents (
    doc_id INT,
    title VARCHAR(500),
    content TEXT,
    doc_type VARCHAR(50),
    created_date DATE,
    author VARCHAR(100),
    department VARCHAR(100),
    file_size INT
) COMMENT = 'AI函数演示：文档表';

-- 4. 知识库表 (用于向量搜索和知识问答测试)
CREATE TABLE IF NOT EXISTS aisql_demo_knowledge_base (
    kb_id INT,
    title VARCHAR(500),
    content TEXT,
    category VARCHAR(100),
    tags VARCHAR(500),
    created_by VARCHAR(100),
    created_date DATE,
    view_count INT,
    is_public BOOLEAN
) COMMENT = 'AI函数演示：知识库表';

-- 5. 用户反馈表 (用于情感分析测试)
CREATE TABLE IF NOT EXISTS aisql_demo_feedback (
    feedback_id INT,
    user_id INT,
    product_id INT,
    rating INT,
    review TEXT,
    feedback_date DATE,
    platform VARCHAR(50),
    verified_purchase BOOLEAN
) COMMENT = 'AI函数演示：用户反馈表';

-- 6. 评论表 (用于评论分析测试)
CREATE TABLE IF NOT EXISTS aisql_demo_reviews (
    review_id INT,
    item_id INT,
    item_type VARCHAR(50),
    user_name VARCHAR(100),
    rating DECIMAL(2,1),
    comment TEXT,
    review_date DATE,
    helpful_count INT,
    verified BOOLEAN
) COMMENT = 'AI函数演示：评论表';

-- 7. 客户分析表 (用于业务分析函数测试)
CREATE TABLE IF NOT EXISTS aisql_demo_customer_analysis (
    analysis_id INT,
    customer_id INT,
    interaction_date DATE,
    channel VARCHAR(50),
    message TEXT,
    emotion VARCHAR(50),
    customer_intent VARCHAR(100),
    resolved BOOLEAN,
    agent_id INT,
    satisfaction_score INT
) COMMENT = 'AI函数演示：客户分析表';

-- ==================== 第二部分：插入示例数据 ====================

-- 插入文章数据
INSERT INTO aisql_demo_articles VALUES
(1, '云器Lakehouse助力企业数字化转型', '随着大数据时代的到来，企业面临着海量数据的存储、处理和分析挑战。云器Lakehouse作为新一代数据湖仓一体化平台，通过统一的架构实现了数据湖的灵活性和数据仓库的高性能。本文将详细介绍云器Lakehouse如何帮助企业构建现代化的数据基础设施，实现数据驱动的业务创新。主要内容包括：1）湖仓一体架构的优势；2）实时数据处理能力；3）AI与大数据的融合；4）成功案例分享。', '张明', '2025-06-10', '技术', '大数据,湖仓一体,数字化转型', '中文'),
(2, 'AI驱动的智能客服系统设计与实现', '本文介绍了一个基于深度学习的智能客服系统的设计与实现。系统采用了最新的大语言模型技术，结合知识图谱和向量检索，能够准确理解用户意图并提供个性化的服务。文章详细阐述了系统架构、核心算法、工程实现以及在实际业务中的应用效果。通过A/B测试，该系统将客户满意度提升了35%，问题解决率达到92%。', '李华', '2025-06-12', '人工智能', 'AI,客服系统,深度学习,NLP', '中文'),
(3, 'Building Modern Data Pipeline with Cloud Technologies', 'This article explores the best practices for building scalable data pipelines using cloud-native technologies. We discuss the architecture patterns, tool selection, and optimization strategies for handling petabyte-scale data processing. Key topics include: stream processing, batch processing, data quality, and cost optimization.', 'John Smith', '2025-06-08', 'Technology', 'Data Engineering,Cloud,Pipeline', '英文');

-- 插入产品数据
INSERT INTO aisql_demo_products VALUES
(1, '智能音箱Pro', '这款智能音箱采用了最新的AI语音识别技术，支持多轮对话和场景理解。内置高品质扬声器，提供360度环绕立体声。支持智能家居控制，可以连接超过1000种智能设备。具备儿童模式和隐私保护功能。', '电子产品', 599.00, 'TechBrand', '中文', 'active'),
(2, '超薄笔记本电脑', '14英寸4K触控屏，Intel最新处理器，16GB内存，512GB固态硬盘。重量仅1.2kg，续航可达15小时。支持快速充电，30分钟充电80%。预装正版操作系统和办公软件。', '电子产品', 5999.00, 'CompTech', '中文', 'active'),
(3, '智能手表运动版', '专为运动爱好者设计，支持50米防水，内置GPS和心率监测。可追踪20多种运动模式，提供专业的运动数据分析。电池续航7天，支持移动支付和消息提醒。', '可穿戴设备', 1299.00, 'SportTech', '中文', 'active');

-- 插入文档数据
INSERT INTO aisql_demo_documents VALUES
(1, '云器Lakehouse外部函数开发指南', '本指南详细介绍了如何在云器Lakehouse中开发和部署外部函数。内容包括：1）外部函数的基本概念；2）Python UDF开发规范；3）函数注册和部署流程；4）最佳实践和常见问题。通过本指南，开发者可以快速掌握外部函数的开发技巧。', '技术文档', '2025-06-01', '技术部', '研发中心', 25600),
(2, '2025年Q2季度业务分析报告', '本报告全面分析了公司2025年第二季度的业务表现。主要亮点：1）营收同比增长45%；2）新客户获取成本降低20%；3）客户满意度提升至95%；4）市场份额扩大3个百分点。报告还包含了详细的数据分析和未来展望。', '业务报告', '2025-06-30', '分析部', '战略规划部', 45000),
(3, '数据安全管理制度v2.0', '为保障公司数据资产安全，特制定本管理制度。主要内容：1）数据分类分级标准；2）数据访问权限管理；3）数据加密和脱敏要求；4）数据备份和恢复流程；5）安全事件应急响应。所有员工必须严格遵守本制度。', '制度文档', '2025-05-15', '安全部', '信息安全中心', 18900);

-- 插入知识库数据
INSERT INTO aisql_demo_knowledge_base VALUES
(1, '如何使用云器Lakehouse创建外部函数', '创建外部函数的步骤：1）准备Python代码，使用@annotate装饰器；2）打包成ZIP文件；3）上传到Volume；4）使用CREATE EXTERNAL FUNCTION语句创建函数；5）测试函数功能。注意事项：确保Python版本兼容，处理好依赖关系。', 'technical', '外部函数,Python,UDF,开发指南', '技术支持', '2025-05-20', 156, true),
(2, 'AI函数最佳实践：文本处理优化技巧', '在使用AI文本处理函数时，可以通过以下方式优化性能：1）批量处理而非逐条处理；2）合理设置模型参数；3）使用缓存避免重复计算；4）选择合适的模型规模。实测表明，批量处理可以提升5倍性能。', 'best-practice', 'AI函数,性能优化,文本处理,最佳实践', '架构师', '2025-06-05', 89, true),
(3, '向量数据库与语义搜索实战', '本文介绍如何结合云器Lakehouse和向量数据库实现语义搜索：1）文本向量化的原理；2）向量相似度计算方法；3）构建语义搜索系统；4）优化检索性能。包含完整的代码示例和性能测试结果。', 'tutorial', '向量数据库,语义搜索,embedding,相似度计算', '数据科学家', '2025-06-10', 234, true);

-- 插入用户反馈数据
INSERT INTO aisql_demo_feedback VALUES
(1, 1001, 1, 5, '非常满意！音质超出预期，语音识别准确率很高，能听懂方言。智能家居控制功能很实用，设置简单。孩子也很喜欢，儿童模式内容丰富且健康。强烈推荐！', '2025-06-11', '官网', true),
(2, 1002, 2, 4, '笔记本很轻薄，适合经常出差使用。性能满足日常办公需求，屏幕显示效果出色。唯一不足是在高负载时风扇声音有点大，希望后续能优化。', '2025-06-09', '电商平台', true),
(3, 1003, 3, 2, '功能是挺多的，但是APP体验不好，经常连接不稳定。运动数据统计有时不准确，GPS定位偏差较大。电池续航也没有宣传的那么长，实际使用只有4-5天。', '2025-06-13', '社交媒体', false),
(4, 1004, 1, 5, '给父母买的，他们很喜欢。语音交互很自然，老人家也能轻松使用。音质清晰，听戏曲效果很好。客服响应及时，解决问题很专业。', '2025-06-14', '官网', true);

-- 插入评论数据
INSERT INTO aisql_demo_reviews VALUES
(1, 101, '餐厅', '美食爱好者', 4.5, '环境优雅，菜品精致，特别推荐他们的招牌菜。服务态度很好，上菜速度适中。价格略高但物有所值。已经去过三次了，每次都有不错的体验。', '2025-06-10', 45, true),
(2, 102, '酒店', '商旅客', 3.0, '位置不错，交通方便。但是房间隔音效果差，晚上能听到隔壁的声音。早餐种类一般，没有什么特色。前台服务还可以，入住退房都比较快。', '2025-06-08', 12, true),
(3, 103, '景点', '旅游达人', 5.0, '非常值得一去！风景壮美，空气清新。建议早上去，人少景美，可以拍到很好的照片。门票价格合理，景区管理规范。带老人小孩都很合适。', '2025-06-12', 89, true);

-- 插入客户分析数据
INSERT INTO aisql_demo_customer_analysis VALUES
(1, 2001, '2025-06-10', '在线客服', '你好，我购买的产品出现了质量问题，屏幕有划痕，要求退换货。订单号是2025061012345。', 'negative', 'complaint', true, 101, 4),
(2, 2002, '2025-06-11', '电话', '想了解一下你们的企业版方案，我们公司有500人左右，需要什么样的配置？价格是多少？', 'neutral', 'inquiry', true, 102, 5),
(3, 2003, '2025-06-12', '邮件', '非常感谢贵公司的优质服务！产品使用体验很好，客服响应也很及时。希望能有更多优惠活动。', 'positive', 'feedback', false, 103, 5),
(4, 2004, '2025-06-13', '社交媒体', '系统登录不了，一直提示密码错误，但我确定密码是对的。已经试了好几次了，很着急！', 'negative', 'technical_support', true, 104, 3);

-- ==================== 第三部分：创建向量表 ====================

-- 8. 向量存储表 (用于向量搜索和相似度计算)
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

-- ==================== 第四部分：创建视图 ====================

-- 创建一个联合视图，方便测试跨表分析
CREATE VIEW IF NOT EXISTS aisql_demo_content_analysis AS
SELECT 
    'article' as content_type,
    article_id as content_id,
    title,
    content,
    author as creator,
    publish_date as created_date
FROM aisql_demo_articles
UNION ALL
SELECT 
    'document' as content_type,
    doc_id as content_id,
    title,
    content,
    author as creator,
    created_date
FROM aisql_demo_documents
UNION ALL
SELECT 
    'knowledge' as content_type,
    kb_id as content_id,
    title,
    content,
    created_by as creator,
    created_date
FROM aisql_demo_knowledge_base;

-- ==================== 第五部分：使用示例 ====================

-- 示例1：测试文本摘要功能
/*
-- 注意：将 'public' 替换为您创建函数时使用的schema
SELECT 
    article_id,
    title,
    public.ai_text_summarize(content, 'your-api-key', 'qwen-plus', 100) as summary
FROM aisql_demo_articles;
*/

-- 示例2：测试情感分析功能
/*
-- 注意：将 'public' 替换为您创建函数时使用的schema
SELECT 
    feedback_id,
    rating,
    public.ai_text_sentiment_analyze(review, 'your-api-key') as sentiment_analysis
FROM aisql_demo_feedback;
*/

-- 示例3：测试多语言翻译功能
/*
-- 注意：将 'public' 替换为您创建函数时使用的schema
SELECT 
    product_id,
    name,
    public.ai_text_translate(description, '英文', 'your-api-key') as english_description
FROM aisql_demo_products
WHERE language = '中文';
*/

-- 示例4：生成向量数据
/*
-- 注意：需要先确保AI函数已部署，并有有效的API密钥
-- 注意：将 'public' 替换为您创建函数时使用的schema
INSERT INTO aisql_demo_embeddings 
SELECT 
    ROW_NUMBER() OVER() as id,
    'article' as content_type,
    article_id as content_id,
    title,
    content,
    CAST(public.ai_text_to_embedding(
        CONCAT(title, ' ', content), 
        'your-api-key',
        'text-embedding-v4'  -- 使用1024维的模型
    ) AS vector(1024)) as embedding,
    publish_date as created_date,
    JSON_OBJECT('category', category, 'author', author) as metadata
FROM aisql_demo_articles;
*/

-- 示例5：向量搜索
/*
-- 设置搜索参数以优化性能
SET cz.vector.index.search.ef = 128;

-- 搜索与查询文本最相似的内容
-- 注意：将 'public' 替换为您创建函数时使用的schema
WITH query_embedding AS (
    SELECT CAST(public.ai_text_to_embedding(
        '如何使用云器Lakehouse创建外部函数', 
        'your-api-key',
        'text-embedding-v4'
    ) AS vector(1024)) as query_vec
)
SELECT 
    e.id,
    e.content_type,
    e.title,
    SUBSTRING(e.content, 1, 200) as content_preview,
    cosine_distance(e.embedding, q.query_vec) as distance,
    1 - cosine_distance(e.embedding, q.query_vec) as similarity_score
FROM aisql_demo_embeddings e, query_embedding q
WHERE cosine_distance(e.embedding, q.query_vec) < 0.5  -- 距离阈值
ORDER BY distance
LIMIT 10;
*/

-- 更多向量搜索示例请参考：docs/examples/vector_search_complete_example.sql

-- ==================== 第六部分：清理脚本 ====================

-- 如需删除所有演示表，执行以下语句：
/*
DROP TABLE IF EXISTS aisql_demo_articles;
DROP TABLE IF EXISTS aisql_demo_products;
DROP TABLE IF EXISTS aisql_demo_documents;
DROP TABLE IF EXISTS aisql_demo_knowledge_base;
DROP TABLE IF EXISTS aisql_demo_feedback;
DROP TABLE IF EXISTS aisql_demo_reviews;
DROP TABLE IF EXISTS aisql_demo_customer_analysis;
DROP TABLE IF EXISTS aisql_demo_embeddings;
DROP VIEW IF EXISTS aisql_demo_content_analysis;
*/