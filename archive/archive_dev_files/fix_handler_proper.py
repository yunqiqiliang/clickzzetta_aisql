#!/usr/bin/env python
"""
正确修复clickzetta_aisql包中的handler问题
确保handler = evaluate在正确的位置
"""

import os
import re

def fix_handler_properly():
    """修复handler属性的位置问题"""
    print("=== 正确修复handler位置问题 ===\n")
    
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
        
        # 移除所有错误位置的handler = evaluate
        content = re.sub(r'\n\s*handler = evaluate\s*#.*?\n', '\n', content)
        
        # 查找所有用@annotate装饰的类
        pattern = r'(@annotate\(["\'][^"\']+["\']\)\s*\nclass\s+(\w+)\([^)]*\):)'
        
        modified = False
        offset = 0
        
        for match in re.finditer(pattern, content):
            class_name = match.group(2)
            class_start = match.end() + offset
            
            # 查找文档字符串的结束位置
            doc_pattern = r'^\s*"""[\s\S]*?"""\s*$'
            remaining_content = content[class_start:]
            doc_match = re.search(doc_pattern, remaining_content, re.MULTILINE)
            
            if doc_match:
                # 在文档字符串后插入
                insert_pos = class_start + doc_match.end()
                # 获取正确的缩进
                indent_line = remaining_content[doc_match.end():].split('\n')[1] if len(remaining_content[doc_match.end():].split('\n')) > 1 else ""
                indent_match = re.match(r'^(\s*)', indent_line)
                indent = indent_match.group(1) if indent_match else '    '
            else:
                # 如果没有文档字符串，在类定义后插入
                insert_pos = class_start
                indent = '    '
            
            # 检查是否已经有handler属性
            # 查找到下一个类定义或文件结尾
            next_class_match = re.search(r'\n@annotate|\nif __name__', content[insert_pos:])
            if next_class_match:
                class_end = insert_pos + next_class_match.start()
            else:
                class_end = len(content)
            
            class_body = content[insert_pos:class_end]
            
            # 检查是否已有正确的handler定义
            if not re.search(r'^\s*handler\s*=\s*evaluate', class_body, re.MULTILINE):
                print(f"  添加handler到类: {class_name}")
                
                # 插入handler属性
                handler_line = f"\n{indent}handler = evaluate  # ClickZetta需要这个属性\n"
                
                content = content[:insert_pos] + handler_line + content[insert_pos:]
                offset += len(handler_line)
                modified = True
        
        if modified:
            # 保存修改后的文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ 文件已修复")
        else:
            print(f"  - 无需修改")
    
    print("\n=== 验证修复结果 ===")
    
    # 简单验证
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计handler = evaluate的数量
            handler_count = len(re.findall(r'handler\s*=\s*evaluate', content))
            class_count = len(re.findall(r'@annotate\(["\'][^"\']+["\']\)\s*\nclass', content))
            
            print(f"{file_path}: {handler_count} handlers, {class_count} classes")
            
            if handler_count != class_count:
                print(f"  ⚠️  数量不匹配！")

if __name__ == "__main__":
    fix_handler_properly()