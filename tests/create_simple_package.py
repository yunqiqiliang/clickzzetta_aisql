#!/usr/bin/env python3
"""
创建一个简化版本的包，直接使用原始bailian_llm的结构
"""

import os
import shutil
import zipfile

def create_simple_package():
    """创建简化的包"""
    
    # 1. 创建临时目录
    temp_dir = "clickzetta_aisql_simple"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 2. 复制原始的 bailian_llm.py（已知可工作）
    shutil.copy2("bailian_llm.py", os.path.join(temp_dir, "bailian_llm.py"))
    print("✅ 复制 bailian_llm.py")
    
    # 3. 创建一个简化的 text_to_embedding 函数（不依赖BaseLLMFunction）
    simple_vector_functions = '''import os
from cz.udf import annotate
import dashscope
from http import HTTPStatus
import json
import sys

@annotate("*->string")
class text_to_embedding(object):
    def evaluate(self, text, api_key, model_name="text-embedding-v4", dimension="auto"):
        try:
            # 设置 API 密钥
            dashscope.api_key = api_key
            
            params = {
                "model": model_name,
                "input": text
            }
            
            # text-embedding-v4支持动态维度
            if model_name == "text-embedding-v4" and dimension != "auto":
                params["parameters"] = {"dimension": int(dimension)}
            
            response = dashscope.TextEmbedding.call(**params)
            
            if response.status_code == HTTPStatus.OK:
                embedding = response.output['embeddings'][0]['embedding']
                result = {
                    "embedding": embedding,
                    "dimension": len(embedding),
                    "model": model_name,
                    "text_tokens": response.usage.total_tokens if hasattr(response, 'usage') else None,
                    "input_text_length": len(text)
                }
                return json.dumps(result, ensure_ascii=False)
            else:
                error_msg = {
                    "error": True,
                    "message": f"嵌入API调用失败: {response.message}"
                }
                return json.dumps(error_msg, ensure_ascii=False)
                
        except Exception as e:
            error_msg = {
                "error": True,
                "message": str(e)
            }
            return json.dumps(error_msg, ensure_ascii=False)
'''
    
    with open(os.path.join(temp_dir, "vector_functions.py"), "w", encoding="utf-8") as f:
        f.write(simple_vector_functions)
    print("✅ 创建简化的 vector_functions.py")
    
    # 4. 复制必要的依赖
    dependencies_to_copy = [
        ("dashscope", "dashscope"),
        ("typing_extensions.py", "typing_extensions.py")
    ]
    
    # 从 clickzetta_aisql 目录复制依赖
    source_dir = "clickzetta_aisql"
    for src, dst in dependencies_to_copy:
        src_path = os.path.join(source_dir, src)
        dst_path = os.path.join(temp_dir, dst)
        
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
            print(f"✅ 复制依赖 {src}")
    
    # 5. 复制所有 dist-info 目录（最小化）
    essential_dist_info = [
        "dashscope-1.23.4.dist-info",
        "typing_extensions-4.14.0.dist-info"
    ]
    
    for dist_info in essential_dist_info:
        src = os.path.join(source_dir, dist_info)
        dst = os.path.join(temp_dir, dist_info)
        if os.path.exists(src):
            shutil.copytree(src, dst)
            print(f"✅ 复制 {dist_info}")
    
    # 6. 创建 zip 包
    zip_filename = "clickzetta_aisql_simple.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # 7. 清理临时目录
    shutil.rmtree(temp_dir)
    
    print(f"\n✅ 创建完成！新包已保存为: {zip_filename}")
    print("\n📝 包含的函数：")
    print("1. bailian_llm.get_industry_classification - 行业分类（原始可工作版本）")
    print("2. vector_functions.text_to_embedding - 文本向量化（简化版本）")
    
    print("\n🚀 使用方法：")
    print("1. 上传包：PUT file:///path/to/clickzetta_aisql_simple.zip @user_files/")
    print("2. 创建函数：")
    print("   HANDLER = 'bailian_llm.get_industry_classification'")
    print("   HANDLER = 'vector_functions.text_to_embedding'")

if __name__ == "__main__":
    create_simple_package()