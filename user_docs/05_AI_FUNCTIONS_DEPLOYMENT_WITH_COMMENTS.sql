-- 云器Lakehouse AI Functions 完整部署脚本（带使用说明）
-- 包含30个生产就绪的AI函数，每个函数都有详细的COMMENT说明
-- 
-- 部署前提条件：
-- 1. 已创建Volume: external_functions_prod
-- 2. 已上传文件: clickzetta_ai_functions_full.zip (2.5MB)
-- 3. 已创建连接: ai_function_connection

-- ⚠️ Schema使用说明：
-- 1. 本脚本示例使用 'public' schema
-- 2. 您可以替换为任何需要的schema名称
-- 3. 调用函数时必须使用相同的schema前缀
-- 4. 例如：CREATE FUNCTION my_schema.ai_text_summarize ...
--        然后调用：SELECT my_schema.ai_text_summarize(...)

-- ==================== 文本处理函数 (8个) ====================

-- 1. 文本摘要生成
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_summarize
AS 'ai_functions_complete.ai_text_summarize'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '生成文本摘要。参数：text(必填)-需要摘要的文本,api_key(必填)-DashScope密钥,model_name(可选,默认qwen-plus)-模型名称,max_length(可选,默认200)-摘要最大字数。返回JSON:{summary:摘要内容,original_length:原文长度,model:使用的模型,timestamp:生成时间}。错误返回:{error:true,message:错误信息}。示例：SELECT public.ai_text_summarize(content,"api-key") FROM articles; SELECT public.ai_text_summarize(content,"api-key","qwen-max",150) FROM docs; 批量处理：SELECT doc_id,json_extract(public.ai_text_summarize(content,"api-key"),"$.summary") as summary FROM documents; 详细文档见docs/FUNCTION_REFERENCE.md';

-- 2. 多语言翻译
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_translate
AS 'ai_functions_complete.ai_text_translate'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '多语言翻译。参数：text(必填)-待翻译文本,target_language(必填)-目标语言(如:英文/日文/法文),api_key(必填)-DashScope密钥,source_language(可选,默认自动检测)-源语言,model_name(可选,默认qwen-plus)。返回JSON:{translated_text:翻译结果,source_language:源语言,target_language:目标语言,model:模型}。示例：SELECT public.ai_text_translate(description,"英文","api-key") FROM products; SELECT public.ai_text_translate(content,"Japanese","api-key","中文") FROM docs; 详见docs/FUNCTION_REFERENCE.md';

-- 3. 情感分析
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_sentiment_analyze
AS 'ai_functions_complete.ai_text_sentiment_analyze'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '情感分析。参数：text(必填)-分析文本,api_key(必填)-DashScope密钥,model_name(可选,默认qwen-plus)。返回JSON:{sentiment:positive/negative/neutral,confidence:置信度,emotions:{joy:0.8,anger:0.1,sadness:0.05,fear:0.05},model:模型}。示例：SELECT public.ai_text_sentiment_analyze(review,"api-key") FROM feedback; SELECT feedback_id,json_extract(public.ai_text_sentiment_analyze(comment,"api-key"),"$.sentiment") as sentiment FROM reviews; 详见docs/FUNCTION_REFERENCE.md';

-- 4. 实体信息提取
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_extract_entities
AS 'ai_functions_complete.ai_text_extract_entities'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '实体信息提取。参数：text(必填)-待提取文本,api_key(必填)-DashScope密钥,entity_types(可选,默认all)-实体类型(all/person/location/organization等),model_name(可选,默认qwen-plus)。返回JSON:{entities:{person:[张三,李四],location:[北京,上海],organization:[云器科技],date:[2025年],number:[100万]},model:模型}。示例：SELECT public.ai_text_extract_entities(news,"api-key","person,organization") FROM articles; 详见docs/FUNCTION_REFERENCE.md';

-- 5. 关键词提取
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_extract_keywords
AS 'ai_functions_complete.ai_text_extract_keywords'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '关键词提取。参数：text(必填)-待提取文本,api_key(必填)-DashScope密钥,max_keywords(可选,默认10)-最多提取数量,model_name(可选,默认qwen-plus)。返回JSON:{keywords:[{word:数据湖,score:0.95},{word:人工智能,score:0.92}],model:模型}。示例：SELECT public.ai_text_extract_keywords(content,"api-key",5) FROM articles; SELECT title,json_extract(public.ai_text_extract_keywords(abstract,"api-key",3),"$.keywords[0].word") as top_keyword FROM papers; 详见docs/FUNCTION_REFERENCE.md';

-- 6. 文本分类
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_classify
AS 'ai_functions_complete.ai_text_classify'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '文本分类。参数：text(必填)-待分类文本,api_key(必填)-DashScope密钥,categories(必填)-类别列表(逗号分隔如:科技,娱乐,体育),model_name(可选,默认qwen-plus)。返回JSON:{category:科技,confidence:0.92,all_scores:{科技:0.92,娱乐:0.05,体育:0.03},model:模型}。示例：SELECT public.ai_text_classify(content,"api-key","科技,金融,教育,娱乐") FROM news; 详见docs/FUNCTION_REFERENCE.md';

-- 7. 文本清洗和标准化
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_clean_normalize
AS 'ai_functions_complete.ai_text_clean_normalize'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '文本清洗标准化。参数：text(必填)-待清洗文本,api_key(必填)-DashScope密钥,operations(可选,默认all)-操作类型(all/remove_html/fix_spacing等),model_name(可选,默认qwen-plus)。返回JSON:{cleaned_text:清洗后文本,operations_applied:[remove_html,fix_spacing],changes_made:15,model:模型}。示例：SELECT public.ai_text_clean_normalize(raw_text,"api-key") FROM documents; 详见docs/FUNCTION_REFERENCE.md';

-- 8. 自动标签生成
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_auto_tag_generate
AS 'ai_functions_complete.ai_auto_tag_generate'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '自动标签生成。参数：text(必填)-待生成标签的文本,api_key(必填)-DashScope密钥,max_tags(可选,默认5)-最多生成标签数,model_name(可选,默认qwen-plus)。返回JSON:{tags:[人工智能,机器学习,数据分析,云计算],model:模型}。示例：SELECT public.ai_auto_tag_generate(content,"api-key",10) FROM articles; SELECT doc_id,public.ai_auto_tag_generate(abstract,"api-key",5) as tags FROM documents; 详见docs/FUNCTION_REFERENCE.md';

-- ==================== 向量处理函数 (5个) ====================

-- 9. 文本转向量嵌入
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_to_embedding
AS 'ai_functions_complete.ai_text_to_embedding'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '文本转向量嵌入。参数：text(必填)-待向量化文本,api_key(必填)-DashScope密钥,model_name(可选,默认text-embedding-v4),dimension(可选,默认auto)-向量维度。返回JSON:{embedding:[0.01,-0.02,...],dimension:1024,model:模型,text_length:256}。示例：CREATE TABLE doc_vectors AS SELECT doc_id,public.ai_text_to_embedding(content,"api-key") as vector FROM docs; 用于语义搜索和相似度计算。详见docs/FUNCTION_REFERENCE.md';

-- 10. 语义相似度计算
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_semantic_similarity
AS 'ai_functions_complete.ai_semantic_similarity'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '语义相似度计算。参数：text1(必填)-第一个文本或向量JSON,text2(必填)-第二个文本或向量JSON,api_key(必填)-DashScope密钥,metric(可选,默认cosine)-度量方式(cosine/euclidean/dot)。返回JSON:{similarity:0.875,metric:cosine,normalized:true}。示例：SELECT public.ai_semantic_similarity(query,document,"api-key") as score FROM corpus; 详见docs/FUNCTION_REFERENCE.md';

-- 11. 文本聚类向量准备
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_text_clustering_prepare
AS 'ai_functions_complete.ai_text_clustering_prepare'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '文本聚类向量准备。参数：texts_json(必填)-文本数组JSON,api_key(必填)-DashScope密钥,model_name(可选,默认text-embedding-v4)。返回JSON:{embeddings:[{text:文本1,vector:[0.01,0.02,...]},{text:文本2,vector:[0.03,0.04,...]}],dimension:1024,count:2}。示例：SELECT public.ai_text_clustering_prepare(json_array_agg(comment),"api-key") FROM reviews GROUP BY category; 详见docs/FUNCTION_REFERENCE.md';

-- 12. 相似文本查找
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_find_similar_text
AS 'ai_functions_complete.ai_find_similar_text'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '相似文本查找。参数：query_text(必填)-查询文本,candidates_json(必填)-候选文本数组JSON,api_key(必填)-DashScope密钥,top_k(可选,默认5)-返回最相似的K个。返回JSON:{results:[{text:相似文本1,similarity:0.95,index:0},{text:相似文本2,similarity:0.88,index:3}]}。示例：SELECT public.ai_find_similar_text("查询内容",json_array_agg(content),"api-key",3) FROM knowledge_base; 详见docs/FUNCTION_REFERENCE.md';

-- 13. 文档语义搜索
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_document_search
AS 'ai_functions_complete.ai_document_search'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '文档语义搜索。参数：query(必填)-搜索查询,documents_json(必填)-文档数组JSON[{id:1,text:内容}],api_key(必填)-DashScope密钥,top_k(可选,默认3)。返回JSON:{results:[{document:文档内容,score:0.92,highlights:[匹配片段1,匹配片段2]}]}。示例：SELECT public.ai_document_search("用户问题",json_array_agg(json_object("id",doc_id,"text",content)),"api-key") FROM docs; 详见docs/FUNCTION_REFERENCE.md';

-- ==================== 多模态处理函数 (8个) ====================

-- 14. 图片描述生成
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_image_describe
AS 'ai_functions_complete.ai_image_describe'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '图片描述生成。参数：image_url(必填)-图片URL,api_key(必填)-DashScope密钥,prompt(可选)-自定义提示词,model_name(可选,默认qwen-vl-plus)。返回JSON:{description:图片描述,objects:[山,雪,天空,树木],scene:自然风景,model:模型}。示例：SELECT public.ai_image_describe(img_url,"api-key") FROM products; SELECT public.ai_image_describe(photo_url,"api-key","详细描述产品特征") FROM catalog; 详见docs/FUNCTION_REFERENCE.md';

-- 15. 图片OCR文字识别
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_image_ocr
AS 'ai_functions_complete.ai_image_ocr'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '图片OCR识别。参数：image_url(必填)-图片URL,api_key(必填)-DashScope密钥,language(可选,默认中英混合)-识别语言,model_name(可选,默认qwen-vl-plus)。返回JSON:{text:识别文字,blocks:[{text:第一段,confidence:0.98},{text:第二段,confidence:0.95}],language:中文,model:模型}。示例：SELECT public.ai_image_ocr(receipt_img,"api-key") FROM invoices; 详见docs/FUNCTION_REFERENCE.md';

-- 16. 图片智能分析
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_image_analyze
AS 'ai_functions_complete.ai_image_analyze'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '图片智能分析。参数：image_url(必填)-图片URL,api_key(必填)-DashScope密钥,analysis_type(可选,默认general)-分析类型(general/objects/scene/people/text),model_name(可选,默认qwen-vl-plus)。返回JSON:{analysis:分析结果,analysis_type:分析类型,image_url:图片地址,model:模型}。示例：SELECT public.ai_image_analyze(photo,"api-key","objects") FROM gallery; 详见docs/FUNCTION_REFERENCE.md';

-- 17. 图片转向量
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_image_to_embedding
AS 'ai_functions_complete.ai_image_to_embedding'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '图片转向量。参数：image_url(必填)-图片URL,api_key(必填)-DashScope密钥,model_name(可选,默认multimodal-embedding-one-peace-v1)。返回JSON:{embedding:[0.1,...],dimension:1024,image_url:图片地址,model:模型}。示例：CREATE TABLE image_vectors AS SELECT img_id,public.ai_image_to_embedding(url,"api-key") as vector FROM images; 用于图片相似搜索。详见docs/FUNCTION_REFERENCE.md';

-- 18. 图片相似度计算
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_image_similarity
AS 'ai_functions_complete.ai_image_similarity'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '图片相似度计算。参数：image_url1(必填)-第一张图片URL,image_url2(必填)-第二张图片URL,api_key(必填)-DashScope密钥,model_name(可选,默认multimodal-embedding-one-peace-v1)。返回JSON:{similarity:0.75,image1:URL1,image2:URL2,model:模型}。示例：SELECT public.ai_image_similarity(img1,img2,"api-key") as similarity FROM image_pairs; 详见docs/FUNCTION_REFERENCE.md';

-- 19. 视频内容摘要
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_video_summarize
AS 'ai_functions_complete.ai_video_summarize'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '视频内容摘要。参数：video_frames_json(必填)-视频帧URL数组JSON,api_key(必填)-DashScope密钥,model_name(可选,默认qwen-vl-plus)。返回JSON:{summary:视频摘要,frame_count:帧数量,model:模型}。示例：SELECT public.ai_video_summarize(json_array(frame1_url,frame2_url,frame3_url),"api-key") FROM videos; 建议提取3-10个关键帧。详见docs/FUNCTION_REFERENCE.md';

-- 20. 图表智能分析
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_chart_analyze
AS 'ai_functions_complete.ai_chart_analyze'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '图表智能分析。参数：chart_image_url(必填)-图表图片URL,api_key(必填)-DashScope密钥,analysis_focus(可选,默认data)-分析重点(data/trend/comparison/insight),model_name(可选,默认qwen-vl-plus)。返回JSON:{analysis:分析结果,focus:分析重点,chart_url:图表地址,model:模型}。示例：SELECT public.ai_chart_analyze(chart_url,"api-key","trend") FROM reports; 详见docs/FUNCTION_REFERENCE.md';

-- 21. 文档智能解析
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_document_parse
AS 'ai_functions_complete.ai_document_parse'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '文档智能解析。参数：doc_images_json(必填)-文档页面图片URL数组JSON,api_key(必填)-DashScope密钥,parse_type(可选,默认structure)-解析类型(structure/content/table/form),model_name(可选,默认qwen-vl-plus)。返回JSON:{parsed_content:解析内容,parse_type:解析类型,page_count:页数,model:模型}。示例：SELECT public.ai_document_parse(json_array(page1,page2),"api-key","table") FROM docs; 详见docs/FUNCTION_REFERENCE.md';

-- ==================== 业务场景函数 (9个) ====================

-- 22. 客户意图分析
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_customer_intent_analyze
AS 'ai_functions_complete.ai_customer_intent_analyze'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '客户意图分析。参数：customer_text(必填)-客户对话文本,api_key(必填)-DashScope密钥,context(可选,默认customer_service)-业务场景,model_name(可选,默认qwen-plus)。返回JSON:{intent:complaint,sub_intents:[refund,quality_issue],urgency:high,sentiment:negative,recommended_action:escalate_to_manager,confidence:0.89}。示例：SELECT public.ai_customer_intent_analyze(feedback,"api-key") FROM tickets; 详见docs/FUNCTION_REFERENCE.md';

-- 23. 销售线索评分
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_sales_lead_score
AS 'ai_functions_complete.ai_sales_lead_score'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '销售线索评分。参数：lead_info(必填)-线索信息JSON,api_key(必填)-DashScope密钥,scoring_model(可选,默认RFM)-评分模型,model_name(可选,默认qwen-plus)。返回JSON:{lead_score:85,rating:A,conversion_probability:0.75,recommendations:[immediate_follow_up,send_product_demo],factors:{budget:90,authority:80,need:85,timeline:85}}。示例：SELECT public.ai_sales_lead_score(json_object("company",company,"budget",budget),"api-key") FROM leads; 详见docs/FUNCTION_REFERENCE.md';

-- 24. 用户评论分析
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_review_analyze
AS 'ai_functions_complete.ai_review_analyze'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '用户评论分析。参数：review_text(必填)-评论文本,api_key(必填)-DashScope密钥,product_type(可选,默认general)-产品类型,model_name(可选,默认qwen-plus)。返回JSON:{sentiment:正面,rating:4.5,aspects:{quality:正面,price:中性,service:负面},keywords:[质量好,价格偏高,服务一般],suggestions:[改善服务态度]}。示例：SELECT public.ai_review_analyze(comment,"api-key","电子产品") FROM reviews; 详见docs/FUNCTION_REFERENCE.md';

-- 25. 风险文本检测
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_risk_text_detect
AS 'ai_functions_complete.ai_risk_text_detect'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '风险文本检测。参数：text(必填)-待检测文本,api_key(必填)-DashScope密钥,risk_types(可选,默认all)-风险类型(all/violence/fraud/sensitive等),model_name(可选,默认qwen-plus)。返回JSON:{risk_level:低/中/高,risk_types:[],risk_details:{},confidence:0.95,safe:true/false}。示例：SELECT content,public.ai_risk_text_detect(content,"api-key") as risk FROM user_posts WHERE status="pending"; 详见docs/FUNCTION_REFERENCE.md';

-- 26. 合同信息提取
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_contract_extract
AS 'ai_functions_complete.ai_contract_extract'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '合同信息提取。参数：contract_text(必填)-合同文本,api_key(必填)-DashScope密钥,extract_fields(可选,默认all)-提取字段(all/parties/amount/date/terms等),model_name(可选,默认qwen-plus)。返回JSON:{parties:[甲方,乙方],amount:100万,date:{start:2025-01-01,end:2025-12-31},terms:[条款1,条款2],obligations:{甲方:[],乙方:[]}}。示例：SELECT public.ai_contract_extract(content,"api-key","parties,amount") FROM contracts; 详见docs/FUNCTION_REFERENCE.md';

-- 27. 简历智能解析
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_resume_parse
AS 'ai_functions_complete.ai_resume_parse'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '简历智能解析。参数：resume_text(必填)-简历文本,api_key(必填)-DashScope密钥,parse_depth(可选,默认standard)-解析深度(basic/standard/detailed),model_name(可选,默认qwen-plus)。返回JSON:{name:张三,experience:5年,skills:[Python,SQL,机器学习],education:[{degree:硕士,school:清华大学}],work_history:[{company:云器科技,position:高级工程师,duration:3年}]}。示例：SELECT public.ai_resume_parse(resume,"api-key","detailed") FROM candidates; 详见docs/FUNCTION_REFERENCE.md';

-- 28. 客户细分分析
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_customer_segment
AS 'ai_functions_complete.ai_customer_segment'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '客户细分分析。参数：customer_data(必填)-客户数据JSON,api_key(必填)-DashScope密钥,segmentation_model(可选,默认RFM)-细分模型(RFM/CLV/behavior等),model_name(可选,默认qwen-plus)。返回JSON:{segment:高价值客户,score:85,characteristics:[购买频繁,金额高,最近活跃],recommendations:[VIP服务,专属优惠],retention_probability:0.9}。示例：SELECT public.ai_customer_segment(json_object("recency",r,"frequency",f,"monetary",m),"api-key") FROM customer_metrics; 详见docs/FUNCTION_REFERENCE.md';

-- 29. 产品描述生成
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_product_description_generate
AS 'ai_functions_complete.ai_product_description_generate'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '产品描述生成。参数：product_info(必填)-产品信息JSON,api_key(必填)-DashScope密钥,style(可选,默认professional)-文案风格(professional/casual/creative/technical),model_name(可选,默认qwen-plus)。返回JSON:{description:产品描述文案,highlights:[亮点1,亮点2],seo_keywords:[关键词1,关键词2],style:professional}。示例：SELECT public.ai_product_description_generate(json_object("name",name,"features",features),"api-key","creative") FROM products; 详见docs/FUNCTION_REFERENCE.md';

-- 30. 行业分类识别
CREATE EXTERNAL FUNCTION IF NOT EXISTS ai_industry_classification
AS 'ai_functions_complete.ai_industry_classification'
USING ARCHIVE 'volume://external_functions_prod/clickzetta_ai_functions_full.zip'
CONNECTION ai_function_connection
WITH PROPERTIES (
    'remote.udf.api' = 'python3.mc.v0',
    'remote.udf.protocol' = 'http.arrow.v0'
)
COMMENT '行业分类识别(原bailian_llm兼容函数)。参数：text(必填)-待分类文本,prompt(必填)-分类提示词,api_key(必填)-DashScope密钥,model_name(必填)-模型名称,temperature(可选,默认0.7),enable_search(可选,默认false)。返回JSON格式分类结果。示例：SELECT public.ai_industry_classification(company_desc,"请根据企业描述判断所属行业，返回JSON格式{一级行业:xxx,二级行业:xxx}","api-key","qwen-plus") FROM companies; 详见docs/FUNCTION_REFERENCE.md';

-- ==================== 部署完成提示 ====================
-- 30个AI函数部署完成！
-- 请确保：
-- 1. 已创建 ai_function_connection 连接
-- 2. 已上传 clickzetta_ai_functions_full.zip 到 volume://external_functions_prod/
-- 3. 拥有有效的DashScope API密钥
-- 
-- 查看函数详情：DESC FUNCTION function_name;
-- 完整文档：docs/FUNCTION_REFERENCE.md