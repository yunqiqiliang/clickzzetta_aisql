#!/usr/bin/env python3
"""
创建与原始可工作版本结构一致的包
"""

import os
import shutil
import zipfile

def create_working_package():
    """创建可工作的包"""
    
    # 1. 创建临时目录
    temp_dir = "clickzetta_aisql_working"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 2. 复制所有 Python 文件到根目录（不要子目录）
    source_dir = "clickzetta_aisql"
    
    # 复制主要的 Python 文件
    files_to_copy = [
        "bailian_llm.py",
        "text_functions.py", 
        "vector_functions.py",
        "multimodal_functions.py",
        "business_functions.py"
    ]
    
    for file in files_to_copy:
        src = os.path.join(source_dir, file)
        dst = os.path.join(temp_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ 复制 {file}")
    
    # 3. 复制 common 目录（保持原有结构）
    src_common = os.path.join(source_dir, "common")
    dst_common = os.path.join(temp_dir, "common")
    if os.path.exists(src_common):
        shutil.copytree(src_common, dst_common)
        print("✅ 复制 common 目录")
    
    # 4. 复制所有依赖（从原始包）
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
            print(f"✅ 复制 {item}")
    
    # 6. 确保 bailian_llm.py 没有 handler 属性（与原始版本一致）
    bailian_path = os.path.join(temp_dir, "bailian_llm.py")
    if os.path.exists(bailian_path):
        with open(bailian_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 移除 handler 属性行
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if 'handler = "evaluate"' not in line:
                new_lines.append(line)
            else:
                print("⚠️ 移除了 handler 属性（与原始版本保持一致）")
        
        content = '\n'.join(new_lines)
        
        # 清理多余的空行
        content = content.replace('\n\n\n', '\n\n')
        
        with open(bailian_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # 7. 创建 zip 包
    zip_filename = "clickzetta_aisql_working.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # 8. 清理临时目录
    shutil.rmtree(temp_dir)
    
    print(f"\n✅ 创建完成！新包已保存为: {zip_filename}")
    print("\n📝 关键改动：")
    print("1. ✅ 所有 Python 文件都在根目录（不在 clickzetta_aisql 子目录）")
    print("2. ✅ 保持了原始版本的扁平结构")
    print("3. ✅ 包含所有必要的依赖")
    print("4. ✅ 移除了 handler 属性（与原始可工作版本一致）")
    
    print("\n🚀 使用方法：")
    print("1. 上传包：PUT file:///path/to/clickzetta_aisql_working.zip @user_files/")
    print("2. 创建函数时使用正确的 Handler 格式：")
    print("   HANDLER = 'bailian_llm.get_industry_classification'")
    print("   HANDLER = 'vector_functions.text_to_embedding'")
    print("   （注意：不需要 clickzetta_aisql 前缀）")

if __name__ == "__main__":
    create_working_package()