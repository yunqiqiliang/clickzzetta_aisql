"""
诊断工具：分析DashScope流式响应的行为
"""

import json

# 模拟可能的流式响应模式

def simulate_incremental_response():
    """模拟增量响应（正常情况）"""
    chunks = [
        "人工智能",
        "是计算机科学",
        "的一个分支。"
    ]
    return chunks

def simulate_cumulative_response():
    """模拟累积响应（问题情况）"""
    chunks = [
        "人工智能",
        "人工智能是计算机科学",
        "人工智能是计算机科学的一个分支。"
    ]
    return chunks

def simulate_mixed_response():
    """模拟混合响应（部分累积）"""
    chunks = [
        "人工智能",
        "是计算机科学",
        "人工智能是计算机科学的一个分支。"  # 第三个chunk包含了完整内容
    ]
    return chunks

def process_stream_simple(chunks):
    """简单的流式处理（原始方式）"""
    full_content = ""
    for chunk in chunks:
        if chunk:
            full_content += chunk
    return full_content

def process_stream_smart(chunks):
    """智能的流式处理（检测累积）"""
    full_content = ""
    previous_content = ""
    
    for i, chunk in enumerate(chunks):
        if chunk:
            # 检查是否为累积响应
            if previous_content and previous_content in chunk:
                # 这是累积响应，直接使用当前chunk
                full_content = chunk
                print(f"  检测到累积响应在chunk {i+1}")
            else:
                # 这是增量响应，累加
                full_content += chunk
            
            previous_content = full_content
    
    return full_content

def process_stream_detect_only(chunks):
    """只检测不修正的处理方式"""
    full_content = ""
    issues = []
    
    for i, chunk in enumerate(chunks):
        if chunk:
            # 检查chunk是否包含之前的full_content
            if full_content and full_content in chunk:
                issues.append(f"Chunk {i+1} 包含了之前的所有内容")
            
            # 检查chunk是否包含重复内容
            if i > 0 and chunks[0] in chunk:
                issues.append(f"Chunk {i+1} 包含了第一个chunk的内容")
            
            full_content += chunk
    
    return full_content, issues

# 测试各种情况
print("=== 流式响应诊断 ===\n")

# 测试1：增量响应
print("1. 增量响应（正常）:")
chunks = simulate_incremental_response()
print(f"   Chunks: {chunks}")
result = process_stream_simple(chunks)
print(f"   简单处理结果: '{result}'")
result_smart = process_stream_smart(chunks)
print(f"   智能处理结果: '{result_smart}'")
print()

# 测试2：累积响应
print("2. 累积响应（问题）:")
chunks = simulate_cumulative_response()
print(f"   Chunks: {chunks}")
result = process_stream_simple(chunks)
print(f"   简单处理结果: '{result}' (长度: {len(result)})")
result_smart = process_stream_smart(chunks.copy())
print(f"   智能处理结果: '{result_smart}' (长度: {len(result_smart)})")
result_detect, issues = process_stream_detect_only(chunks)
print(f"   检测到的问题: {issues}")
print()

# 测试3：混合响应
print("3. 混合响应:")
chunks = simulate_mixed_response()
print(f"   Chunks: {chunks}")
result = process_stream_simple(chunks)
print(f"   简单处理结果: '{result}' (长度: {len(result)})")
result_smart = process_stream_smart(chunks.copy())
print(f"   智能处理结果: '{result_smart}' (长度: {len(result_smart)})")
print()

# 真实场景模拟
print("4. 真实场景模拟（根据bug报告）:")
original_text = "人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能才能完成的任务的系统。"
print(f"   原文: '{original_text}' (长度: {len(original_text)})")

# 模拟可能的累积响应
simulated_chunks = [
    "人工智能",
    "人工智能（人工智能（AI",
    "人工智能（人工智能（AI）是计算机科学人工智能（AI）是计算机科学的分支，致力于",
    # ... 继续累积
]

# 展示如何产生1849字符的输出
def simulate_extreme_cumulative():
    """模拟极端累积情况"""
    text = "人工智能"
    chunks = [text]
    
    # 每次都包含之前的内容并添加新内容
    for i in range(5):
        text = text + f"（{text}）是计算机科学"
        chunks.append(text)
    
    return chunks

print("\n5. 极端累积模拟:")
extreme_chunks = simulate_extreme_cumulative()
for i, chunk in enumerate(extreme_chunks[:3]):  # 只显示前3个
    print(f"   Chunk {i+1} (长度 {len(chunk)}): {chunk[:50]}...")

result = process_stream_simple(extreme_chunks)
print(f"   简单处理最终长度: {len(result)}")
result_smart = process_stream_smart(extreme_chunks)
print(f"   智能处理最终长度: {len(result_smart)}")

# 提供修复建议
print("\n=== 修复建议 ===")
print("1. 使用智能流式处理，检测累积响应")
print("2. 或者直接使用非流式调用（stream=False）")
print("3. 添加输出长度保护机制")
print("4. 实现响应内容去重逻辑")