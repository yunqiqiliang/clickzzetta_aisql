"""
最小化测试函数 - 基于成功的bailian_llm.py模式
完全自包含，不依赖任何外部库
"""

import os
import json
import sys

# 模拟 @annotate 装饰器 (如果不能导入cz.udf)
def annotate(signature):
    def decorator(cls):
        cls._signature = signature
        return cls
    return decorator

try:
    from cz.udf import annotate
except ImportError:
    # 使用模拟的装饰器
    pass

@annotate("*->string")
class ai_simple_echo(object):
    
    def evaluate(self, text, prefix="回显"):
        """
        最简单的回显函数，不依赖任何外部服务
        用于测试ZIP包和UDF服务器的基本加载功能
        """
        try:
            # 构造返回结果
            result = {
                "input_text": text,
                "output_text": f"{prefix}: {text}",
                "function_name": "ai_simple_echo",
                "timestamp": "2025-06-14T12:00:00Z",
                "success": True
            }
            
            # 返回 JSON 字符串
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            # 返回错误信息
            error_msg = {
                "error": True,
                "message": str(e),
                "function_name": "ai_simple_echo"
            }
            return json.dumps(error_msg, ensure_ascii=False)


if __name__ == '__main__':
    # 本地测试代码
    if len(sys.argv) < 2:
        print("Usage: python minimal_test.py <text> [prefix]")
        print("Example: python minimal_test.py '测试文本' '前缀'")
        sys.exit(1)
    
    # 获取参数
    text = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else "回显"
    
    # 创建实例并调用
    echo_func = ai_simple_echo()
    result = echo_func.evaluate(text, prefix)
    
    # 输出结果
    print(result)