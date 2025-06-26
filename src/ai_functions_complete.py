"""
ClickZetta AI Functions Complete Package
完整的AI函数包 - 30个生产就绪的AI函数
基于成功的bailian_llm.py模式构建
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
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.7)
            
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
                else:
                    full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            result = {"summary": full_content, "original_length": len(text), "model": model_name, "timestamp": datetime.now().isoformat()}
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
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.3)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            result = {"translated_text": full_content, "original_text": text, "target_language": target_language, "model": model_name}
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
            {"role": "system", "content": """你是专业情感分析专家。分析文本情感倾向。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"sentiment": "positive|negative|neutral", "confidence": 0.95, "emotions": ["joy", "anger"], "keywords": ["关键词1"]}"""},
            {"role": "user", "content": f"分析情感：{text}"}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.1)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
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
            {"role": "system", "content": """你是专业信息提取专家。从文本中提取实体信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"entities": [{"text": "实体名", "type": "PERSON|ORG|LOC|MISC", "confidence": 0.95}]}"""},
            {"role": "user", "content": f"提取实体（类型：{entity_types}）：{text}"}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.2)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"entities": full_content}
            result["entity_types"] = entity_types
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_text_extract_keywords(object):
    def evaluate(self, text, api_key, max_keywords=10, model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是关键词提取专家。提取文本的核心关键词。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"keywords": [{{"word": "关键词", "weight": 0.95, "category": "核心概念"}}]}}（最多提取{max_keywords}个关键词）"""},
            {"role": "user", "content": text}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.3)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"keywords": full_content.split("、") if "、" in full_content else [full_content]}
            result["max_keywords"] = max_keywords
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_text_classify(object):
    def evaluate(self, text, api_key, categories="auto", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是文本分类专家。将文本分类到合适类别。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"category": "分类名称", "confidence": 0.95, "subcategory": "子分类", "categories_considered": ["类别1", "类别2"]}}（候选类别：{categories}）"""},
            {"role": "user", "content": text}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.2)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"classification": full_content}
            result["categories"] = categories
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_text_clean_normalize(object):
    def evaluate(self, text, api_key, operations="all", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是文本清洗专家。执行文本清洗和标准化操作。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"cleaned_text": "清洗后文本", "operations_applied": ["去重", "标准化"], "changes_count": 5}}（执行操作：{operations}）"""},
            {"role": "user", "content": text}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.1)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"cleaned_text": full_content}
            result["operations"] = operations
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_auto_tag_generate(object):
    def evaluate(self, text, api_key, max_tags=10, model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是智能标签生成专家。为文本生成相关标签。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"tags": [{{"tag": "标签名", "relevance": 0.95, "category": "主题"}}]}}（生成{max_tags}个标签）"""},
            {"role": "user", "content": text}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.5)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"tags": full_content.split("、") if "、" in full_content else [full_content]}
            result["max_tags"] = max_tags
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

# ==================== 向量函数 (5个) ====================

@annotate("*->string")
class ai_text_to_embedding(object):
    def evaluate(self, text, api_key, model_name="text-embedding-v4"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            dashscope.api_key = api_key
            response = dashscope.TextEmbedding.call(model=model_name, input=text)
            if response.status_code == HTTPStatus.OK:
                embedding = response.output['embeddings'][0]['embedding']
                result = {"embedding": embedding, "dimension": len(embedding), "model": model_name, "text_length": len(text)}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"嵌入生成失败: {response.message}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_semantic_similarity(object):
    def evaluate(self, text1, text2, api_key, model_name="text-embedding-v4"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            dashscope.api_key = api_key
            
            # 获取两个文本的嵌入
            response1 = dashscope.TextEmbedding.call(model=model_name, input=text1)
            response2 = dashscope.TextEmbedding.call(model=model_name, input=text2)
            
            if response1.status_code == HTTPStatus.OK and response2.status_code == HTTPStatus.OK:
                emb1 = response1.output['embeddings'][0]['embedding']
                emb2 = response2.output['embeddings'][0]['embedding']
                
                # 计算余弦相似度
                import math
                dot_product = sum(a * b for a, b in zip(emb1, emb2))
                magnitude1 = math.sqrt(sum(a * a for a in emb1))
                magnitude2 = math.sqrt(sum(a * a for a in emb2))
                similarity = dot_product / (magnitude1 * magnitude2)
                
                result = {"similarity": similarity, "text1_length": len(text1), "text2_length": len(text2), "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": "嵌入生成失败"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_text_clustering_prepare(object):
    def evaluate(self, texts_json, api_key, model_name="text-embedding-v4"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            texts = json.loads(texts_json)
            dashscope.api_key = api_key
            
            embeddings = []
            for text in texts:
                response = dashscope.TextEmbedding.call(model=model_name, input=text)
                if response.status_code == HTTPStatus.OK:
                    embeddings.append(response.output['embeddings'][0]['embedding'])
                else:
                    return json.dumps({"error": True, "message": f"嵌入生成失败: {response.message}"}, ensure_ascii=False)
            
            result = {"embeddings": embeddings, "count": len(embeddings), "dimension": len(embeddings[0]) if embeddings else 0}
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_find_similar_text(object):
    def evaluate(self, query_text, candidate_texts_json, api_key, top_k=5, model_name="text-embedding-v4"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            candidate_texts = json.loads(candidate_texts_json)
            dashscope.api_key = api_key
            
            # 获取查询文本嵌入
            query_response = dashscope.TextEmbedding.call(model=model_name, input=query_text)
            if query_response.status_code != HTTPStatus.OK:
                return json.dumps({"error": True, "message": "查询文本嵌入失败"}, ensure_ascii=False)
            
            query_emb = query_response.output['embeddings'][0]['embedding']
            similarities = []
            
            for text in candidate_texts:
                response = dashscope.TextEmbedding.call(model=model_name, input=text)
                if response.status_code == HTTPStatus.OK:
                    emb = response.output['embeddings'][0]['embedding']
                    
                    # 计算余弦相似度
                    import math
                    dot_product = sum(a * b for a, b in zip(query_emb, emb))
                    magnitude1 = math.sqrt(sum(a * a for a in query_emb))
                    magnitude2 = math.sqrt(sum(a * a for a in emb))
                    similarity = dot_product / (magnitude1 * magnitude2)
                    
                    similarities.append({"text": text, "similarity": similarity})
            
            # 排序并返回top_k
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            result = {"similar_texts": similarities[:top_k], "total_candidates": len(candidate_texts)}
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_document_search(object):
    def evaluate(self, query, documents_json, api_key, top_k=3, model_name="text-embedding-v4"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            documents = json.loads(documents_json)  # [{"id": "1", "text": "content"}, ...]
            dashscope.api_key = api_key
            
            # 获取查询嵌入
            query_response = dashscope.TextEmbedding.call(model=model_name, input=query)
            if query_response.status_code != HTTPStatus.OK:
                return json.dumps({"error": True, "message": "查询嵌入失败"}, ensure_ascii=False)
            
            query_emb = query_response.output['embeddings'][0]['embedding']
            results = []
            
            for doc in documents:
                response = dashscope.TextEmbedding.call(model=model_name, input=doc["text"])
                if response.status_code == HTTPStatus.OK:
                    emb = response.output['embeddings'][0]['embedding']
                    
                    # 计算相似度
                    import math
                    dot_product = sum(a * b for a, b in zip(query_emb, emb))
                    magnitude1 = math.sqrt(sum(a * a for a in query_emb))
                    magnitude2 = math.sqrt(sum(a * a for a in emb))
                    similarity = dot_product / (magnitude1 * magnitude2)
                    
                    results.append({
                        "doc_id": doc["id"], 
                        "score": similarity, 
                        "snippet": doc["text"][:200] + "..." if len(doc["text"]) > 200 else doc["text"]
                    })
            
            results.sort(key=lambda x: x["score"], reverse=True)
            result = {"results": results[:top_k], "query": query, "total_docs": len(documents)}
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

# ==================== 多模态函数 (8个) ====================

@annotate("*->string")
class ai_image_describe(object):
    def evaluate(self, image_url, api_key, prompt="描述这张图片", model_name="qwen-vl-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            dashscope.api_key = api_key
            messages = [
                {"role": "user", "content": [
                    {"image": image_url},
                    {"text": prompt}
                ]}
            ]
            
            response = dashscope.MultiModalConversation.call(model=model_name, messages=messages)
            if response.status_code == HTTPStatus.OK:
                description = response.output.choices[0].message.content
                result = {"description": description, "image_url": image_url, "prompt": prompt, "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"图片描述失败: {response.message}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_image_ocr(object):
    def evaluate(self, image_url, api_key, language="auto", model_name="qwen-vl-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            dashscope.api_key = api_key
            messages = [
                {"role": "user", "content": [
                    {"image": image_url},
                    {"text": f"请识别图片中的文字内容（语言：{language}）"}
                ]}
            ]
            
            response = dashscope.MultiModalConversation.call(model=model_name, messages=messages)
            if response.status_code == HTTPStatus.OK:
                text = response.output.choices[0].message.content
                result = {"text": text, "image_url": image_url, "language": language, "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"OCR识别失败: {response.message}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_image_analyze(object):
    def evaluate(self, image_url, api_key, analysis_type="general", model_name="qwen-vl-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            dashscope.api_key = api_key
            prompts = {
                "general": "请全面分析这张图片，包括内容、场景、对象等",
                "objects": "请识别图片中的所有对象和物品",
                "scene": "请描述图片的场景和环境",
                "people": "请分析图片中的人物信息",
                "text": "请提取图片中的所有文字信息"
            }
            
            prompt = prompts.get(analysis_type, prompts["general"])
            messages = [
                {"role": "user", "content": [
                    {"image": image_url},
                    {"text": prompt}
                ]}
            ]
            
            response = dashscope.MultiModalConversation.call(model=model_name, messages=messages)
            if response.status_code == HTTPStatus.OK:
                analysis = response.output.choices[0].message.content
                result = {"analysis": analysis, "analysis_type": analysis_type, "image_url": image_url, "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"图片分析失败: {response.message}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_image_to_embedding(object):
    def evaluate(self, image_url, api_key, model_name="multimodal-embedding-one-peace-v1"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            dashscope.api_key = api_key
            response = dashscope.MultiModalEmbedding.call(
                model=model_name,
                input={"image": image_url}
            )
            
            if response.status_code == HTTPStatus.OK:
                embedding = response.output['embeddings'][0]['embedding']
                result = {"embedding": embedding, "dimension": len(embedding), "image_url": image_url, "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"图片嵌入生成失败: {response.message}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_image_similarity(object):
    def evaluate(self, image_url1, image_url2, api_key, model_name="multimodal-embedding-one-peace-v1"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            dashscope.api_key = api_key
            
            # 获取两张图片的嵌入
            response1 = dashscope.MultiModalEmbedding.call(model=model_name, input={"image": image_url1})
            response2 = dashscope.MultiModalEmbedding.call(model=model_name, input={"image": image_url2})
            
            if response1.status_code == HTTPStatus.OK and response2.status_code == HTTPStatus.OK:
                emb1 = response1.output['embeddings'][0]['embedding']
                emb2 = response2.output['embeddings'][0]['embedding']
                
                # 计算余弦相似度
                import math
                dot_product = sum(a * b for a, b in zip(emb1, emb2))
                magnitude1 = math.sqrt(sum(a * a for a in emb1))
                magnitude2 = math.sqrt(sum(a * a for a in emb2))
                similarity = dot_product / (magnitude1 * magnitude2)
                
                result = {"similarity": similarity, "image1": image_url1, "image2": image_url2, "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": "图片嵌入生成失败"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_video_summarize(object):
    def evaluate(self, video_frames_json, api_key, model_name="qwen-vl-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            frame_urls = json.loads(video_frames_json)
            dashscope.api_key = api_key
            
            # 构建消息，包含多个视频帧
            content = []
            for url in frame_urls:
                content.append({"image": url})
            content.append({"text": "请基于这些视频帧生成视频内容摘要"})
            
            messages = [{"role": "user", "content": content}]
            
            response = dashscope.MultiModalConversation.call(model=model_name, messages=messages)
            if response.status_code == HTTPStatus.OK:
                summary = response.output.choices[0].message.content
                result = {"summary": summary, "frame_count": len(frame_urls), "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"视频摘要失败: {response.message}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_chart_analyze(object):
    def evaluate(self, chart_image_url, api_key, analysis_focus="data", model_name="qwen-vl-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            dashscope.api_key = api_key
            focus_prompts = {
                "data": "请分析图表中的数据趋势和关键数值",
                "trend": "请分析图表显示的趋势变化",
                "comparison": "请比较图表中不同数据系列的差异",
                "insight": "请从图表中提取商业洞察和结论"
            }
            
            prompt = focus_prompts.get(analysis_focus, focus_prompts["data"])
            messages = [
                {"role": "user", "content": [
                    {"image": chart_image_url},
                    {"text": prompt}
                ]}
            ]
            
            response = dashscope.MultiModalConversation.call(model=model_name, messages=messages)
            if response.status_code == HTTPStatus.OK:
                analysis = response.output.choices[0].message.content
                result = {"analysis": analysis, "focus": analysis_focus, "chart_url": chart_image_url, "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"图表分析失败: {response.message}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_document_parse(object):
    def evaluate(self, doc_images_json, api_key, parse_type="structure", model_name="qwen-vl-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        try:
            image_urls = json.loads(doc_images_json)
            dashscope.api_key = api_key
            
            parse_prompts = {
                "structure": "请解析文档结构，包括标题、段落、表格等",
                "content": "请提取文档中的所有文字内容",
                "table": "请提取文档中的表格数据",
                "form": "请识别并提取表单字段和内容"
            }
            
            prompt = parse_prompts.get(parse_type, parse_prompts["structure"])
            
            # 构建消息，包含所有文档页面
            content = []
            for url in image_urls:
                content.append({"image": url})
            content.append({"text": prompt})
            
            messages = [{"role": "user", "content": content}]
            
            response = dashscope.MultiModalConversation.call(model=model_name, messages=messages)
            if response.status_code == HTTPStatus.OK:
                parsed_content = response.output.choices[0].message.content
                result = {"parsed_content": parsed_content, "parse_type": parse_type, "page_count": len(image_urls), "model": model_name}
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({"error": True, "message": f"文档解析失败: {response.message}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

# ==================== 业务场景函数 (9个) ====================

@annotate("*->string")
class ai_customer_intent_analyze(object):
    def evaluate(self, customer_text, api_key, business_context="general", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是客户意图分析专家。分析客户文本的真实意图。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"intent": "购买意向|咨询|投诉|建议", "confidence": 0.95, "urgency": "high|medium|low", "emotions": ["satisfied"], "action_required": "立即处理"}}（业务背景：{business_context}）"""},
            {"role": "user", "content": customer_text}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.2)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"intent_analysis": full_content}
            
            result.update({"customer_text": customer_text, "business_context": business_context, "model": model_name})
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_sales_lead_score(object):
    def evaluate(self, lead_info, api_key, scoring_criteria="RFM", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是销售线索评分专家。根据标准评估线索价值。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"score": 85, "grade": "A|B|C|D", "probability": 0.85, "factors": [{{"factor": "预算充足", "impact": "positive", "weight": 0.3}}], "next_action": "立即跟进"}}（评分标准：{scoring_criteria}）"""},
            {"role": "user", "content": f"线索信息：{lead_info}"}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.1)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"lead_score": full_content}
            
            result.update({"lead_info": lead_info, "scoring_criteria": scoring_criteria, "model": model_name})
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_review_analyze(object):
    def evaluate(self, review_text, api_key, product_type="general", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是评论分析专家。分析用户评论的多维度信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"sentiment": "positive|negative|neutral", "rating_predicted": 4.5, "aspects": [{{"aspect": "服务", "sentiment": "positive", "score": 4.2}}], "key_issues": ["待改进点"]}}（产品类型：{product_type}）"""},
            {"role": "user", "content": f"评论内容：{review_text}"}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.2)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"review_analysis": full_content}
            
            result.update({"review_text": review_text, "product_type": product_type, "model": model_name})
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_risk_text_detect(object):
    def evaluate(self, text, api_key, risk_types="all", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是风险检测专家。检测文本中的各类风险内容。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"risk_level": "high|medium|low|none", "risk_types": ["欺诈", "违规"], "confidence": 0.95, "flagged_content": ["具体风险文本"], "action_required": true}}（风险类型：{risk_types}）"""},
            {"role": "user", "content": text}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.1)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"risk_assessment": full_content}
            
            result.update({"original_text": text, "risk_types": risk_types, "model": model_name})
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_contract_extract(object):
    def evaluate(self, contract_text, api_key, extract_fields="all", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是合同信息提取专家。提取合同的关键信息字段。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"parties": ["甲方", "乙方"], "amount": "1000000", "start_date": "2024-01-01", "end_date": "2024-12-31", "key_terms": ["重要条款"], "risk_points": ["风险点"]}}（提取字段：{extract_fields}）"""},
            {"role": "user", "content": f"合同内容：{contract_text}"}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.1)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"contract_info": full_content}
            
            result.update({"extract_fields": extract_fields, "contract_length": len(contract_text), "model": model_name})
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_resume_parse(object):
    def evaluate(self, resume_text, api_key, parse_depth="standard", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是简历解析专家。解析简历的结构化信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"name": "姓名", "education": [{{"degree": "本科", "school": "大学", "major": "专业"}}], "experience": [{{"title": "职位", "company": "公司", "duration": "2年"}}], "skills": ["技能1"]}}（解析深度：{parse_depth}）"""},
            {"role": "user", "content": f"简历内容：{resume_text}"}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.1)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"resume_info": full_content}
            
            result.update({"parse_depth": parse_depth, "resume_length": len(resume_text), "model": model_name})
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_customer_segment(object):
    def evaluate(self, customer_data, api_key, segmentation_model="RFM", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是客户细分专家。根据模型进行客户细分分析。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"segment": "高价值客户", "scores": {{"R": 5, "F": 4, "M": 5}}, "total_score": 85, "characteristics": ["购买频繁"], "recommendations": ["VIP服务"], "retention_probability": 0.92}}（使用模型：{segmentation_model}）"""},
            {"role": "user", "content": f"客户数据：{customer_data}"}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.2)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"segment": "未知", "scores": {}, "analysis": full_content}
            
            result.update({"segmentation_model": segmentation_model, "customer_data": customer_data, "model": model_name})
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_product_description_generate(object):
    def evaluate(self, product_info, api_key, style="professional", model_name="qwen-plus"):
        if not HAS_DASHSCOPE:
            return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)
        
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": f"""你是产品文案专家。生成吸引人的产品描述。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"title": "产品标题", "description": "详细描述", "features": ["特色1", "特色2"], "benefits": ["优势1"], "target_audience": "目标用户", "selling_points": ["卖点1"]}}（文案风格：{style}）"""},
            {"role": "user", "content": f"产品信息：{product_info}"}
        ]
        
        try:
            response = dashscope.Generation.call(model=model_name, messages=messages, stream=False, result_format='message', temperature=0.6)
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        full_content = response.output.choices[0].message.content or ""
                    else:
                        full_content = ""
            else:
                return json.dumps({"error": True, "message": f"API调用失败: {response.message}"}, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                result = {"product_description": full_content}
            
            result.update({"style": style, "product_info": product_info, "model": model_name})
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": True, "message": str(e)}, ensure_ascii=False)

@annotate("*->string")
class ai_industry_classification(object):
    def evaluate(self, text, prompt, api_key, model_name, temperature=0.7, enable_search=False):
        dashscope.api_key = api_key
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
        
        try:
            response = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=False,
                result_format='message',
                temperature=temperature,
                enable_search=enable_search,
                top_p=0.8
            )
            
            full_content = ""
            if response.status_code == HTTPStatus.OK:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    if hasattr(response.output.choices[0].message, 'content'):
                        content = response.output.choices[0].message.content
                        if content:
                            full_content = content
            else:
                error_msg = {
                    "error": True,
                    "message": f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
                }
                return json.dumps(error_msg, ensure_ascii=False)
            
            try:
                result = json.loads(full_content)
            except:
                import re
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                json_match = re.search(json_pattern, full_content)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except:
                        result = {"一级行业": "未能解析", "二级行业": "未能解析", "原始内容": full_content}
                else:
                    result = {"一级行业": "未能解析", "二级行业": "未能解析", "原始内容": full_content}
            
            if "一级行业" not in result or "二级行业" not in result:
                result = {
                    "一级行业": result.get("一级行业", "未知"),
                    "二级行业": result.get("二级行业", "未知"),
                    "原始内容": full_content
                }
            
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            error_msg = {"error": True, "message": str(e)}
            return json.dumps(error_msg, ensure_ascii=False)


if __name__ == '__main__':
    print("ClickZetta AI Functions Complete Package - 30个生产就绪的AI函数")
    print("包含: 8个文本处理 + 5个向量处理 + 8个多模态 + 9个业务场景函数")
    
    # 快速测试
    test_summarize = ai_text_summarize()
    result = test_summarize.evaluate("这是一个测试文本", "test-key")
    print("测试结果:", result)