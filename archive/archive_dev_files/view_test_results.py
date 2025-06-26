#!/usr/bin/env python3
"""
查看测试结果并生成验收报告
"""

import json
import os
import glob
from datetime import datetime


def view_latest_test_results():
    """查看最新的测试结果"""
    
    # 尝试多个可能的数据目录
    possible_dirs = [
        "/Users/liangmo/Documents/GitHub/clickzetta_aisql/data",
        "../clickzetta_aisql/data",
        "../../clickzetta_aisql/data",
        "./data"
    ]
    
    data_dir = None
    for dir_path in possible_dirs:
        if os.path.exists(dir_path):
            data_dir = dir_path
            break
    
    if not data_dir:
        print("❌ 未找到数据目录")
        return
    
    # 查找最新的测试报告
    report_files = glob.glob(os.path.join(data_dir, "test_report_*.json"))
    if not report_files:
        print(f"❌ 在 {data_dir} 中未找到测试报告")
        return
    
    latest_report = max(report_files, key=os.path.getctime)
    print(f"📄 分析报告: {latest_report}")
    
    with open(latest_report, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # 生成验收报告
    generate_acceptance_report(report)


def generate_acceptance_report(report):
    """生成功能验收报告"""
    
    print("\n" + "="*80)
    print("🎯 AI函数功能验收报告")
    print("="*80)
    print(f"测试时间: {report.get('test_time', 'N/A')}")
    
    # 1. 总体统计
    summary = report.get('summary', {})
    total = summary.get('total', 0)
    success = summary.get('success', 0)
    failed = summary.get('failed', 0)
    success_rate = (success / total * 100) if total > 0 else 0
    
    print(f"\n📊 总体统计")
    print(f"• 测试函数总数: {total}")
    print(f"• 成功: {success} ({success_rate:.1f}%)")
    print(f"• 失败: {failed}")
    
    # 2. 按类别统计
    print(f"\n📂 分类统计")
    for category, stats in summary.get('by_category', {}).items():
        cat_total = stats['total']
        cat_success = stats['success']
        cat_rate = (cat_success / cat_total * 100) if cat_total > 0 else 0
        print(f"\n{category}:")
        print(f"  • 函数数: {cat_total}")
        print(f"  • 成功率: {cat_rate:.1f}%")
    
    # 3. 功能验收结果
    print(f"\n✅ 功能验收结果")
    
    # 定义验收标准
    acceptance_criteria = {
        "功能完整性": success_rate >= 70,
        "文本处理": check_category_rate(summary, "文本处理") >= 90,
        "业务场景": check_category_rate(summary, "业务场景") >= 80,
        "向量处理": check_category_rate(summary, "向量处理") >= 80,
        "多模态处理": check_category_rate(summary, "多模态处理") >= 50  # 放宽标准
    }
    
    all_passed = True
    for criterion, passed in acceptance_criteria.items():
        status = "✅ 通过" if passed else "❌ 未通过"
        print(f"• {criterion}: {status}")
        if not passed:
            all_passed = False
    
    # 4. 问题清单
    details = report.get('details', [])
    failed_functions = [d for d in details if d['status'] != 'SUCCESS']
    
    if failed_functions:
        print(f"\n❌ 失败函数清单 ({len(failed_functions)}个)")
        for func in failed_functions:
            print(f"• {func['function']}: {func['status']} - {func.get('error', 'Unknown error')[:50]}...")
    
    # 5. 性能指标
    success_details = [d for d in details if d['status'] == 'SUCCESS']
    if success_details:
        avg_time = sum(d['execution_time'] for d in success_details) / len(success_details)
        avg_size = sum(d['result_size'] for d in success_details) / len(success_details)
        
        print(f"\n⚡ 性能指标")
        print(f"• 平均响应时间: {avg_time:.2f}秒")
        print(f"• 平均返回大小: {avg_size:.0f}字节")
        
        # 找出最慢的函数
        slow_functions = sorted(success_details, key=lambda x: x['execution_time'], reverse=True)[:3]
        print(f"\n最慢的函数:")
        for func in slow_functions:
            print(f"  • {func['function']}: {func['execution_time']:.2f}秒")
    
    # 6. 数据合理性分析
    print(f"\n📏 数据大小合理性分析")
    
    # 向量函数
    vector_functions = ['ai_text_to_embedding', 'ai_text_clustering_prepare']
    vector_results = [d for d in success_details if d['function'] in vector_functions]
    if vector_results:
        print(f"\n向量函数（大数据正常）:")
        for func in vector_results:
            print(f"  • {func['function']}: {func['result_size']:,} 字节 ✅")
    
    # 多模态内容函数
    content_functions = ['ai_image_describe', 'ai_image_ocr', 'ai_document_parse']
    content_results = [d for d in success_details if d['function'] in content_functions]
    if content_results:
        print(f"\n内容提取函数（丰富内容必要）:")
        for func in content_results:
            print(f"  • {func['function']}: {func['result_size']:,} 字节 ✅")
    
    # 需要优化的函数
    compact_functions = [
        'ai_text_summarize', 'ai_text_sentiment_analyze', 'ai_customer_segment',
        'ai_sales_lead_score', 'ai_review_analyze'
    ]
    compact_results = [d for d in success_details if d['function'] in compact_functions and d['result_size'] > 400]
    if compact_results:
        print(f"\n需要优化的函数:")
        for func in compact_results:
            compression = (1200 - func['result_size']) / 1200 * 100
            print(f"  • {func['function']}: {func['result_size']} 字节 (压缩率{compression:.1f}%)")
    
    # 7. 验收结论
    print(f"\n📋 验收结论")
    if all_passed and success_rate >= 75:
        print("✅ 功能验收通过！")
        print(f"• 整体成功率 {success_rate:.1f}% 达到要求")
        print("• 核心功能类别均满足验收标准")
    else:
        print("⚠️ 功能验收部分通过")
        print(f"• 需要修复 {len(failed_functions)} 个失败的函数")
        print("• 建议优化部分函数的返回大小")
    
    # 8. 下一步建议
    print(f"\n🚀 下一步建议")
    if failed_functions:
        print("1. 优先修复失败的函数，特别是API错误")
    if compact_results:
        print("2. 优化业务函数的返回格式，减少冗余")
    print("3. 对所有函数进行生产环境部署前的最终测试")
    print("4. 编写用户使用文档和最佳实践指南")


def check_category_rate(summary, category):
    """检查特定类别的成功率"""
    cat_stats = summary.get('by_category', {}).get(category, {})
    total = cat_stats.get('total', 0)
    success = cat_stats.get('success', 0)
    return (success / total * 100) if total > 0 else 0


if __name__ == '__main__':
    view_latest_test_results()