"""
ClickZetta AI Functions Fixed Version
修复文本重复累积问题的版本
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

# ==================== 修复后的文本处理函数 ====================

@annotate("*->string")
class ai_text_summarize(object):
    def evaluate(self, text, api_key, model_name="qwen-plus", max_length=200):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        # 输入验证和保护
        if not text or not isinstance(text, str):
            return json.dumps({"error": True, "message": "Invalid input text"}, ensure_ascii=False)
        
        # 限制输入长度，防止过长输入
        if len(text) > 10000:
            text = text[:10000]
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"你是专业的文本摘要专家。请将文本总结为不超过{max_length}字的摘要。只返回摘要内容，不要重复原文。"},
            {"role": "user", "content": text}
        ]
        
        try:
            # 使用非流式调用，避免累积问题
            response = dashscope.Generation.call(
                model=model_name, 
                messages=messages, 
                result_format='message', 
                temperature=0.7,
                stream=False  # 关键修改：使用非流式调用
            )
            
            if response.status_code == HTTPStatus.OK:
                summary = response.output.choices[0].message.content
                
                # 输出保护：确保摘要不会超过原文长度
                if len(summary) > len(text):
                    # 如果摘要比原文还长，说明出现了问题，进行截断
                    summary = summary[:max_length]
                
                # 检测重复内容
                if self._detect_repetition(summary):
                    # 如果检测到重复，尝试提取第一个完整句子
                    summary = self._extract_first_sentences(summary, max_length)
                
                result = {
                    "summary": summary.strip(), 
                    "original_length": len(text), 
                    "summary_length": len(summary),
                    "model": model_name, 
                    "timestamp": datetime.now().isoformat()
                }
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
                
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)
    
    def _detect_repetition(self, text, threshold=0.5):
        """检测文本中是否有重复内容"""
        if len(text) < 50:
            return False
        
        # 简单的重复检测：检查前半部分是否在后半部分重复出现
        half_len = len(text) // 4
        prefix = text[:half_len]
        
        # 统计prefix在整个文本中出现的次数
        count = text.count(prefix)
        return count > 2  # 如果出现超过2次，认为有重复
    
    def _extract_first_sentences(self, text, max_length):
        """提取前几个完整的句子"""
        sentences = []
        current_length = 0
        
        # 按句号、问号、感叹号分割
        import re
        sentence_endings = re.split(r'[。！？.!?]', text)
        
        for sent in sentence_endings:
            if current_length + len(sent) <= max_length:
                sentences.append(sent)
                current_length += len(sent)
            else:
                break
        
        result = '。'.join(sentences)
        if result and not result.endswith('。'):
            result += '。'
        
        return result[:max_length]

@annotate("*->string")
class ai_text_sentiment_analyze(object):
    def evaluate(self, text, api_key, model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        # 输入验证
        if not text or not isinstance(text, str):
            return json.dumps({"error": True, "message": "Invalid input text"}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        
        # 更明确的prompt，避免重复
        prompt = f"""请分析以下文本的情感，返回严格的JSON格式，不要有任何额外内容：
{{
  "sentiment": "positive/negative/neutral",
  "confidence": 0.0-1.0,
  "emotions": {{
    "joy": 0.0-1.0,
    "anger": 0.0-1.0,
    "sadness": 0.0-1.0,
    "fear": 0.0-1.0
  }}
}}

文本：{text}"""
        
        messages = [
            {"role": "system", "content": "你是专业情感分析专家。只返回JSON格式结果，不要任何解释或额外内容。"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # 使用非流式调用
            response = dashscope.Generation.call(
                model=model_name, 
                messages=messages, 
                result_format='message', 
                temperature=0.1,
                stream=False,  # 使用非流式调用
                max_tokens=200  # 限制输出长度
            )
            
            if response.status_code == HTTPStatus.OK:
                content = response.output.choices[0].message.content
                
                # 清理可能的markdown代码块标记
                content = content.strip()
                if content.startswith('```'):
                    content = content.split('\n', 1)[1]
                if content.endswith('```'):
                    content = content.rsplit('\n', 1)[0]
                content = content.strip()
                
                try:
                    # 尝试解析JSON
                    result = json.loads(content)
                    
                    # 验证结果格式
                    if "sentiment" not in result:
                        # 如果格式不对，返回默认格式
                        result = {
                            "sentiment": "neutral",
                            "confidence": 0.5,
                            "raw_response": content[:200]  # 保存原始响应的前200字符
                        }
                except json.JSONDecodeError:
                    # JSON解析失败，返回默认格式
                    result = {
                        "sentiment": "neutral",
                        "confidence": 0.0,
                        "error": "Failed to parse response",
                        "raw_response": content[:200]
                    }
                
                result["model"] = model_name
                result["text_length"] = len(text)
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
                
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

# ==================== 测试函数 ====================

if __name__ == "__main__":
    # 本地测试
    test_text = "人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能才能完成的任务的系统。"
    
    # 模拟测试
    summarizer = ai_text_summarize()
    result = summarizer.evaluate(test_text, "test-key", "qwen-plus", 50)
    print("摘要测试:", result)
    
    analyzer = ai_text_sentiment_analyze()
    result = analyzer.evaluate("今天心情非常好！", "test-key")
    print("情感分析测试:", result)