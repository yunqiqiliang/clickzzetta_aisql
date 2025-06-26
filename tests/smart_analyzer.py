#!/usr/bin/env python3
"""
智能测试分析器
根据函数类型应用不同的评估标准
"""

import json
import os
import glob
from datetime import datetime
from typing import Dict, List, Tuple


class SmartTestAnalyzer:
    """智能测试分析器"""
    
    def __init__(self):
        # 定义不同类型函数的合理预期
        self.function_expectations = {
            # 文本处理函数 - 应该精简
            "text_compact": {
                "functions": [
                    "ai_text_summarize", "ai_text_translate", "ai_text_sentiment_analyze",
                    "ai_text_extract_entities", "ai_text_extract_keywords", "ai_text_classify",
                    "ai_text_clean_normalize", "ai_auto_tag_generate"
                ],
                "max_size": 400,
                "target_compression": 67,
                "description": "文本处理函数（应精简）"
            },
            
            # 向量函数 - 大数据是正常的
            "vector_large": {
                "functions": [
                    "ai_text_to_embedding", "ai_text_clustering_prepare"
                ],
                "max_size": None,  # 不限制大小
                "target_compression": None,  # 不要求压缩
                "description": "向量函数（大数据正常）"
            },
            
            # 向量搜索函数 - 中等大小
            "vector_search": {
                "functions": [
                    "ai_semantic_similarity", "ai_find_similar_text", "ai_document_search"
                ],
                "max_size": 5000,
                "target_compression": 30,
                "description": "向量搜索函数（中等大小）"
            },
            
            # 多模态内容函数 - 内容丰富是必要的
            "multimodal_content": {
                "functions": [
                    "ai_image_describe", "ai_image_ocr", "ai_document_parse"
                ],
                "max_size": None,  # 取决于内容
                "target_compression": None,
                "description": "多模态内容函数（内容丰富必要）"
            },
            
            # 多模态分析函数 - 适度控制
            "multimodal_analysis": {
                "functions": [
                    "ai_image_analyze", "ai_chart_analyze", "ai_video_summarize",
                    "ai_image_to_embedding", "ai_image_similarity"
                ],
                "max_size": 5000,
                "target_compression": 30,
                "description": "多模态分析函数（适度控制）"
            },
            
            # 业务场景函数 - 应该精简
            "business_compact": {
                "functions": [
                    "ai_customer_intent_analyze", "ai_sales_lead_score", "ai_review_analyze",
                    "ai_risk_text_detect", "ai_contract_extract", "ai_resume_parse",
                    "ai_customer_segment", "ai_product_description_generate", "ai_industry_classification"
                ],
                "max_size": 800,
                "target_compression": 50,
                "description": "业务场景函数（应精简）"
            }
        }
        
        # 创建函数到类型的映射
        self.function_type_map = {}
        for type_name, config in self.function_expectations.items():
            for func in config["functions"]:
                self.function_type_map[func] = type_name
    
    def get_function_type(self, function_name: str) -> Tuple[str, Dict]:
        """获取函数类型和预期"""
        type_name = self.function_type_map.get(function_name, "unknown")
        expectations = self.function_expectations.get(type_name, {
            "max_size": 1000,
            "target_compression": 50,
            "description": "未分类函数"
        })
        return type_name, expectations
    
    def evaluate_function_result(self, result: Dict) -> Dict:
        """评估单个函数结果"""
        func_name = result.get("function", "")
        func_type, expectations = self.get_function_type(func_name)
        
        evaluation = {
            "function": func_name,
            "type": func_type,
            "status": result.get("status", "UNKNOWN"),
            "expectations": expectations["description"]
        }
        
        if result["status"] == "SUCCESS":
            size = result.get("result_size", 0)
            compression = result.get("compression_rate", 0)
            
            # 根据函数类型评估
            if expectations["max_size"] is None:
                # 不限制大小的函数
                evaluation["size_status"] = "OK"
                evaluation["size_message"] = f"{size}字节（不限制）"
            elif size <= expectations["max_size"]:
                evaluation["size_status"] = "GOOD"
                evaluation["size_message"] = f"{size}字节（目标≤{expectations['max_size']}）"
            else:
                evaluation["size_status"] = "NEED_OPTIMIZE"
                evaluation["size_message"] = f"{size}字节（超出{size - expectations['max_size']}字节）"
            
            if expectations["target_compression"] is None:
                # 不要求压缩的函数
                evaluation["compression_status"] = "OK"
                evaluation["compression_message"] = f"{compression:.1f}%（不要求）"
            elif compression >= expectations["target_compression"]:
                evaluation["compression_status"] = "GOOD"
                evaluation["compression_message"] = f"{compression:.1f}%（目标≥{expectations['target_compression']}%）"
            else:
                evaluation["compression_status"] = "NEED_OPTIMIZE"
                evaluation["compression_message"] = f"{compression:.1f}%（差{expectations['target_compression'] - compression:.1f}%）"
            
            # 综合评估
            if evaluation["size_status"] in ["OK", "GOOD"] and evaluation["compression_status"] in ["OK", "GOOD"]:
                evaluation["overall"] = "PASS"
            elif "NEED_OPTIMIZE" in [evaluation["size_status"], evaluation["compression_status"]]:
                evaluation["overall"] = "OPTIMIZE"
            else:
                evaluation["overall"] = "CHECK"
        else:
            evaluation["overall"] = "FAIL"
            evaluation["error"] = result.get("error", "Unknown error")
        
        return evaluation
    
    def analyze_report(self, report_path: str = None):
        """分析测试报告"""
        # 加载报告
        if not report_path:
            report_files = glob.glob("data/test_report_*.json")
            if not report_files:
                print("❌ 未找到测试报告")
                return
            report_path = max(report_files, key=os.path.getctime)
        
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        print("🧠 智能测试分析报告")
        print("=" * 80)
        print(f"📅 测试时间: {report.get('test_time', 'N/A')}")
        print(f"📄 报告文件: {report_path}")
        print("=" * 80)
        
        # 分析每个函数
        evaluations = []
        for result in report.get("details", []):
            eval_result = self.evaluate_function_result(result)
            evaluations.append(eval_result)
        
        # 按类型分组统计
        type_stats = {}
        for eval_result in evaluations:
            func_type = eval_result["type"]
            if func_type not in type_stats:
                type_stats[func_type] = {
                    "total": 0, "pass": 0, "optimize": 0, "fail": 0,
                    "functions": []
                }
            
            type_stats[func_type]["total"] += 1
            type_stats[func_type]["functions"].append(eval_result)
            
            if eval_result["overall"] == "PASS":
                type_stats[func_type]["pass"] += 1
            elif eval_result["overall"] == "OPTIMIZE":
                type_stats[func_type]["optimize"] += 1
            elif eval_result["overall"] == "FAIL":
                type_stats[func_type]["fail"] += 1
        
        # 输出分类统计
        print("\n📊 分类统计")
        for type_name, config in self.function_expectations.items():
            if type_name in type_stats:
                stats = type_stats[type_name]
                print(f"\n🏷️ {config['description']}")
                print(f"  总数: {stats['total']} | ✅ 通过: {stats['pass']} | 🔧 需优化: {stats['optimize']} | ❌ 失败: {stats['fail']}")
        
        # 详细问题分析
        print("\n\n📋 详细分析")
        
        # 1. 失败的函数
        failed = [e for e in evaluations if e["overall"] == "FAIL"]
        if failed:
            print("\n❌ 失败函数（需要修复）")
            for e in failed:
                print(f"  • {e['function']}: {e.get('error', 'Unknown error')}")
        
        # 2. 需要优化的函数（但要考虑类型）
        need_optimize = [e for e in evaluations if e["overall"] == "OPTIMIZE"]
        if need_optimize:
            print("\n🔧 需要优化的函数")
            # 只显示真正需要优化的（排除向量和内容类函数）
            real_optimize = [e for e in need_optimize if e["type"] not in ["vector_large", "multimodal_content"]]
            for e in real_optimize:
                print(f"  • {e['function']} ({e['expectations']})")
                if "size_message" in e:
                    print(f"    - 大小: {e['size_message']}")
                if "compression_message" in e:
                    print(f"    - 压缩: {e['compression_message']}")
        
        # 3. 特殊说明
        print("\n💡 特殊说明")
        
        # 向量函数
        vector_funcs = [e for e in evaluations if e["type"] == "vector_large" and e["status"] == "SUCCESS"]
        if vector_funcs:
            print("\n📐 向量函数（大数据是正常的）")
            for e in vector_funcs:
                size = next((r["result_size"] for r in report["details"] if r["function"] == e["function"]), 0)
                print(f"  • {e['function']}: {size:,} 字节 ✅")
        
        # OCR和文档解析
        content_funcs = [e for e in evaluations if e["type"] == "multimodal_content" and e["status"] == "SUCCESS"]
        if content_funcs:
            print("\n📄 内容提取函数（完整内容是必要的）")
            for e in content_funcs:
                size = next((r["result_size"] for r in report["details"] if r["function"] == e["function"]), 0)
                print(f"  • {e['function']}: {size:,} 字节 ✅")
        
        # 生成建议
        self.generate_recommendations(evaluations)
    
    def generate_recommendations(self, evaluations: List[Dict]):
        """生成优化建议"""
        print("\n\n🎯 优化建议")
        print("=" * 60)
        
        # 统计真正需要行动的项
        real_issues = []
        
        for e in evaluations:
            if e["overall"] == "FAIL":
                real_issues.append({
                    "priority": 1,
                    "function": e["function"],
                    "action": "修复错误",
                    "detail": e.get("error", "")
                })
            elif e["overall"] == "OPTIMIZE" and e["type"] in ["text_compact", "business_compact"]:
                real_issues.append({
                    "priority": 2,
                    "function": e["function"],
                    "action": "优化大小",
                    "detail": f"{e.get('size_message', '')} / {e.get('compression_message', '')}"
                })
        
        # 按优先级排序
        real_issues.sort(key=lambda x: x["priority"])
        
        if real_issues:
            print("\n需要处理的问题：")
            current_priority = None
            for issue in real_issues:
                if issue["priority"] != current_priority:
                    current_priority = issue["priority"]
                    priority_name = "🚨 紧急" if current_priority == 1 else "⚠️ 重要"
                    print(f"\n{priority_name}:")
                print(f"  • {issue['function']}: {issue['action']}")
                if issue["detail"]:
                    print(f"    {issue['detail']}")
        else:
            print("\n✅ 所有函数都在合理范围内！")
        
        print("\n📌 总结：")
        success_count = sum(1 for e in evaluations if e["overall"] in ["PASS", "OK"])
        total_count = len(evaluations)
        print(f"  • 符合预期: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
        print(f"  • 需要修复: {len([e for e in evaluations if e['overall'] == 'FAIL'])} 个")
        print(f"  • 建议优化: {len([e for e in real_issues if e['priority'] == 2])} 个")


def main():
    """主函数"""
    analyzer = SmartTestAnalyzer()
    analyzer.analyze_report()
    
    print("\n\n✅ 智能分析完成！")
    print("\n根据函数类型的不同特点，给出了差异化的评估和建议。")


if __name__ == '__main__':
    main()