#!/usr/bin/env python3
"""
测试结果分析工具
分析测试报告，生成优化建议
"""

import json
import os
import glob
from datetime import datetime
from typing import Dict, List, Any


class TestResultAnalyzer:
    """测试结果分析器"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.jira_targets = {
            "compression_rate": 67,  # JIRA-001目标
            "max_response_size": 400,  # 字节
            "success_rate": 100,  # 百分比
            "max_response_time": 3.0  # 秒
        }
        
    def load_latest_report(self) -> Dict[str, Any]:
        """加载最新的测试报告"""
        report_files = glob.glob(os.path.join(self.data_dir, "test_report_*.json"))
        if not report_files:
            raise FileNotFoundError("未找到测试报告文件")
        
        # 获取最新的文件
        latest_file = max(report_files, key=os.path.getctime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_jira_compliance(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """分析JIRA-001合规性"""
        details = report.get("details", [])
        success_results = [r for r in details if r["status"] == "SUCCESS"]
        
        compliance = {
            "jira_001_status": "UNKNOWN",
            "metrics": {
                "compression": {
                    "target": self.jira_targets["compression_rate"],
                    "achieved": 0,
                    "compliant_functions": [],
                    "non_compliant_functions": []
                },
                "response_size": {
                    "target": self.jira_targets["max_response_size"],
                    "achieved": 0,
                    "compliant_functions": [],
                    "non_compliant_functions": []
                }
            }
        }
        
        # 分析每个成功的函数
        for result in success_results:
            func_name = result["function"]
            compression = result.get("compression_rate", 0)
            size = result.get("result_size", 0)
            
            # 检查压缩率
            if compression >= self.jira_targets["compression_rate"]:
                compliance["metrics"]["compression"]["compliant_functions"].append({
                    "name": func_name,
                    "rate": compression
                })
            else:
                compliance["metrics"]["compression"]["non_compliant_functions"].append({
                    "name": func_name,
                    "rate": compression,
                    "gap": self.jira_targets["compression_rate"] - compression
                })
            
            # 检查响应大小
            if size <= self.jira_targets["max_response_size"]:
                compliance["metrics"]["response_size"]["compliant_functions"].append({
                    "name": func_name,
                    "size": size
                })
            else:
                compliance["metrics"]["response_size"]["non_compliant_functions"].append({
                    "name": func_name,
                    "size": size,
                    "excess": size - self.jira_targets["max_response_size"]
                })
        
        # 计算整体合规率
        if success_results:
            compression_compliance = len(compliance["metrics"]["compression"]["compliant_functions"]) / len(success_results) * 100
            size_compliance = len(compliance["metrics"]["response_size"]["compliant_functions"]) / len(success_results) * 100
            
            compliance["metrics"]["compression"]["achieved"] = compression_compliance
            compliance["metrics"]["response_size"]["achieved"] = size_compliance
            
            # 判断JIRA-001状态
            if compression_compliance >= 80 and size_compliance >= 80:
                compliance["jira_001_status"] = "PASSED"
            elif compression_compliance >= 60 or size_compliance >= 60:
                compliance["jira_001_status"] = "PARTIAL"
            else:
                compliance["jira_001_status"] = "FAILED"
        
        return compliance
    
    def analyze_function_categories(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """分析各类函数的表现"""
        details = report.get("details", [])
        category_analysis = {}
        
        for result in details:
            category = result.get("category", "未知")
            if category not in category_analysis:
                category_analysis[category] = {
                    "total": 0,
                    "success": 0,
                    "failed": 0,
                    "avg_time": 0,
                    "avg_size": 0,
                    "functions": []
                }
            
            cat_data = category_analysis[category]
            cat_data["total"] += 1
            cat_data["functions"].append(result["function"])
            
            if result["status"] == "SUCCESS":
                cat_data["success"] += 1
                # 累积时间和大小用于计算平均值
                if "execution_time" in result:
                    cat_data["avg_time"] += result["execution_time"]
                if "result_size" in result:
                    cat_data["avg_size"] += result["result_size"]
            else:
                cat_data["failed"] += 1
        
        # 计算平均值
        for category, data in category_analysis.items():
            if data["success"] > 0:
                data["avg_time"] /= data["success"]
                data["avg_size"] /= data["success"]
                data["success_rate"] = data["success"] / data["total"] * 100
            else:
                data["success_rate"] = 0
        
        return category_analysis
    
    def generate_optimization_suggestions(self, report: Dict[str, Any], compliance: Dict[str, Any]) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 基于JIRA-001合规性的建议
        compression_non_compliant = compliance["metrics"]["compression"]["non_compliant_functions"]
        size_non_compliant = compliance["metrics"]["response_size"]["non_compliant_functions"]
        
        if compression_non_compliant:
            suggestions.append(f"🔧 压缩率优化: {len(compression_non_compliant)}个函数未达到67%压缩率目标")
            for func in compression_non_compliant[:5]:  # 只显示前5个
                suggestions.append(f"   • {func['name']}: 当前{func['rate']:.1f}%, 差距{func['gap']:.1f}%")
        
        if size_non_compliant:
            suggestions.append(f"📏 响应大小优化: {len(size_non_compliant)}个函数超过400字节限制")
            for func in size_non_compliant[:5]:
                suggestions.append(f"   • {func['name']}: {func['size']}字节, 超出{func['excess']}字节")
        
        # 基于失败函数的建议
        failed_results = [r for r in report.get("details", []) if r["status"] != "SUCCESS"]
        if failed_results:
            suggestions.append(f"\n❌ 失败函数修复: {len(failed_results)}个函数需要修复")
            
            # 按错误类型分组
            error_types = {}
            for result in failed_results:
                error_type = result.get("status", "UNKNOWN")
                if error_type not in error_types:
                    error_types[error_type] = []
                error_types[error_type].append(result["function"])
            
            for error_type, functions in error_types.items():
                suggestions.append(f"   • {error_type}: {', '.join(functions[:3])}")
        
        # 性能优化建议
        details = report.get("details", [])
        slow_functions = [r for r in details if r.get("status") == "SUCCESS" and r.get("execution_time", 0) > 3.0]
        if slow_functions:
            suggestions.append(f"\n⏱️ 性能优化: {len(slow_functions)}个函数响应时间超过3秒")
            for func in sorted(slow_functions, key=lambda x: x["execution_time"], reverse=True)[:3]:
                suggestions.append(f"   • {func['function']}: {func['execution_time']:.2f}秒")
        
        return suggestions
    
    def generate_report(self):
        """生成分析报告"""
        try:
            # 加载最新报告
            report = self.load_latest_report()
            
            print("📊 测试结果分析报告")
            print("=" * 80)
            print(f"测试时间: {report.get('test_time', 'N/A')}")
            
            # 总体统计
            summary = report.get("summary", {})
            print(f"\n📈 总体统计:")
            print(f"  • 测试函数: {summary.get('total', 0)}个")
            print(f"  • 成功: {summary.get('success', 0)}个")
            print(f"  • 失败: {summary.get('failed', 0)}个")
            
            success_rate = summary.get('success', 0) / summary.get('total', 1) * 100
            print(f"  • 成功率: {success_rate:.1f}%")
            
            # JIRA-001合规性分析
            print(f"\n🎯 JIRA-001合规性分析:")
            compliance = self.analyze_jira_compliance(report)
            
            print(f"  状态: {compliance['jira_001_status']}")
            print(f"  • 压缩率达标: {compliance['metrics']['compression']['achieved']:.1f}%")
            print(f"  • 响应大小达标: {compliance['metrics']['response_size']['achieved']:.1f}%")
            
            # 分类分析
            print(f"\n📂 分类性能分析:")
            category_analysis = self.analyze_function_categories(report)
            
            for category, data in category_analysis.items():
                print(f"\n  {category}:")
                print(f"    • 函数数: {data['total']}")
                print(f"    • 成功率: {data.get('success_rate', 0):.1f}%")
                if data["success"] > 0:
                    print(f"    • 平均响应时间: {data['avg_time']:.2f}秒")
                    print(f"    • 平均返回大小: {data['avg_size']:.0f}字节")
            
            # 优化建议
            print(f"\n💡 优化建议:")
            suggestions = self.generate_optimization_suggestions(report, compliance)
            for suggestion in suggestions:
                print(f"  {suggestion}")
            
            # 保存详细分析结果
            self.save_analysis_results(report, compliance, category_analysis, suggestions)
            
        except Exception as e:
            print(f"❌ 分析失败: {str(e)}")
    
    def save_analysis_results(self, report, compliance, category_analysis, suggestions):
        """保存分析结果"""
        analysis_result = {
            "analysis_time": datetime.now().isoformat(),
            "test_report_time": report.get("test_time"),
            "jira_001_compliance": compliance,
            "category_performance": category_analysis,
            "optimization_suggestions": suggestions,
            "summary": {
                "total_functions": report["summary"]["total"],
                "success_rate": report["summary"]["success"] / report["summary"]["total"] * 100,
                "jira_001_status": compliance["jira_001_status"]
            }
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        analysis_file = os.path.join(self.data_dir, f"analysis_result_{timestamp}.json")
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 分析结果已保存: {analysis_file}")


def main():
    """主函数"""
    analyzer = TestResultAnalyzer()
    analyzer.generate_report()
    
    print("\n✅ 分析完成!")
    print("\n下一步建议:")
    print("1. 根据优化建议修改相应函数")
    print("2. 重新运行测试验证改进效果")
    print("3. 关注未达到JIRA-001目标的函数")


if __name__ == '__main__':
    main()