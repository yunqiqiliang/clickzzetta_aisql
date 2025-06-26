"""
ClickZetta AI Functions Complete Package V2
修复流式响应累积问题的版本
保持与原始bailian_llm.py相同的处理逻辑
"""

import os
import json
import sys
from datetime import datetime

# 模拟装饰器（用于本地测试）
def annotate(signature):
    def decorator(cls):
        cls._signature = signature
        return cls
    return decorator

try:
    from cz.udf import annotate
except ImportError:
    pass

# 模拟HTTP状态
try:
    from http import HTTPStatus
except ImportError:
    class HTTPStatus:
        OK = 200

# 检测dashscope可用性
try:
    import dashscope
    HAS_DASHSCOPE = True
except ImportError:
    HAS_DASHSCOPE = False

# ==================== 文本处理函数 (8个) ====================

@annotate("*->string")
class ai_text_summarize(object):
    def evaluate(self, text, api_key, model_name="qwen-plus", max_length=200):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"你是专业的文本摘要专家。请将文本总结为不超过{max_length}字的摘要。"},
            {"role": "user", "content": text}
        ]
        
        try:
            # 重要：对于SQL环境，使用非流式调用更稳定
            response = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=False,  # 改为非流式
                result_format='message',
                temperature=0.7,
                top_p=0.8
            )
            
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
                else:
                    full_content = ""
            else:
                return json.dumps({
                    "error": True,
                    "message": f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
                }, ensure_ascii=False)
            
            result = {
                "summary": full_content, 
                "original_length": len(text), 
                "model": model_name, 
                "timestamp": datetime.now().isoformat()
            }
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_text_translate(object):
    def evaluate(self, text, target_language, api_key, model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"你是专业翻译专家，请将文本翻译成{target_language}。"},
            {"role": "user", "content": text}
        ]
        
        try:
            response = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=False,  # 非流式
                result_format='message',
                temperature=0.3,
                top_p=0.8
            )
            
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
                else:
                    full_content = ""
            else:
                return json.dumps({
                    "error": True,
                    "message": f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
                }, ensure_ascii=False)
            
            result = {
                "translated_text": full_content, 
                "original_text": text, 
                "target_language": target_language, 
                "model": model_name
            }
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_text_sentiment_analyze(object):
    def evaluate(self, text, api_key, model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        
        # 明确的JSON格式要求
        prompt = """分析文本情感，返回JSON格式：
{
  "sentiment": "positive/negative/neutral",
  "confidence": 0.0-1.0,
  "emotions": {
    "joy": 0.0-1.0,
    "anger": 0.0-1.0,
    "sadness": 0.0-1.0,
    "fear": 0.0-1.0
  }
}"""
        
        messages = [
            {"role": "system", "content": "你是专业情感分析专家。" + prompt},
            {"role": "user", "content": f"分析情感：{text}"}
        ]
        
        try:
            response = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=False,  # 非流式
                result_format='message',
                temperature=0.1,
                top_p=0.8
            )
            
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
                else:
                    full_content = ""
            else:
                return json.dumps({
                    "error": True,
                    "message": f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
                }, ensure_ascii=False)
            
            # 尝试解析JSON
            try:
                # 清理可能的markdown标记
                import re
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                json_match = re.search(json_pattern, full_content)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = json.loads(full_content)
            except:
                result = {"sentiment_analysis": full_content}
            
            result["model"] = model_name
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_text_extract_entities(object):
    def evaluate(self, text, api_key, entity_types="all", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": "你是专业信息提取专家，从文本中提取实体信息，返回JSON格式。"},
            {"role": "user", "content": f"提取实体（类型：{entity_types}）：{text}"}
        ]
        
        try:
            response = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=False,  # 非流式
                result_format='message',
                temperature=0.2,
                top_p=0.8
            )
            
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
                else:
                    full_content = ""
            else:
                return json.dumps({
                    "error": True,
                    "message": f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
                }, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"entities": full_content}
            result["model"] = model_name
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

# 后续函数省略，都采用相同的非流式调用模式...