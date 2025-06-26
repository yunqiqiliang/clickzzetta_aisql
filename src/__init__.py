"""
ClickZetta AI SQL Functions Package
基于百炼大模型的AI SQL函数集合
"""

__version__ = "1.0.0"
__author__ = "ClickZetta Team"

# 导入所有函数类
from .text_functions import *
from .vector_functions import *
from .multimodal_functions import *
from .business_functions import *
from .bailian_llm import get_industry_classification

__all__ = [
    # 文本处理
    'text_to_embedding',
    'batch_text_to_embedding',
    'text_summarize',
    'text_translate',
    'text_sentiment_analyze',
    'text_extract_entities',
    'text_extract_keywords',
    'text_classify',
    'text_clean_normalize',
    'semantic_search',
    
    # 多模态处理
    'image_analyze',
    'image_ocr_extract',
    'image_to_embedding',
    'multimodal_analyze',
    'product_image_analyze',
    'image_caption_generate',
    'visual_question_answer',
    'hybrid_search',
    
    # 业务场景
    'customer_intent_analyze',
    'sales_lead_score',
    'review_analyze',
    'risk_text_detect',
    'contract_extract',
    'resume_parse',
    'faq_match',
    'customer_segment',
    'product_description_generate',
    'marketing_copy_generate',
    'auto_tag_generate',
    'content_moderate',
    
    # 原始实现
    'get_industry_classification',
]