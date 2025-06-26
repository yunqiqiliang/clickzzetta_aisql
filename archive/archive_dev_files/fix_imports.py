#!/usr/bin/env python3
"""
修复导入问题 - 将相对导入改为绝对导入
"""

import os
import shutil
import zipfile
import re

def fix_imports_in_file(file_path):
    """修复单个文件中的导入"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复相对导入
    # from .common.xxx import yyy -> from common.xxx import yyy
    content = re.sub(r'from \.common\.', 'from common.', content)
    content = re.sub(r'from \.', 'from ', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_fixed_package():
    """创建修复导入问题的包"""
    
    # 1. 创建临时目录
    temp_dir = "clickzetta_aisql_fixed"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 2. 复制文件并修复导入
    source_dir = "clickzetta_aisql"
    
    # 复制主要的 Python 文件
    files_to_fix = [
        "bailian_llm.py",
        "text_functions.py", 
        "vector_functions.py",
        "multimodal_functions.py",
        "business_functions.py"
    ]
    
    for file in files_to_fix:
        src = os.path.join(source_dir, file)
        dst = os.path.join(temp_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            fix_imports_in_file(dst)
            print(f"✅ 复制并修复 {file}")
    
    # 3. 复制 common 目录
    src_common = os.path.join(source_dir, "common")
    dst_common = os.path.join(temp_dir, "common")
    if os.path.exists(src_common):
        shutil.copytree(src_common, dst_common)
        # 修复common目录中的文件
        for root, dirs, files in os.walk(dst_common):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    fix_imports_in_file(file_path)
        print("✅ 复制并修复 common 目录")
    
    # 4. 复制所有依赖
    dependencies = [
        "dashscope", "aiohttp", "yarl", "multidict", "frozenlist",
        "aiosignal", "aiohappyeyeballs", "async_timeout", "attrs",
        "propcache", "typing_extensions.py", "certifi", "charset_normalizer",
        "idna", "requests", "urllib3", "websocket", "attr"
    ]
    
    for dep in dependencies:
        src_path = os.path.join(source_dir, dep)
        dst_path = os.path.join(temp_dir, dep)
        
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
            print(f"✅ 复制依赖 {dep}")
    
    # 5. 复制所有 .dist-info 目录
    for item in os.listdir(source_dir):
        if item.endswith('.dist-info'):
            src = os.path.join(source_dir, item)
            dst = os.path.join(temp_dir, item)
            shutil.copytree(src, dst)
    
    # 6. 创建 zip 包
    zip_filename = "clickzetta_aisql_fixed_imports.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # 7. 清理临时目录
    shutil.rmtree(temp_dir)
    
    print(f"\n✅ 创建完成！新包已保存为: {zip_filename}")
    print("\n📝 关键修复：")
    print("1. ✅ 将所有相对导入改为绝对导入")
    print("2. ✅ from .common.xxx -> from common.xxx")
    print("3. ✅ 保持了完整的依赖结构")
    
    print("\n🚀 测试方法：")
    print("1. 上传包：PUT file:///path/to/clickzetta_aisql_fixed_imports.zip @user_files/")
    print("2. 创建函数：")
    print("   AS 'vector_functions.text_to_embedding'")
    print("   USING ARCHIVE 'volume://user_files/clickzetta_aisql_fixed_imports.zip'")

if __name__ == "__main__":
    create_fixed_package()