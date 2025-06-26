#!/usr/bin/env python
"""
仅检查核心AI函数文件的语法
"""

import os
import py_compile
import ast

def check_core_files():
    """检查核心AI函数文件"""
    print("=== 检查核心AI函数文件语法 ===\n")
    
    core_files = [
        'clickzetta_aisql/vector_functions.py',
        'clickzetta_aisql/text_functions.py', 
        'clickzetta_aisql/multimodal_functions.py',
        'clickzetta_aisql/business_functions.py',
        'clickzetta_aisql/__init__.py',
        'clickzetta_aisql/common/__init__.py',
        'clickzetta_aisql/common/base_llm.py',
        'clickzetta_aisql/common/prompt_templates.py',
        'clickzetta_aisql/common/response_parser.py',
        'bailian_llm.py'
    ]
    
    error_count = 0
    
    for file_path in core_files:
        if not os.path.exists(file_path):
            print(f"✗ 文件不存在: {file_path}")
            continue
            
        print(f"检查: {file_path}")
        try:
            # 编译检查
            py_compile.compile(file_path, doraise=True)
            
            # AST解析检查
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
            
            print(f"  ✓ 语法正确")
            
        except SyntaxError as e:
            error_count += 1
            print(f"  ❌ 语法错误: 第 {e.lineno} 行")
            print(f"     {e.msg}")
            if e.text:
                print(f"     {e.text.strip()}")
                print(f"     {' ' * (e.offset - 1)}^")
                
        except Exception as e:
            error_count += 1
            print(f"  ❌ 其他错误: {str(e)}")
    
    print(f"\n=== 检查完成 ===")
    print(f"总文件数: {len(core_files)}")
    print(f"语法错误: {error_count}")
    
    if error_count == 0:
        print("\n✅ 所有核心文件语法检查通过！")
        return True
    else:
        print(f"\n❌ 发现 {error_count} 个语法错误")
        return False

if __name__ == "__main__":
    check_core_files()