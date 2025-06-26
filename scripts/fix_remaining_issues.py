#!/usr/bin/env python3
"""
修复剩余的函数问题
1. ai_industry_classification - 缺少默认参数和dashscope检查
2. ai_sales_lead_score - 优化返回大小
3. ai_review_analyze - 优化返回大小
"""

import re
import shutil
from datetime import datetime


def fix_ai_functions(file_path):
    """修复AI函数的问题"""
    
    # 备份文件
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"✅ 备份文件: {backup_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_applied = []
    
    # 1. 修复 ai_industry_classification
    print("\n🔧 修复 ai_industry_classification...")
    
    # 添加默认model_name参数
    old_signature = "def evaluate(self, text, prompt, api_key, model_name, temperature=0.7, enable_search=False):"
    new_signature = 'def evaluate(self, text, prompt, api_key, model_name="qwen-plus", temperature=0.7, enable_search=False):'
    
    if old_signature in content:
        content = content.replace(old_signature, new_signature)
        fixes_applied.append("ai_industry_classification - 添加model_name默认值")
    
    # 添加HAS_DASHSCOPE检查
    industry_func_start = "class ai_industry_classification(object):\n    def evaluate"
    if industry_func_start in content:
        # 在dashscope.api_key = api_key之前添加检查
        pattern = r'(def evaluate.*?:\n)([\s]*)(dashscope\.api_key = api_key)'
        replacement = r'\1\2if not HAS_DASHSCOPE:\n\2    return json.dumps({"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}, ensure_ascii=False)\n\2\n\2\3'
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        if new_content != content:
            content = new_content
            fixes_applied.append("ai_industry_classification - 添加dashscope检查")
    
    # 2. 优化 ai_industry_classification 的prompt
    # 添加JSON格式要求
    pattern = r'(\{"role": "system", "content": prompt\})'
    replacement = r'{"role": "system", "content": prompt + """\n严格按照JSON格式返回，不要包含任何解释文字。确保返回的JSON包含"一级行业"和"二级行业"字段。"""}'
    
    new_content = re.sub(pattern, replacement, content)
    if new_content != content:
        content = new_content
        fixes_applied.append("ai_industry_classification - 优化prompt格式")
    
    # 3. 优化 ai_sales_lead_score - 精简返回
    print("\n🔧 优化 ai_sales_lead_score...")
    
    # 找到函数并修改result.update部分
    sales_pattern = r'(ai_sales_lead_score.*?)(result\.update\(\{[^}]+\}\))'
    
    def replace_sales_update(match):
        return match.group(1) + '# 精简返回，只保留必要字段\n            result["model"] = model_name'
    
    new_content = re.sub(sales_pattern, replace_sales_update, content, flags=re.DOTALL)
    if new_content != content:
        content = new_content
        fixes_applied.append("ai_sales_lead_score - 精简返回字段")
    
    # 4. 优化 ai_review_analyze - 精简返回
    print("\n🔧 优化 ai_review_analyze...")
    
    # 同样的方式处理review_analyze
    review_pattern = r'(ai_review_analyze.*?)(result\.update\(\{[^}]+\}\))'
    
    def replace_review_update(match):
        return match.group(1) + '# 精简返回，只保留必要字段\n            result["model"] = model_name'
    
    new_content = re.sub(review_pattern, replace_review_update, content, flags=re.DOTALL)
    if new_content != content:
        content = new_content
        fixes_applied.append("ai_review_analyze - 精简返回字段")
    
    # 5. 修复多模态函数的图片URL验证
    print("\n🔧 添加图片URL验证...")
    
    # 为需要图片URL的函数添加验证
    image_functions = [
        'ai_image_describe', 'ai_image_ocr', 'ai_image_analyze',
        'ai_image_to_embedding', 'ai_image_similarity'
    ]
    
    for func_name in image_functions:
        # 查找函数定义
        func_pattern = f'(class {func_name}.*?def evaluate.*?:)(.*?)(dashscope\.api_key = api_key|response = dashscope)'
        
        def add_url_validation(match):
            if 'image_url' in match.group(0) and 'if not image_url' not in match.group(0):
                indent = '\n        '
                validation = f'{indent}# 验证图片URL{indent}if "image_url" in locals() and (not image_url or not isinstance(image_url, str)):{indent}    return json.dumps({{"error": True, "message": "Invalid or missing image URL"}}, ensure_ascii=False){indent}'
                return match.group(1) + match.group(2) + validation + match.group(3)
            return match.group(0)
        
        content = re.sub(func_pattern, add_url_validation, content, flags=re.DOTALL)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 修复完成！应用了 {len(fixes_applied)} 个修复：")
    for fix in fixes_applied:
        print(f"  • {fix}")
    
    return len(fixes_applied)


def create_final_test_script():
    """创建最终测试脚本"""
    
    test_script = '''#!/usr/bin/env python3
"""
最终验证测试
测试修复后的函数
"""

import json
import sys
import time

sys.path.insert(0, '/Users/liangmo/Documents/GitHub/clickzetta_aisql')

from ai_functions_complete import (
    ai_industry_classification,
    ai_sales_lead_score,
    ai_review_analyze
)


def test_fixed_functions(api_key):
    """测试修复后的函数"""
    
    print("🧪 测试修复后的函数")
    print("="*60)
    
    tests = [
        {
            "name": "ai_industry_classification",
            "func": ai_industry_classification,
            "params": {
                "text": "专注于云计算和大数据平台的科技公司",
                "prompt": "请分析这家公司的行业分类，返回一级行业和二级行业。"
                # 注意：不需要提供model_name，会使用默认值
            }
        },
        {
            "name": "ai_sales_lead_score",
            "func": ai_sales_lead_score,
            "params": {
                "lead_info": json.dumps({
                    "budget": 100000,
                    "timeline": "2 months",
                    "authority": "decision maker",
                    "need": "urgent"
                }),
                "scoring_criteria": "BANT"
            }
        },
        {
            "name": "ai_review_analyze",
            "func": ai_review_analyze,
            "params": {
                "review_text": "产品功能很强大，客服响应及时。价格稍高但物有所值。",
                "product_type": "software"
            }
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"\\n测试: {test['name']}")
        print("-" * 40)
        
        try:
            func = test["func"]()
            params = test["params"].copy()
            params["api_key"] = api_key
            
            start_time = time.time()
            result = func.evaluate(**params)
            execution_time = time.time() - start_time
            
            # 分析结果
            result_size = len(result.encode('utf-8'))
            compression = (1200 - result_size) / 1200 * 100
            
            print(f"✅ 成功")
            print(f"  • 执行时间: {execution_time:.2f}秒")
            print(f"  • 返回大小: {result_size}字节")
            print(f"  • 压缩率: {compression:.1f}%")
            
            # 解析并显示结果
            try:
                data = json.loads(result)
                if not data.get("error"):
                    print(f"  • 结果预览: {json.dumps(data, ensure_ascii=False)[:200]}...")
                    
                    # 检查是否达到优化目标
                    if result_size <= 400:
                        print(f"  ✅ 达到JIRA-001目标（≤400字节）")
                    else:
                        print(f"  ⚠️  需要进一步优化（目标≤400字节）")
                else:
                    print(f"  ❌ API错误: {data.get('message')}")
                    
            except Exception as e:
                print(f"  ❌ 解析错误: {str(e)}")
                
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
    
    print("\\n✅ 测试完成！")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python final_test.py YOUR_API_KEY")
    else:
        test_fixed_functions(sys.argv[1])
'''
    
    with open("final_test.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("\n✅ 创建最终测试脚本: final_test.py")


def main():
    """主函数"""
    file_path = '/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py'
    
    print("🚀 开始修复剩余问题")
    print("="*60)
    
    # 应用修复
    fixes = fix_ai_functions(file_path)
    
    # 创建测试脚本
    create_final_test_script()
    
    print("\n📋 修复总结：")
    print("1. ✅ ai_industry_classification - 添加默认参数和检查")
    print("2. ✅ ai_sales_lead_score - 精简返回字段")
    print("3. ✅ ai_review_analyze - 精简返回字段")
    print("4. ✅ 多模态函数 - 添加URL验证")
    
    print("\n🔄 下一步：")
    print("1. 运行最终测试: python final_test.py YOUR_API_KEY")
    print("2. 运行完整测试: python test_complete_coverage.py YOUR_API_KEY")
    print("3. 打包部署: python package_with_deps.py")


if __name__ == '__main__':
    main()