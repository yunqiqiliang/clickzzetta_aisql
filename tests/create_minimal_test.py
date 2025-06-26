#!/usr/bin/env python3
"""
创建一个最小的测试包，只包含bailian_llm.py
用于验证原始可工作版本
"""

import os
import shutil
import zipfile

def create_minimal_test():
    """创建最小测试包"""
    
    # 1. 创建临时目录
    temp_dir = "minimal_test"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 2. 只复制 bailian_llm.py（已知可工作）
    if os.path.exists("bailian_llm.py"):
        shutil.copy2("bailian_llm.py", os.path.join(temp_dir, "bailian_llm.py"))
        print("✅ 复制 bailian_llm.py")
    else:
        # 从根目录复制
        shutil.copy2("/Users/liangmo/Documents/GitHub/mcp-clickzetta-server/bailian_llm.py", 
                     os.path.join(temp_dir, "bailian_llm.py"))
        print("✅ 复制 bailian_llm.py（从根目录）")
    
    # 3. 创建一个极简的text_to_embedding（完全独立，不依赖任何导入）
    minimal_text_embedding = '''import json

class text_to_embedding(object):
    def evaluate(self, text, api_key, model_name="test", dimension="auto"):
        # 极简实现，只返回测试数据
        result = {
            "embedding": [0.1, 0.2, 0.3],
            "dimension": 3,
            "model": model_name,
            "input_text": text
        }
        return json.dumps(result, ensure_ascii=False)
'''
    
    with open(os.path.join(temp_dir, "test_functions.py"), "w", encoding="utf-8") as f:
        f.write(minimal_text_embedding)
    print("✅ 创建极简的 test_functions.py")
    
    # 4. 从原始包复制必要的依赖（只复制dashscope相关）
    source_bailian = "/Users/liangmo/Downloads/bailian_llm"
    if os.path.exists(source_bailian):
        # 复制dashscope
        for item in ["dashscope", "dashscope-1.23.4.dist-info"]:
            src = os.path.join(source_bailian, item)
            dst = os.path.join(temp_dir, item)
            if os.path.exists(src):
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                print(f"✅ 复制 {item}")
        
        # 复制typing_extensions.py
        src_typing = os.path.join(source_bailian, "typing_extensions.py")
        if os.path.exists(src_typing):
            shutil.copy2(src_typing, os.path.join(temp_dir, "typing_extensions.py"))
            print("✅ 复制 typing_extensions.py")
    
    # 5. 创建 zip 包
    zip_filename = "minimal_test.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # 6. 清理临时目录
    shutil.rmtree(temp_dir)
    
    print(f"\n✅ 创建完成！新包已保存为: {zip_filename}")
    print("\n📝 测试步骤：")
    print("1. 上传包：PUT file:///path/to/minimal_test.zip @user_files/")
    print("\n2. 先测试原始函数（应该成功）：")
    print("   CREATE EXTERNAL FUNCTION get_industry_classification")
    print("   AS 'bailian_llm.get_industry_classification'")
    print("   USING ARCHIVE 'volume://user_files/minimal_test.zip'")
    print("   CONNECTION your_connection")
    print("   WITH PROPERTIES ('remote.udf.api' = 'python3.mc.v0')")
    print("\n3. 再测试新函数：")
    print("   CREATE EXTERNAL FUNCTION test_embedding")
    print("   AS 'test_functions.text_to_embedding'")
    print("   USING ARCHIVE 'volume://user_files/minimal_test.zip'")
    print("   CONNECTION your_connection")
    print("   WITH PROPERTIES ('remote.udf.api' = 'python3.mc.v0')")

if __name__ == "__main__":
    create_minimal_test()