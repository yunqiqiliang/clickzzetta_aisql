#!/usr/bin/env python3
"""
快速修复AI函数文本重复问题的脚本
可以直接替换现有的ai_functions_complete.py
"""

import shutil
import os
import re
from datetime import datetime

def fix_stream_calls(content):
    """修复流式调用问题"""
    # 1. 将stream=True改为stream=False
    content = re.sub(
        r'stream\s*=\s*True',
        'stream=False',
        content
    )
    
    # 2. 修改流式响应处理为单次响应
    # 原模式：for response in responses:
    # 新模式：response = responses (单次调用)
    
    # 查找并替换流式处理代码块
    pattern = r'''responses = dashscope\.Generation\.call\((.*?)\)
(\s+)full_content = ""
(\s+)for response in responses:
(\s+)if response\.status_code == HTTPStatus\.OK:
(\s+)if hasattr\(response\.output, 'choices'\) and len\(response\.output\.choices\) > 0:
(\s+)content = response\.output\.choices\[0\]\.message\.content
(\s+)if content: full_content \+= content'''
    
    replacement = r'''response = dashscope.Generation.call(\1)
\2if response.status_code == HTTPStatus.OK:
\3    if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
\4        full_content = response.output.choices[0].message.content or ""
\5        # 添加输出长度保护
\6        if len(full_content) > len(text) * 2:
\7            full_content = full_content[:len(text)]'''
    
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    
    return content

def add_max_tokens_limit(content):
    """为所有API调用添加max_tokens限制"""
    # 在Generation.call中添加max_tokens参数
    pattern = r'(dashscope\.Generation\.call\([^)]+)'
    
    def add_max_tokens(match):
        call_str = match.group(1)
        if 'max_tokens' not in call_str:
            # 根据不同函数设置不同的限制
            if 'summarize' in call_str:
                return call_str + ', max_tokens=500'
            elif 'sentiment' in call_str:
                return call_str + ', max_tokens=200'
            else:
                return call_str + ', max_tokens=1000'
        return call_str
    
    content = re.sub(pattern, add_max_tokens, content)
    return content

def add_output_validation(content):
    """添加输出验证函数"""
    validation_code = '''
    def _validate_output(self, output, input_text, max_ratio=2.0):
        """验证输出是否合理"""
        if not output:
            return output
        
        # 检查长度
        if len(output) > len(input_text) * max_ratio:
            # 智能截断
            return self._smart_truncate(output, int(len(input_text) * max_ratio))
        
        # 检查重复
        if self._has_repetition(output):
            # 提取第一部分
            parts = output.split(output[:50])
            if len(parts) > 2:
                return parts[0] + output[:50]
        
        return output
    
    def _has_repetition(self, text):
        """简单的重复检测"""
        if len(text) < 100:
            return False
        
        # 检查前1/4是否重复出现
        quarter = len(text) // 4
        prefix = text[:quarter]
        return text.count(prefix) > 2
    
    def _smart_truncate(self, text, max_length):
        """智能截断文本"""
        if len(text) <= max_length:
            return text
        
        # 在句子边界截断
        for sep in ['。', '！', '？', '.', '!', '?', '\n']:
            pos = text[:max_length].rfind(sep)
            if pos > max_length // 2:
                return text[:pos + 1]
        
        return text[:max_length]
'''
    
    # 在每个类定义后添加验证方法
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # 在类定义后添加验证方法
        if line.strip().startswith('class ai_') and line.strip().endswith('(object):'):
            # 找到下一个def evaluate
            for j in range(i+1, min(i+10, len(lines))):
                if lines[j].strip().startswith('def evaluate'):
                    # 在evaluate方法后插入验证方法
                    indent = '    '  # 类方法的缩进
                    validation_lines = validation_code.strip().split('\n')
                    
                    # 找到evaluate方法的结束位置
                    k = j + 1
                    while k < len(lines) and (lines[k].startswith('        ') or lines[k].strip() == ''):
                        k += 1
                    
                    # 在合适的位置插入
                    insert_pos = len(new_lines) + (k - i - 1)
                    for val_line in validation_lines:
                        if val_line:
                            new_lines.insert(insert_pos, indent + val_line)
                            insert_pos += 1
                    break
    
    return '\n'.join(new_lines)

def optimize_prompts(content):
    """优化提示词，明确要求不重复"""
    replacements = [
        # 摘要提示词优化
        (
            r'"你是专业的文本摘要专家。请将文本总结为不超过\{max_length\}字的摘要。"',
            '"你是专业的文本摘要专家。请将文本总结为不超过{max_length}字的摘要。要求：1)不要重复原文 2)使用简洁语言 3)只输出摘要内容"'
        ),
        # 情感分析提示词优化
        (
            r'"你是专业情感分析专家，分析文本情感倾向，返回JSON格式。"',
            '"你是专业情感分析专家。请分析文本情感，只返回JSON格式结果，不要任何解释。格式：{sentiment, confidence, emotions}"'
        ),
        # 实体提取提示词优化
        (
            r'"你是专业信息提取专家，从文本中提取实体信息，返回JSON格式。"',
            '"你是专业信息提取专家。提取实体并返回JSON格式，不要重复原文，只列出实体。"'
        )
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    return content

def main():
    """主函数：应用所有修复"""
    print("开始修复AI函数文本重复问题...")
    
    # 1. 备份原文件
    source_file = "ai_functions_complete.py"
    backup_file = f"ai_functions_complete.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if os.path.exists(source_file):
        shutil.copy2(source_file, backup_file)
        print(f"已备份原文件到: {backup_file}")
    
    # 2. 读取原文件内容
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 3. 应用修复
    print("应用修复...")
    
    # 修复流式调用
    content = fix_stream_calls(content)
    print("  ✓ 已修复流式调用问题")
    
    # 添加max_tokens限制
    content = add_max_tokens_limit(content)
    print("  ✓ 已添加输出长度限制")
    
    # 优化提示词
    content = optimize_prompts(content)
    print("  ✓ 已优化提示词")
    
    # 添加输出验证
    # content = add_output_validation(content)
    # print("  ✓ 已添加输出验证")
    
    # 4. 保存修复后的文件
    output_file = "ai_functions_complete_fixed.py"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n修复完成！修复后的文件: {output_file}")
    print("\n后续步骤:")
    print("1. 测试修复后的函数")
    print("2. 如果测试通过，替换原文件:")
    print(f"   cp {output_file} {source_file}")
    print("3. 重新打包并部署:")
    print("   python package_with_deps.py")
    print("   # 上传新的ZIP包到ClickZetta")
    
    # 5. 生成测试脚本
    test_script = '''#!/usr/bin/env python3
"""测试修复后的AI函数"""

import json
from ai_functions_complete_fixed import ai_text_summarize, ai_text_sentiment_analyze

def test_summarize():
    """测试摘要功能"""
    print("测试文本摘要...")
    
    test_cases = [
        "人工智能（AI）是计算机科学的一个分支。",
        "这是一段较长的测试文本，包含多个句子。用于验证摘要功能是否正常工作。确保没有重复内容。",
        "今天天气很好。" * 10  # 重复内容测试
    ]
    
    summarizer = ai_text_summarize()
    
    for i, text in enumerate(test_cases):
        result = summarizer.evaluate(text, "test-api-key", "qwen-plus", 50)
        data = json.loads(result)
        
        print(f"\\n测试用例 {i+1}:")
        print(f"输入长度: {len(text)}")
        print(f"输出: {data}")
        
        if "summary" in data:
            ratio = len(data["summary"]) / len(text)
            print(f"长度比率: {ratio:.2f}")
            
            # 检查是否有重复
            if text[:20] in data["summary"]:
                print("⚠️  警告：可能包含原文重复")
            else:
                print("✓ 无明显重复")

def test_sentiment():
    """测试情感分析"""
    print("\\n测试情感分析...")
    
    test_cases = [
        "今天心情非常好！",
        "这个产品质量太差了。",
        "一般般吧。"
    ]
    
    analyzer = ai_text_sentiment_analyze()
    
    for i, text in enumerate(test_cases):
        result = analyzer.evaluate(text, "test-api-key", "qwen-plus")
        
        print(f"\\n测试用例 {i+1}: {text}")
        print(f"结果: {result}")

if __name__ == "__main__":
    print("开始测试修复后的AI函数...\\n")
    test_summarize()
    test_sentiment()
    print("\\n测试完成！")
'''
    
    with open("test_fixed_functions.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print(f"\n已生成测试脚本: test_fixed_functions.py")
    print("运行测试: python test_fixed_functions.py")

if __name__ == "__main__":
    main()