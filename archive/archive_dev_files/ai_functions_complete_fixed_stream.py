"""
ClickZetta AI Functions - 修复流式响应累积问题
保持流式调用，但智能处理累积响应
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

# ==================== 文本处理函数 (修复版) ====================

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
            responses = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=True,
                result_format='message',
                temperature=0.7,
                top_p=0.8
            )
            
            # 智能处理流式响应
            full_content = ""
            last_chunk = ""
            
            for response in responses:
                if response.status_code == HTTPStatus.OK:
                    if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                        if hasattr(response.output.choices[0].message, 'content'):
                            content = response.output.choices[0].message.content
                            if content:
                                # 检查是否为累积响应
                                if last_chunk and last_chunk in content:
                                    # 这是累积响应，提取新增部分
                                    new_part = content[len(last_chunk):]
                                    full_content += new_part
                                    last_chunk = content
                                elif full_content and full_content in content:
                                    # 整个响应包含了之前的所有内容，直接使用
                                    full_content = content
                                    last_chunk = content
                                else:
                                    # 正常的增量响应
                                    full_content += content
                                    last_chunk = content
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
            responses = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=True,
                result_format='message',
                temperature=0.3,
                top_p=0.8
            )
            
            # 智能处理流式响应
            full_content = ""
            last_chunk = ""
            
            for response in responses:
                if response.status_code == HTTPStatus.OK:
                    if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                        if hasattr(response.output.choices[0].message, 'content'):
                            content = response.output.choices[0].message.content
                            if content:
                                # 检查是否为累积响应
                                if last_chunk and last_chunk in content:
                                    # 这是累积响应，提取新增部分
                                    new_part = content[len(last_chunk):]
                                    full_content += new_part
                                    last_chunk = content
                                elif full_content and full_content in content:
                                    # 整个响应包含了之前的所有内容，直接使用
                                    full_content = content
                                    last_chunk = content
                                else:
                                    # 正常的增量响应
                                    full_content += content
                                    last_chunk = content
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
        messages = [
            {"role": "system", "content": "你是专业情感分析专家，分析文本情感倾向，返回JSON格式。"},
            {"role": "user", "content": f"分析情感：{text}"}
        ]
        
        try:
            responses = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=True,
                result_format='message',
                temperature=0.1,
                top_p=0.8
            )
            
            # 智能处理流式响应
            full_content = ""
            last_chunk = ""
            
            for response in responses:
                if response.status_code == HTTPStatus.OK:
                    if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                        if hasattr(response.output.choices[0].message, 'content'):
                            content = response.output.choices[0].message.content
                            if content:
                                # 检查是否为累积响应
                                if last_chunk and last_chunk in content:
                                    # 这是累积响应，提取新增部分
                                    new_part = content[len(last_chunk):]
                                    full_content += new_part
                                    last_chunk = content
                                elif full_content and full_content in content:
                                    # 整个响应包含了之前的所有内容，直接使用
                                    full_content = content
                                    last_chunk = content
                                else:
                                    # 正常的增量响应
                                    full_content += content
                                    last_chunk = content
                else:
                    return json.dumps({
                        "error": True,
                        "message": f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
                    }, ensure_ascii=False)
            
            # 尝试解析JSON
            try:
                # 首先尝试直接解析
                result = json.loads(full_content)
            except:
                # 如果解析失败，尝试提取JSON部分
                import re
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                json_match = re.search(json_pattern, full_content)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except:
                        # 如果还是失败，构造一个默认格式
                        result = {"sentiment_analysis": full_content}
                else:
                    # 构造默认格式
                    result = {"sentiment_analysis": full_content}
            
            result["model"] = model_name
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

# ... 其他函数采用相同的智能流式处理方式 ...