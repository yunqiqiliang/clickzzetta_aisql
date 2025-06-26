#!/usr/bin/env python
"""
最终修复：为所有函数添加handler = "evaluate"字符串属性
"""

import os
import re

def fix_handler_as_string():
    """修复handler属性为字符串格式"""
    print("=== 最终修复：handler = 'evaluate' ===\n")
    
    # 需要修复的文件列表
    files_to_fix = [
        'clickzetta_aisql/vector_functions.py',
        'clickzetta_aisql/text_functions.py',
        'clickzetta_aisql/multimodal_functions.py',
        'clickzetta_aisql/business_functions.py',
        'bailian_llm.py'
    ]
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            print(f"✗ 文件不存在: {file_path}")
            continue
            
        print(f"处理文件: {file_path}")
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 移除所有错误的handler定义
        content = re.sub(r'\n\s*handler = evaluate\s*#.*?\n', '\n', content)
        content = re.sub(r'\n\s*handler = "evaluate"\s*#.*?\n', '\n', content)
        content = re.sub(r"\n\s*handler = 'evaluate'\s*#.*?\n", '\n', content)
        
        # 2. 查找所有用@annotate装饰的类并添加正确的handler
        pattern = r'(@annotate\(["\'][^"\']+["\']\)\s*\nclass\s+(\w+)\([^)]*\):\s*\n)'
        
        def add_handler(match):
            class_def = match.group(1)
            class_name = match.group(2)
            
            # 查找文档字符串
            remaining = content[match.end():]
            doc_match = re.match(r'(\s*"""[\s\S]*?"""\s*\n)', remaining)
            
            if doc_match:
                # 在文档字符串后插入
                doc_string = doc_match.group(1)
                # 获取正确的缩进
                indent_match = re.search(r'\n(\s+)def ', remaining[doc_match.end():])
                if indent_match:
                    indent = indent_match.group(1)
                else:
                    indent = '    '
                return class_def + doc_string + f'{indent}handler = "evaluate"  # ClickZetta需要这个属性\n\n'
            else:
                # 没有文档字符串，直接在类定义后插入
                return class_def + '    handler = "evaluate"  # ClickZetta需要这个属性\n\n'
        
        # 替换所有匹配
        new_content = re.sub(pattern + r'(\s*"""[\s\S]*?"""\s*\n)?', add_handler, content)
        
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✓ 文件已修复")
    
    print("\n=== 验证修复结果 ===")
    
    # 验证
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计handler = "evaluate"的数量
            handler_count = len(re.findall(r'handler\s*=\s*["\']evaluate["\']', content))
            class_count = len(re.findall(r'@annotate\(["\'][^"\']+["\']\)\s*\nclass', content))
            
            print(f"{file_path}: {handler_count} handlers, {class_count} classes")
            
            if handler_count != class_count:
                print(f"  ⚠️  数量不匹配！需要手动检查")

if __name__ == "__main__":
    fix_handler_as_string()