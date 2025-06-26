#!/usr/bin/env python3
"""验证clickzetta_aisql包结构"""

import zipfile
import os

def verify_package(zip_path):
    """验证包结构"""
    print(f"验证包: {zip_path}")
    print("=" * 60)
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # 列出所有文件
        files = zf.namelist()
        
        # 统计文件类型
        py_files = [f for f in files if f.endswith('.py')]
        ai_function_files = [f for f in py_files if any(x in f for x in ['vector', 'text', 'multimodal', 'business', 'bailian'])]
        
        print(f"总文件数: {len(files)}")
        print(f"Python文件数: {len(py_files)}")
        print(f"AI函数文件: {len(ai_function_files)}")
        
        print("\n📁 AI函数文件结构:")
        for f in sorted(ai_function_files):
            print(f"  - {f}")
        
        # 检查handler路径
        print("\n🔍 建议的handler路径格式:")
        
        # 检查text_to_embedding
        if any('vector_functions.py' in f for f in files):
            print("\n对于text_to_embedding函数:")
            print("  方式1: clickzetta_aisql.vector_functions.text_to_embedding")
            print("  方式2: vector_functions.text_to_embedding")
            
        # 读取vector_functions.py内容
        try:
            with zf.open('clickzetta_aisql/vector_functions.py') as f:
                content = f.read().decode('utf-8')
                if 'class text_to_embedding' in content and 'handler = "evaluate"' in content:
                    print("  ✅ 确认: text_to_embedding类有handler属性")
        except:
            try:
                with zf.open('vector_functions.py') as f:
                    content = f.read().decode('utf-8')
                    if 'class text_to_embedding' in content and 'handler = "evaluate"' in content:
                        print("  ✅ 确认: text_to_embedding类有handler属性")
            except:
                print("  ⚠️ 警告: 无法验证handler属性")

if __name__ == "__main__":
    # 验证原包
    if os.path.exists('clickzetta_aisql.zip'):
        verify_package('clickzetta_aisql.zip')
        print("\n" + "=" * 60 + "\n")
    
    # 验证修复后的包
    if os.path.exists('clickzetta_aisql_fixed.zip'):
        verify_package('clickzetta_aisql_fixed.zip')