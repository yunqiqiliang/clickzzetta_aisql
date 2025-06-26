import os
from cz.udf import annotate
import dashscope
from http import HTTPStatus
import json
import sys

@annotate("*->string")
class get_industry_classification(object):
    
    handler = "evaluate"  # ClickZetta需要这个属性

    def evaluate(self, text, prompt, api_key, model_name, temperature=0.7, enable_search=False):
        
        # 设置 API 密钥
        dashscope.api_key = api_key
        
        # 构建消息
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
        
        try:
            # 调用模型
            responses = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=True,
                result_format='message',
                temperature=temperature,
                enable_search=enable_search,
                top_p=0.8
            )
            
            # 收集完整的响应内容
            full_content = ""
            for response in responses:
                if response.status_code == HTTPStatus.OK:
                    if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                        if hasattr(response.output.choices[0].message, 'content'):
                            content = response.output.choices[0].message.content
                            if content:
                                full_content += content
                else:
                    # 返回错误信息
                    error_msg = {
                        "error": True,
                        "message": f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
                    }
                    return json.dumps(error_msg, ensure_ascii=False)
            
            # 尝试解析 LLM 返回的内容为 JSON
            # 假设 LLM 返回的内容已经是 JSON 格式
            try:
                # 首先尝试直接解析
                result = json.loads(full_content)
            except:
                # 如果解析失败，尝试提取 JSON 部分
                import re
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                json_match = re.search(json_pattern, full_content)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except:
                        # 如果还是失败，构造一个默认格式
                        result = {
                            "一级行业": "未能解析",
                            "二级行业": "未能解析",
                            "原始内容": full_content
                        }
                else:
                    # 构造默认格式
                    result = {
                        "一级行业": "未能解析",
                        "二级行业": "未能解析",
                        "原始内容": full_content
                    }
            
            # 确保返回的 JSON 包含所需字段
            if "一级行业" not in result or "二级行业" not in result:
                # 如果缺少必要字段，尝试从原始内容中提取
                result = {
                    "一级行业": result.get("一级行业", "未知"),
                    "二级行业": result.get("二级行业", "未知"),
                    "原始内容": full_content
                }
            
            # 返回 JSON 字符串
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            # 返回错误信息
            error_msg = {
                "error": True,
                "message": str(e)
            }
            return json.dumps(error_msg, ensure_ascii=False)


if __name__ == '__main__':
    # 检查参数数量
    if len(sys.argv) < 5:
        print("Usage: python get_industry_classification.py <text> <prompt> <api_key> <model_name> [temperature] [enable_search]")
        print("Example: python get_industry_classification.py \"公司描述\" \"分类提示\" \"api-key\" \"qwen-plus\" 0.7 false")
        sys.exit(1)
    
    # 获取必需参数
    text = sys.argv[1]
    prompt = sys.argv[2]
    api_key = sys.argv[3]
    model_name = sys.argv[4]
    
    # 获取可选参数
    temperature = float(sys.argv[5]) if len(sys.argv) > 5 else 0.7
    enable_search = sys.argv[6].lower() == 'true' if len(sys.argv) > 6 else False
    
    # 创建实例并调用
    classifier = get_industry_classification()
    result = classifier.evaluate(text, prompt, api_key, model_name, temperature, enable_search)
    
    # 输出结果
    print(result)
