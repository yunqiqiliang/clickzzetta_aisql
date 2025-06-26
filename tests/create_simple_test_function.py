#!/usr/bin/env python3
"""
创建简单的测试函数，基于成功的bailian_llm.py模式
"""

test_function_content = '''import os
from cz.udf import annotate
import dashscope
from http import HTTPStatus
import json
import sys

@annotate("*->string")
class ai_text_summarize(object):
    
    def evaluate(self, text, api_key, model_name="qwen-plus", max_length=200):
        
        # 设置 API 密钥
        dashscope.api_key = api_key
        
        # 构建消息
        messages = [
            {"role": "system", "content": f"你是一个专业的文本摘要专家。请将以下文本总结为不超过{max_length}字的摘要。"},
            {"role": "user", "content": text}
        ]
        
        try:
            # 调用模型
            responses = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                stream=True,
                result_format='message',
                temperature=0.7,
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
            
            # 构造返回结果
            result = {
                "summary": full_content,
                "original_length": len(text),
                "summary_length": len(full_content),
                "model": model_name
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
    if len(sys.argv) < 4:
        print("Usage: python simple_text_function.py <text> <api_key> <model_name> [max_length]")
        print("Example: python simple_text_function.py \\"需要摘要的文本\\" \\"api-key\\" \\"qwen-plus\\" 200")
        sys.exit(1)
    
    # 获取必需参数
    text = sys.argv[1]
    api_key = sys.argv[2]
    model_name = sys.argv[3]
    
    # 获取可选参数
    max_length = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    
    # 创建实例并调用
    summarizer = ai_text_summarize()
    result = summarizer.evaluate(text, api_key, model_name, max_length)
    
    # 输出结果
    print(result)
'''

# 写入文件
with open('/Users/liangmo/Documents/GitHub/mcp-clickzetta-server/clickzetta_aisql/simple_text_function.py', 'w', encoding='utf-8') as f:
    f.write(test_function_content)

print("✅ 创建了简单的测试函数：simple_text_function.py")
print("🎯 这个函数完全基于成功的模式")
print("📝 可以用这个测试是否能被UDF服务器找到")