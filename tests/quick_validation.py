#!/usr/bin/env python3
"""
快速验证脚本
用于快速验证关键函数的优化效果
"""

import json
import sys
import time
from datetime import datetime

sys.path.insert(0, '/Users/liangmo/Documents/GitHub/clickzetta_aisql')

# 关键函数列表（JIRA-001重点优化目标）
KEY_FUNCTIONS = [
    # 已优化的函数
    "ai_customer_segment",
    "ai_text_sentiment_analyze", 
    "ai_text_extract_keywords",
    "ai_customer_intent_analyze",
    "ai_sales_lead_score",
    
    # 需要验证的其他函数
    "ai_text_summarize",
    "ai_text_translate",
    "ai_review_analyze",
    "ai_product_description_generate"
]


def validate_function(func_name: str, test_params: dict, api_key: str) -> dict:
    """验证单个函数"""
    try:
        # 动态导入
        module = __import__('ai_functions_complete')
        func_class = getattr(module, func_name, None)
        
        if not func_class:
            return {"status": "NOT_FOUND", "error": f"函数{func_name}未找到"}
        
        # 创建实例并调用
        func = func_class()
        params = test_params.copy()
        params["api_key"] = api_key
        
        start_time = time.time()
        result = func.evaluate(**params)
        execution_time = time.time() - start_time
        
        # 分析结果
        result_size = len(result.encode('utf-8'))
        compression_rate = (1200 - result_size) / 1200 * 100
        
        # 尝试解析JSON
        try:
            result_data = json.loads(result)
            json_valid = True
            
            # 检查是否有冗余内容
            has_redundancy = False
            if isinstance(result_data, dict):
                # 检查常见的冗余字段
                redundant_fields = ['model', 'timestamp', 'api_key', 'model_name']
                for field in redundant_fields:
                    if field in result_data:
                        has_redundancy = True
                        break
                
                # 检查是否有长解释文本
                for key, value in result_data.items():
                    if isinstance(value, str) and len(value) > 500:
                        has_redundancy = True
                        break
        except:
            json_valid = False
            has_redundancy = True
            result_data = None
        
        return {
            "status": "SUCCESS",
            "execution_time": execution_time,
            "result_size": result_size,
            "compression_rate": compression_rate,
            "json_valid": json_valid,
            "has_redundancy": has_redundancy,
            "meets_jira_001": compression_rate >= 67 and result_size <= 400,
            "sample": result[:200] + "..." if len(result) > 200 else result
        }
        
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python quick_validation.py YOUR_API_KEY")
        return
    
    api_key = sys.argv[1]
    
    print("🚀 JIRA-001 快速验证")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"目标: 压缩率≥67%, 返回大小≤400字节")
    print("=" * 60)
    
    # 定义测试参数
    test_configs = {
        "ai_customer_segment": {
            "customer_data": '{"recency": 30, "frequency": 5, "monetary": 1500}',
            "segmentation_model": "RFM"
        },
        "ai_text_sentiment_analyze": {
            "text": "产品质量很好，非常满意！"
        },
        "ai_text_extract_keywords": {
            "text": "人工智能和机器学习是未来技术发展的重要方向",
            "max_keywords": 3
        },
        "ai_customer_intent_analyze": {
            "customer_text": "我想了解你们的产品价格",
            "business_context": "general"
        },
        "ai_sales_lead_score": {
            "lead_info": '{"budget": 50000, "timeline": "1 month", "authority": "decision maker"}',
            "scoring_criteria": "BANT"
        },
        "ai_text_summarize": {
            "text": "人工智能技术正在快速发展，深度学习、自然语言处理等领域取得重大突破。",
            "max_length": 50
        },
        "ai_text_translate": {
            "text": "Hello world",
            "target_language": "中文"
        },
        "ai_review_analyze": {
            "review_text": "产品不错，但价格偏高",
            "product_type": "general"
        },
        "ai_product_description_generate": {
            "product_info": '{"name": "智能手表", "features": ["心率监测", "GPS"]}',
            "style": "professional"
        }
    }
    
    # 执行验证
    results = []
    passed_count = 0
    
    for func_name in KEY_FUNCTIONS:
        if func_name not in test_configs:
            print(f"\n⚠️  {func_name}: 缺少测试配置")
            continue
        
        print(f"\n🔍 验证: {func_name}")
        result = validate_function(func_name, test_configs[func_name], api_key)
        results.append({"function": func_name, **result})
        
        if result["status"] == "SUCCESS":
            status_icon = "✅" if result["meets_jira_001"] else "❌"
            print(f"  {status_icon} 状态: 成功")
            print(f"  • 执行时间: {result['execution_time']:.2f}秒")
            print(f"  • 返回大小: {result['result_size']}字节")
            print(f"  • 压缩率: {result['compression_rate']:.1f}%")
            print(f"  • JSON有效: {'是' if result['json_valid'] else '否'}")
            print(f"  • 有冗余: {'是' if result['has_redundancy'] else '否'}")
            
            if result["meets_jira_001"]:
                passed_count += 1
        else:
            print(f"  ❌ 状态: 失败 - {result.get('error', 'Unknown')}")
    
    # 生成总结
    print("\n" + "=" * 60)
    print("📊 验证总结")
    print("=" * 60)
    
    success_results = [r for r in results if r["status"] == "SUCCESS"]
    if success_results:
        avg_compression = sum(r["compression_rate"] for r in success_results) / len(success_results)
        avg_size = sum(r["result_size"] for r in success_results) / len(success_results)
        
        print(f"✅ 成功验证: {len(success_results)}/{len(KEY_FUNCTIONS)}")
        print(f"🎯 JIRA-001达标: {passed_count}/{len(success_results)} ({passed_count/len(success_results)*100:.1f}%)")
        print(f"📊 平均压缩率: {avg_compression:.1f}%")
        print(f"📏 平均返回大小: {avg_size:.0f}字节")
    
    # 需要优化的函数
    need_optimization = [r for r in results if r["status"] == "SUCCESS" and not r["meets_jira_001"]]
    if need_optimization:
        print(f"\n⚠️  需要进一步优化的函数:")
        for r in need_optimization:
            print(f"  • {r['function']}: 压缩率{r['compression_rate']:.1f}%, 大小{r['result_size']}字节")
    
    # 保存验证结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_file = f"data/validation_result_{timestamp}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "validation_time": datetime.now().isoformat(),
            "key_functions": KEY_FUNCTIONS,
            "results": results,
            "summary": {
                "total": len(KEY_FUNCTIONS),
                "success": len(success_results),
                "jira_001_passed": passed_count,
                "avg_compression": avg_compression if success_results else 0,
                "avg_size": avg_size if success_results else 0
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结果已保存: {result_file}")


if __name__ == '__main__':
    main()