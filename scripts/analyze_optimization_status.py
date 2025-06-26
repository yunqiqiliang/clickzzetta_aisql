#!/usr/bin/env python3
"""
分析AI函数优化状态
识别哪些函数已优化，哪些还需要优化
"""

import re

def analyze_optimization_status(file_path):
    """分析文件中的函数优化状态"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有AI函数
    function_pattern = r'class (ai_\w+)\(object\):'
    all_functions = re.findall(function_pattern, content)
    
    # 查找已优化的函数（包含"严格按照以下JSON格式返回"）
    optimized_functions = []
    
    # 分割成类定义块
    class_blocks = re.split(r'(?=class ai_\w+\(object\):)', content)
    
    for block in class_blocks:
        if 'class ai_' in block:
            # 提取类名
            match = re.search(r'class (ai_\w+)\(object\):', block)
            if match:
                class_name = match.group(1)
                # 检查是否包含优化标记
                if '严格按照以下JSON格式返回' in block:
                    optimized_functions.append(class_name)
    
    # 分类函数
    text_functions = []
    vector_functions = []
    multimodal_functions = []
    business_functions = []
    
    for func in all_functions:
        if func.startswith('ai_text_') or func == 'ai_auto_tag_generate':
            text_functions.append(func)
        elif func in ['ai_text_to_embedding', 'ai_semantic_similarity', 'ai_text_clustering_prepare', 
                      'ai_find_similar_text', 'ai_document_search']:
            vector_functions.append(func)
        elif func.startswith('ai_image_') or func.startswith('ai_video_') or func in ['ai_chart_analyze', 'ai_document_parse']:
            multimodal_functions.append(func)
        else:
            business_functions.append(func)
    
    # 输出分析结果
    print("🔍 AI函数优化状态分析")
    print("=" * 60)
    print(f"\n📊 总计: {len(all_functions)} 个函数")
    print(f"✅ 已优化: {len(optimized_functions)} 个")
    print(f"❌ 待优化: {len(all_functions) - len(optimized_functions)} 个")
    
    print("\n🏷️ 已优化的函数:")
    for func in sorted(optimized_functions):
        print(f"  ✅ {func}")
    
    print("\n📋 各类别优化状态:")
    
    # 文本处理函数
    print(f"\n1️⃣ 文本处理函数 ({len(text_functions)}个):")
    for func in text_functions:
        status = "✅" if func in optimized_functions else "❌"
        print(f"  {status} {func}")
    
    # 向量函数
    print(f"\n2️⃣ 向量函数 ({len(vector_functions)}个):")
    for func in vector_functions:
        status = "✅" if func in optimized_functions else "❌"
        print(f"  {status} {func}")
    
    # 多模态函数
    print(f"\n3️⃣ 多模态函数 ({len(multimodal_functions)}个):")
    for func in multimodal_functions:
        status = "✅" if func in optimized_functions else "❌"
        print(f"  {status} {func}")
    
    # 业务场景函数
    print(f"\n4️⃣ 业务场景函数 ({len(business_functions)}个):")
    for func in business_functions:
        status = "✅" if func in optimized_functions else "❌"
        print(f"  {status} {func}")
    
    # 推荐优化的函数
    unoptimized = [f for f in all_functions if f not in optimized_functions]
    
    if unoptimized:
        print("\n🎯 建议优化的函数（按优先级）:")
        
        # 优先级1：返回JSON格式的函数
        priority1 = []
        priority2 = []
        priority3 = []
        
        for func in unoptimized:
            if func in text_functions or func in business_functions:
                priority1.append(func)
            elif func in vector_functions:
                priority2.append(func)
            else:
                priority3.append(func)
        
        if priority1:
            print("\n  优先级1 - 文本/业务函数（最容易优化，收益最大）:")
            for func in priority1:
                print(f"    • {func}")
        
        if priority2:
            print("\n  优先级2 - 向量函数（返回嵌入向量，优化空间有限）:")
            for func in priority2:
                print(f"    • {func}")
        
        if priority3:
            print("\n  优先级3 - 多模态函数（处理图片/视频，优化复杂）:")
            for func in priority3:
                print(f"    • {func}")
    
    return optimized_functions, unoptimized

if __name__ == '__main__':
    file_path = '/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py'
    analyze_optimization_status(file_path)