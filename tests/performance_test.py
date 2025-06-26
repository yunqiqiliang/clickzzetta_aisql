#!/usr/bin/env python3
"""
性能测试脚本
测试AI函数的并发性能和批量处理能力
"""

import json
import sys
import time
import asyncio
import concurrent.futures
from datetime import datetime

sys.path.insert(0, '/Users/liangmo/Documents/GitHub/clickzetta_aisql')

def test_batch_processing(func_name, test_data, api_key):
    """测试批量处理性能"""
    from ai_functions_complete import ai_text_sentiment_analyze
    
    start_time = time.time()
    results = []
    
    # 创建函数实例
    func = ai_text_sentiment_analyze()
    
    # 批量处理
    for text in test_data:
        result = func.evaluate(text=text, api_key=api_key)
        results.append(result)
    
    end_time = time.time()
    
    return {
        "total_time": end_time - start_time,
        "avg_time": (end_time - start_time) / len(test_data),
        "count": len(test_data),
        "results": results
    }


def test_concurrent_requests(func_name, test_data, api_key, max_workers=5):
    """测试并发请求性能"""
    from ai_functions_complete import ai_text_sentiment_analyze
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 创建函数实例
        func = ai_text_sentiment_analyze()
        
        # 提交并发任务
        futures = []
        for text in test_data:
            future = executor.submit(func.evaluate, text=text, api_key=api_key)
            futures.append(future)
        
        # 等待所有任务完成
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    end_time = time.time()
    
    return {
        "total_time": end_time - start_time,
        "avg_time": (end_time - start_time) / len(test_data),
        "count": len(test_data),
        "max_workers": max_workers
    }


def main():
    if len(sys.argv) < 2:
        print("使用方法: python performance_test.py YOUR_API_KEY")
        return
    
    api_key = sys.argv[1]
    
    # 加载测试数据
    with open('data/batch_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    reviews = test_data['batch_sentiment']['reviews']
    
    print("🚀 开始性能测试")
    print("=" * 50)
    
    # 1. 顺序处理测试
    print("\n1️⃣ 顺序处理测试")
    seq_result = test_batch_processing('ai_text_sentiment_analyze', reviews, api_key)
    print(f"  总耗时: {seq_result['total_time']:.2f}秒")
    print(f"  平均耗时: {seq_result['avg_time']:.2f}秒/请求")
    
    # 2. 并发处理测试
    print("\n2️⃣ 并发处理测试")
    for workers in [2, 5, 10]:
        conc_result = test_concurrent_requests(
            'ai_text_sentiment_analyze', reviews, api_key, max_workers=workers
        )
        print(f"  {workers}并发: 总耗时{conc_result['total_time']:.2f}秒, "
              f"平均{conc_result['avg_time']:.2f}秒/请求")
    
    print("\n✅ 性能测试完成!")


if __name__ == '__main__':
    main()
