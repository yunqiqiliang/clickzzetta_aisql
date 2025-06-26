#!/usr/bin/env python3
"""
快速测试AI函数优化效果
使用真实API密钥验证JIRA-001目标
"""

import json
import sys
import os
import time

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_functions_complete import ai_customer_segment

def quick_test(api_key):
    """快速测试ai_customer_segment函数"""
    print("🧪 快速测试ai_customer_segment函数")
    print("=" * 50)
    
    # 测试数据
    test_cases = [
        {"name": "高价值客户", "data": '{"recency": 15, "frequency": 8, "monetary": 2500}'},
        {"name": "中等价值客户", "data": '{"recency": 45, "frequency": 3, "monetary": 800}'},
        {"name": "低价值客户", "data": '{"recency": 180, "frequency": 1, "monetary": 100}'}
    ]
    
    func = ai_customer_segment()
    
    for i, test in enumerate(test_cases):
        print(f"\n测试 {i+1}: {test['name']}")
        print(f"输入: {test['data']}")
        
        # 调用函数
        start = time.time()
        result = func.evaluate(test['data'], api_key, 'RFM', 'qwen-plus')
        duration = time.time() - start
        
        # 分析结果
        result_size = len(result.encode('utf-8'))
        print(f"响应时间: {duration:.2f}秒")
        print(f"返回大小: {result_size} bytes")
        
        # 解析JSON
        try:
            data = json.loads(result)
            
            # 检查是否有segmentation_analysis字段（冗余文本）
            if 'segmentation_analysis' in data:
                analysis = data['segmentation_analysis']
                print(f"分析文本长度: {len(analysis)} 字符")
                
                # 检查是否包含冗余解释
                redundant_keywords = ["RFM模型", "三个维度", "评分规则", "以下是基于"]
                redundancy_found = [k for k in redundant_keywords if k in analysis]
                if redundancy_found:
                    print(f"⚠️  发现冗余文本: {redundancy_found}")
                    print(f"冗余度: 高（包含模型解释）")
                else:
                    print(f"✅ 未发现明显冗余文本")
            
            # 显示JSON结构
            print(f"JSON字段: {list(data.keys())}")
            
            # 计算压缩率（相对于1.2KB基准）
            compression = (1200 - result_size) / 1200 * 100
            print(f"压缩率: {compression:.1f}% (目标: 67%+)")
            
            if compression >= 67:
                print(f"✅ 达成压缩目标！")
            else:
                print(f"❌ 未达成压缩目标")
                
            # 显示部分返回内容
            print(f"\n返回内容预览:")
            print(json.dumps(data, ensure_ascii=False, indent=2)[:500] + "...")
            
        except Exception as e:
            print(f"❌ 解析错误: {e}")
        
        print("-" * 50)

def main():
    # 硬编码API密钥（请替换为您的实际密钥）
    # api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    # 或从命令行参数获取
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        print("使用方法: python quick_test_real_api.py YOUR_API_KEY")
        print("或直接修改代码中的api_key变量")
        return
    
    quick_test(api_key)
    
    print("\n💡 测试完成！")
    print("\n分析结论:")
    print("- 如果返回大小 > 400 bytes，说明包含冗余文本")
    print("- 如果发现'RFM模型'等解释性文字，说明优化未生效")
    print("- 如果压缩率 < 67%，需要应用新的优化提示词")
    
    print("\n下一步:")
    print("1. 如果测试显示冗余度高，运行: python optimize_ai_functions.py")
    print("2. 重新打包: python package_with_deps.py")
    print("3. 部署到ClickZetta测试")

if __name__ == '__main__':
    main()