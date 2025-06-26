#!/usr/bin/env python
"""
创建最终的clickzetta_aisql.zip包
包含所有修复后的文件和依赖
"""

import os
import shutil
import zipfile
import sys

def create_final_package():
    """创建最终的AI SQL函数包"""
    print("=== 创建最终的clickzetta_aisql.zip包 ===\n")
    
    # 定义输出路径
    output_path = "/Users/liangmo/Downloads/clickzetta_aisql.zip"
    
    # 创建临时目录
    temp_dir = "temp_clickzetta_aisql"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    print("1. 复制修复后的clickzetta_aisql目录...")
    # 复制clickzetta_aisql目录
    shutil.copytree("clickzetta_aisql", os.path.join(temp_dir, "clickzetta_aisql"))
    
    print("2. 复制所有依赖包...")
    # 依赖包列表（从requirements.txt）
    dependencies = [
        "dashscope",
        "requests", 
        "aiohttp",
        "aiohappyeyeballs",
        "aiosignal",
        "async_timeout",
        "attrs",
        "charset_normalizer",
        "idna",
        "multidict",
        "yarl",
        "certifi",
        "urllib3",
        "websocket",
        "websocket_client",
        "typing_extensions",
        "frozenlist",
        "propcache"
    ]
    
    # 查找并复制依赖包
    copied_deps = []
    for dep in dependencies:
        # 查找包目录
        if os.path.exists(dep):
            shutil.copytree(dep, os.path.join(temp_dir, dep))
            copied_deps.append(dep)
            print(f"   ✓ {dep}")
        
        # 查找dist-info目录
        for item in os.listdir("."):
            if item.startswith(f"{dep}-") and item.endswith(".dist-info"):
                shutil.copytree(item, os.path.join(temp_dir, item))
                print(f"   ✓ {item}")
                break
            elif item.replace("_", "-").startswith(f"{dep}-") and item.endswith(".dist-info"):
                shutil.copytree(item, os.path.join(temp_dir, item))
                print(f"   ✓ {item}")
                break
    
    # 特殊处理typing_extensions.py（单文件）
    if os.path.exists("typing_extensions.py"):
        shutil.copy2("typing_extensions.py", os.path.join(temp_dir, "typing_extensions.py"))
        print("   ✓ typing_extensions.py")
    
    print("\n3. 创建ZIP文件...")
    # 创建ZIP文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # 清理临时目录
    shutil.rmtree(temp_dir)
    
    # 获取文件大小
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    
    print(f"\n✅ 打包完成！")
    print(f"   文件路径: {output_path}")
    print(f"   文件大小: {file_size:.2f} MB")
    print(f"   包含依赖: {len(copied_deps)} 个包")
    
    # 验证ZIP内容
    print("\n4. 验证ZIP内容...")
    with zipfile.ZipFile(output_path, 'r') as zipf:
        file_list = zipf.namelist()
        
        # 统计各类文件
        py_files = [f for f in file_list if f.endswith('.py')]
        ai_functions = [f for f in py_files if f.startswith('clickzetta_aisql/') and 'functions.py' in f]
        
        print(f"   总文件数: {len(file_list)}")
        print(f"   Python文件: {len(py_files)}")
        print(f"   AI函数模块: {len(ai_functions)}")
        
        # 检查关键文件
        key_files = [
            'clickzetta_aisql/__init__.py',
            'clickzetta_aisql/vector_functions.py',
            'clickzetta_aisql/text_functions.py',
            'clickzetta_aisql/multimodal_functions.py',
            'clickzetta_aisql/business_functions.py',
            'clickzetta_aisql/common/base_llm.py'
        ]
        
        print("\n   关键文件检查:")
        for key_file in key_files:
            if key_file in file_list:
                print(f"   ✓ {key_file}")
            else:
                print(f"   ✗ {key_file} (缺失)")
    
    print("\n🎉 clickzetta_aisql.zip 已准备就绪，可以上传到ClickZetta使用！")

if __name__ == "__main__":
    create_final_package()