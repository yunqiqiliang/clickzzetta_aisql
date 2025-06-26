# 云器Lakehouse AI Functions 函数参考手册

## 📚 目录

- [文本处理函数](#文本处理函数)
- [向量处理函数](#向量处理函数)
- [多模态处理函数](#多模态处理函数)
- [业务场景函数](#业务场景函数)

---

## 🔤 文本处理函数

### 1. ai_text_summarize - 文本摘要生成

**功能描述**: 对输入文本生成智能摘要

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要摘要的文本内容 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| model_name | STRING | 否 | qwen-plus | 模型名称 |
| max_length | INT | 否 | 200 | 摘要最大长度（字数） |

**返回值**: JSON字符串
```json
{
  "summary": "生成的摘要内容",
  "original_length": 1024,  // 原文长度
  "model": "qwen-plus",     // 使用的模型
  "timestamp": "2025-06-14T10:30:00"  // 生成时间
}
```

**错误返回**:
```json
{
  "error": true,
  "message": "错误描述信息"
}
```

**使用示例**:
```sql
SELECT public.ai_text_summarize(
    content, 
    'your-api-key',
    'qwen-plus',
    150
) as summary_result
FROM documents;
```

---

### 2. ai_text_translate - 多语言翻译

**功能描述**: 将文本翻译成目标语言

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要翻译的文本 |
| target_language | STRING | 是 | - | 目标语言（如：英文、日文、法文等） |
| api_key | STRING | 是 | - | DashScope API密钥 |
| source_language | STRING | 否 | 自动检测 | 源语言 |
| model_name | STRING | 否 | qwen-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "translated_text": "翻译后的文本",
  "source_language": "中文",
  "target_language": "英文",
  "model": "qwen-plus"
}
```

**使用示例**:
```sql
SELECT public.ai_text_translate(
    description,
    '英文',
    'your-api-key'
) as english_version
FROM products;
```

---

### 3. ai_text_sentiment_analyze - 情感分析

**功能描述**: 分析文本的情感倾向和情绪

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要分析的文本 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| model_name | STRING | 否 | qwen-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "sentiment": "positive",     // positive/negative/neutral
  "confidence": 0.95,          // 置信度
  "emotions": {                // 情绪分析
    "joy": 0.8,
    "anger": 0.1,
    "sadness": 0.05,
    "fear": 0.05
  },
  "model": "qwen-plus"
}
```

**使用示例**:
```sql
SELECT 
    feedback_id,
    public.ai_text_sentiment_analyze(feedback_text, 'your-api-key') as sentiment
FROM customer_feedback;
```

---

### 4. ai_text_extract_entities - 实体信息提取

**功能描述**: 从文本中提取人名、地名、组织等实体信息

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要提取实体的文本 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| entity_types | STRING | 否 | all | 实体类型：all/person/location/organization等 |
| model_name | STRING | 否 | qwen-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "entities": {
    "person": ["张三", "李四"],
    "location": ["北京", "上海"],
    "organization": ["云器科技", "阿里云"],
    "date": ["2025年6月14日"],
    "number": ["100万", "50%"]
  },
  "model": "qwen-plus"
}
```

**使用示例**:
```sql
SELECT public.ai_text_extract_entities(
    news_content,
    'your-api-key',
    'person,organization'
) as entities
FROM news_articles;
```

---

### 5. ai_text_extract_keywords - 关键词提取

**功能描述**: 从文本中提取关键词和关键短语

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要提取关键词的文本 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| max_keywords | INT | 否 | 10 | 最多提取的关键词数量 |
| model_name | STRING | 否 | qwen-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "keywords": [
    {"word": "数据湖", "score": 0.95},
    {"word": "人工智能", "score": 0.92},
    {"word": "云计算", "score": 0.88}
  ],
  "model": "qwen-plus"
}
```

**使用示例**:
```sql
SELECT public.ai_text_extract_keywords(
    article_content,
    'your-api-key',
    5
) as top_keywords
FROM articles;
```

---

### 6. ai_text_classify - 文本分类

**功能描述**: 将文本分类到预定义或自定义的类别

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要分类的文本 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| categories | STRING | 是 | - | 类别列表，逗号分隔（如：科技,娱乐,体育） |
| model_name | STRING | 否 | qwen-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "category": "科技",
  "confidence": 0.92,
  "all_scores": {
    "科技": 0.92,
    "娱乐": 0.05,
    "体育": 0.03
  },
  "model": "qwen-plus"
}
```

**使用示例**:
```sql
SELECT public.ai_text_classify(
    content,
    'your-api-key',
    '科技,金融,教育,娱乐,体育'
) as category
FROM news;
```

---

### 7. ai_text_clean_normalize - 文本清洗和标准化

**功能描述**: 清洗和标准化文本，去除噪音和格式化内容

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要清洗的文本 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| operations | STRING | 否 | all | 操作类型：all/remove_html/fix_spacing等 |
| model_name | STRING | 否 | qwen-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "cleaned_text": "清洗后的文本",
  "operations_applied": ["remove_html", "fix_spacing", "normalize_punctuation"],
  "changes_made": 15,
  "model": "qwen-plus"
}
```

---

### 8. ai_auto_tag_generate - 自动标签生成

**功能描述**: 为文本自动生成相关标签

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要生成标签的文本 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| max_tags | INT | 否 | 5 | 最多生成的标签数量 |
| model_name | STRING | 否 | qwen-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "tags": ["人工智能", "机器学习", "数据分析", "云计算"],
  "model": "qwen-plus"
}
```

---

## 🧮 向量处理函数

### 9. ai_text_to_embedding - 文本转向量嵌入

**功能描述**: 将文本转换为向量表示，用于语义搜索和相似度计算

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | STRING | 是 | - | 需要向量化的文本 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| model_name | STRING | 否 | text-embedding-v4 | 嵌入模型名称 |
| dimension | STRING | 否 | auto | 向量维度：auto/1024/768等 |

**返回值**: JSON字符串
```json
{
  "embedding": [0.0123, -0.0456, 0.0789, ...],  // 向量数组
  "dimension": 1024,                             // 向量维度
  "model": "text-embedding-v4",
  "text_length": 256
}
```

**使用示例**:
```sql
-- 创建向量化的表
CREATE TABLE documents_vectors AS
SELECT 
    doc_id,
    public.ai_text_to_embedding(content, 'your-api-key') as content_vector
FROM documents;
```

---

### 10. ai_semantic_similarity - 语义相似度计算

**功能描述**: 计算两个文本或向量之间的语义相似度

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text1 | STRING | 是 | - | 第一个文本或向量JSON |
| text2 | STRING | 是 | - | 第二个文本或向量JSON |
| api_key | STRING | 是 | - | DashScope API密钥 |
| metric | STRING | 否 | cosine | 相似度度量：cosine/euclidean/dot |

**返回值**: JSON字符串
```json
{
  "similarity": 0.875,
  "metric": "cosine",
  "normalized": true
}
```

---

### 11. ai_text_clustering_prepare - 文本聚类向量准备

**功能描述**: 为文本聚类准备向量数据

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| texts_json | STRING | 是 | - | 文本数组的JSON字符串 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| model_name | STRING | 否 | text-embedding-v4 | 模型名称 |

**返回值**: JSON字符串
```json
{
  "embeddings": [
    {"text": "文本1", "vector": [0.01, 0.02, ...]},
    {"text": "文本2", "vector": [0.03, 0.04, ...]}
  ],
  "dimension": 1024,
  "count": 2
}
```

---

### 12. ai_find_similar_text - 相似文本查找

**功能描述**: 在候选文本中查找最相似的内容

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| query_text | STRING | 是 | - | 查询文本 |
| candidates_json | STRING | 是 | - | 候选文本数组的JSON |
| api_key | STRING | 是 | - | DashScope API密钥 |
| top_k | INT | 否 | 5 | 返回最相似的K个结果 |

**返回值**: JSON字符串
```json
{
  "results": [
    {"text": "相似文本1", "similarity": 0.95, "index": 0},
    {"text": "相似文本2", "similarity": 0.88, "index": 3}
  ]
}
```

---

### 13. ai_document_search - 文档语义搜索

**功能描述**: 基于语义理解的文档搜索

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| query | STRING | 是 | - | 搜索查询 |
| documents_json | STRING | 是 | - | 文档数组的JSON |
| api_key | STRING | 是 | - | DashScope API密钥 |
| top_k | INT | 否 | 3 | 返回结果数量 |

**返回值**: JSON字符串
```json
{
  "results": [
    {
      "document": "文档内容",
      "score": 0.92,
      "highlights": ["匹配片段1", "匹配片段2"]
    }
  ]
}
```

---

## 🎨 多模态处理函数

### 14. ai_image_describe - 图片描述生成

**功能描述**: 为图片生成自然语言描述

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| image_url | STRING | 是 | - | 图片URL地址 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| prompt | STRING | 否 | - | 自定义提示词 |
| model_name | STRING | 否 | qwen-vl-plus | 视觉模型名称 |

**返回值**: JSON字符串
```json
{
  "description": "这是一张展示山景的照片，远处是雪山...",
  "objects": ["山", "雪", "天空", "树木"],
  "scene": "自然风景",
  "model": "qwen-vl-plus"
}
```

---

### 15. ai_image_ocr - 图片OCR文字识别

**功能描述**: 从图片中提取文字内容

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| image_url | STRING | 是 | - | 图片URL地址 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| language | STRING | 否 | 中英混合 | 识别语言 |
| model_name | STRING | 否 | qwen-vl-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "text": "识别出的文字内容",
  "blocks": [
    {"text": "第一段文字", "confidence": 0.98},
    {"text": "第二段文字", "confidence": 0.95}
  ],
  "language": "中文",
  "model": "qwen-vl-plus"
}
```

---

### 16-21. 其他多模态函数

包括：
- **ai_image_analyze** - 图片智能分析
- **ai_image_to_embedding** - 图片转向量
- **ai_image_similarity** - 图片相似度计算
- **ai_video_summarize** - 视频内容摘要
- **ai_chart_analyze** - 图表智能分析
- **ai_document_parse** - 文档智能解析

---

## 💼 业务场景函数

### 22. ai_customer_intent_analyze - 客户意图分析

**功能描述**: 分析客户文本中的意图和需求

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| customer_text | STRING | 是 | - | 客户对话或反馈文本 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| context | STRING | 否 | customer_service | 业务场景上下文 |
| model_name | STRING | 否 | qwen-plus | 模型名称 |

**返回值**: JSON字符串
```json
{
  "intent": "complaint",           // 主要意图
  "sub_intents": ["refund", "quality_issue"],
  "urgency": "high",
  "sentiment": "negative",
  "recommended_action": "escalate_to_manager",
  "confidence": 0.89
}
```

---

### 23. ai_sales_lead_score - 销售线索评分

**功能描述**: 对销售线索进行智能评分和分析

**参数说明**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| lead_info | STRING | 是 | - | 线索信息的JSON字符串 |
| api_key | STRING | 是 | - | DashScope API密钥 |
| scoring_model | STRING | 否 | RFM | 评分模型类型 |
| model_name | STRING | 否 | qwen-plus | AI模型名称 |

**返回值**: JSON字符串
```json
{
  "lead_score": 85,
  "rating": "A",
  "conversion_probability": 0.75,
  "recommendations": [
    "immediate_follow_up",
    "send_product_demo"
  ],
  "factors": {
    "budget": 90,
    "authority": 80,
    "need": 85,
    "timeline": 85
  }
}
```

---

### 24-30. 其他业务函数

包括：
- **ai_review_analyze** - 用户评论分析
- **ai_risk_text_detect** - 风险文本检测
- **ai_contract_extract** - 合同信息提取
- **ai_resume_parse** - 简历智能解析
- **ai_customer_segment** - 客户细分分析
- **ai_product_description_generate** - 产品描述生成
- **ai_industry_classification** - 行业分类识别

---

## 🔧 通用说明

### 错误处理

所有函数都遵循统一的错误返回格式：
```json
{
  "error": true,
  "message": "具体错误信息",
  "function": "函数名称",
  "timestamp": "2025-06-14T10:30:00"
}
```

### API密钥

- 所有函数都需要有效的DashScope API密钥
- 建议将API密钥存储在配置表中，避免硬编码
- 示例：
```sql
CREATE TABLE ai_config (
    config_key STRING,
    config_value STRING
);

INSERT INTO ai_config VALUES ('api_key', 'your-secure-api-key');
```

### 模型选择

不同模型的特点和适用场景：

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| qwen-turbo | 快速响应，成本低 | 大批量简单任务 |
| qwen-plus | 平衡性能 | 日常使用推荐 |
| qwen-max | 最高质量 | 复杂任务 |
| qwen-long | 长文本处理 | 文档处理 |
| text-embedding-v4 | 1024维向量 | 语义搜索 |
| qwen-vl-plus | 视觉理解 | 图片分析 |

### 性能优化建议

1. **批量处理**: 尽可能使用批量查询减少API调用
2. **缓存结果**: 对相同输入缓存结果避免重复调用
3. **异步处理**: 大量数据时考虑异步处理模式
4. **模型选择**: 根据任务复杂度选择合适的模型

---

## 📞 技术支持

如需更多帮助，请联系云器Lakehouse技术支持团队。

---

*最后更新：2025年6月14日*