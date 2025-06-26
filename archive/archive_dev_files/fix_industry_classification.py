#!/usr/bin/env python3
"""
修复 ai_industry_classification 函数
1. 添加 model_name 默认参数
2. 添加 HAS_DASHSCOPE 检查
3. 优化 prompt 格式
"""

import re
import shutil
from datetime import datetime


def fix_industry_classification(file_path):
    """修复行业分类函数"""
    
    # 备份文件
    backup_path = f"{file_path}.backup_industry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"✅ 备份文件: {backup_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_applied = []
    
    # 1. 修复函数签名 - 添加 model_name 默认值
    print("\n🔧 修复函数签名...")
    
    old_signature = "def evaluate(self, text, prompt, api_key, model_name, temperature=0.7, enable_search=False):"
    new_signature = 'def evaluate(self, text, prompt, api_key, model_name="qwen-plus", temperature=0.7, enable_search=False):'
    
    if old_signature in content:
        content = content.replace(old_signature, new_signature)
        fixes_applied.append("添加 model_name 默认参数")
        print("  ✅ 添加 model_name='qwen-plus' 默认值")
    
    # 2. 添加 HAS_DASHSCOPE 检查
    print("\n🔧 添加 dashscope 检查...")
    
    # 查找函数开始位置
    pattern = r'(class ai_industry_classification.*?def evaluate.*?:\n)([\s]*)(dashscope\.api_key = api_key)'
    
    def add_dashscope_check(match):
        indent = match.group(2)
        check_code = f'''{indent}if not HAS_DASHSCOPE:
{indent}    return json.dumps({{"error": True, "message": "DashScope library not available. Please ensure the deployment package includes all dependencies."}}, ensure_ascii=False)
{indent}
{indent}'''
        return match.group(1) + check_code + match.group(3)
    
    new_content = re.sub(pattern, add_dashscope_check, content, flags=re.DOTALL)
    if new_content != content:
        content = new_content
        fixes_applied.append("添加 HAS_DASHSCOPE 检查")
        print("  ✅ 添加 dashscope 库检查")
    
    # 3. 优化 prompt 处理，添加 JSON 格式要求
    print("\n🔧 优化 prompt 格式...")
    
    # 查找 messages 定义
    pattern = r'(messages = \[\s*\{"role": "system", "content": prompt\})'
    
    def optimize_prompt(match):
        return '''messages = [
            {"role": "system", "content": prompt + """
严格按照JSON格式返回，不要包含任何解释文字。
确保返回的JSON包含"一级行业"和"二级行业"字段。
示例格式：{"一级行业": "信息技术", "二级行业": "云计算服务"}"""}'''
    
    new_content = re.sub(pattern, optimize_prompt, content)
    if new_content != content:
        content = new_content
        fixes_applied.append("优化 prompt 格式")
        print("  ✅ 添加 JSON 格式要求")
    
    # 4. 改进错误处理
    print("\n🔧 改进错误处理...")
    
    # 查找错误处理部分，确保返回正确的默认值
    pattern = r'(result = \{"一级行业": "未能解析", "二级行业": "未能解析", "原始内容": full_content\})'
    replacement = '''result = {"一级行业": "未能解析", "二级行业": "未能解析", "原始内容": full_content[:200] if len(full_content) > 200 else full_content}'''
    
    if pattern in content:
        content = re.sub(pattern, replacement, content)
        fixes_applied.append("优化错误处理")
        print("  ✅ 限制原始内容长度")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 修复完成！应用了 {len(fixes_applied)} 个修复：")
    for i, fix in enumerate(fixes_applied, 1):
        print(f"  {i}. {fix}")
    
    return fixes_applied


def create_test_script():
    """创建测试脚本"""
    
    test_script = '''#!/usr/bin/env python3
"""
测试修复后的 ai_industry_classification 函数
"""

import json
import sys
import time
from datetime import datetime

sys.path.insert(0, '/Users/liangmo/Documents/GitHub/clickzetta_aisql')

from ai_functions_complete import ai_industry_classification


def test_industry_classification(api_key):
    """测试行业分类函数"""
    
    print("🏢 测试行业分类函数")
    print("="*60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 测试用例
    test_cases = [
        {
            "text": "专注于云计算和大数据分析平台的科技公司",
            "prompt": "请分析这家公司的行业分类，返回一级行业和二级行业。"
        },
        {
            "text": "提供在线教育和培训服务的互联网平台",
            "prompt": "判断该企业所属行业类别。"
        },
        {
            "text": "生产新能源汽车电池的制造企业",
            "prompt": "分析企业行业归属。"
        },
        {
            "text": "连锁餐饮品牌，主营火锅和中式快餐",
            "prompt": "确定该企业的行业分类。"
        }
    ]
    
    # 测试不同参数组合
    print("\\n1️⃣ 测试默认参数（不提供 model_name）")
    print("-" * 40)
    
    func = ai_industry_classification()
    result = func.evaluate(
        text=test_cases[0]["text"],
        prompt=test_cases[0]["prompt"],
        api_key=api_key
        # 注意：不提供 model_name，应该使用默认值 "qwen-plus"
    )
    
    analyze_result(result, test_cases[0]["text"])
    
    # 测试所有用例
    print("\\n2️⃣ 测试多个行业案例")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\\n案例 {i}: {test_case['text'][:30]}...")
        
        func = ai_industry_classification()
        start_time = time.time()
        
        result = func.evaluate(
            text=test_case["text"],
            prompt=test_case["prompt"],
            api_key=api_key,
            temperature=0.3  # 降低温度以获得更稳定的结果
        )
        
        execution_time = time.time() - start_time
        analyze_result(result, test_case["text"], execution_time)
    
    # 测试错误处理
    print("\\n3️⃣ 测试错误处理")
    print("-" * 40)
    
    # 测试无效输入
    func = ai_industry_classification()
    result = func.evaluate(
        text="",
        prompt="分析行业",
        api_key=api_key
    )
    print("空文本测试:")
    analyze_result(result, "")


def analyze_result(result, input_text, execution_time=None):
    """分析测试结果"""
    
    try:
        data = json.loads(result)
        
        if data.get("error"):
            print(f"  ❌ 错误: {data.get('message')}")
        else:
            print(f"  ✅ 成功")
            if execution_time:
                print(f"  • 执行时间: {execution_time:.2f}秒")
            
            # 显示结果
            print(f"  • 一级行业: {data.get('一级行业', '未知')}")
            print(f"  • 二级行业: {data.get('二级行业', '未知')}")
            
            # 检查数据大小和格式
            result_size = len(result.encode('utf-8'))
            compression = (1200 - result_size) / 1200 * 100
            print(f"  • 数据大小: {result_size} 字节 (压缩率: {compression:.1f}%)")
            
            # 验证必要字段
            if "一级行业" in data and "二级行业" in data:
                print(f"  ✅ 格式正确")
            else:
                print(f"  ⚠️  缺少必要字段")
                
    except Exception as e:
        print(f"  ❌ 解析失败: {str(e)}")
        print(f"  原始结果: {result[:200]}...")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python test_industry_classification.py YOUR_API_KEY")
        return
    
    api_key = sys.argv[1]
    
    print("🚀 开始测试修复后的行业分类函数")
    print()
    
    test_industry_classification(api_key)
    
    print("\\n✅ 测试完成！")
    print("\\n📋 验收要点：")
    print("1. 默认参数是否生效（不提供 model_name）")
    print("2. 返回格式是否正确（包含一级/二级行业）")
    print("3. 数据大小是否合理（应该 <400 字节）")
    print("4. 错误处理是否正常")


if __name__ == '__main__':
    main()
'''
    
    with open("test_industry_classification.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("\n✅ 创建测试脚本: test_industry_classification.py")


def show_before_after():
    """显示修复前后对比"""
    
    print("\n📝 修复前后对比")
    print("="*60)
    
    print("\n修复前的问题：")
    print("```python")
    print("# 1. 缺少默认参数")
    print("def evaluate(self, text, prompt, api_key, model_name, temperature=0.7, enable_search=False):")
    print("    # 如果不提供 model_name 会报错")
    print("")
    print("# 2. 缺少 dashscope 检查")
    print("dashscope.api_key = api_key  # 如果没有 dashscope 库会崩溃")
    print("")
    print("# 3. 返回格式不稳定")
    print('{"role": "system", "content": prompt}  # 可能返回非JSON格式')
    print("```")
    
    print("\n修复后的改进：")
    print("```python")
    print("# 1. 添加默认参数")
    print('def evaluate(self, text, prompt, api_key, model_name="qwen-plus", temperature=0.7, enable_search=False):')
    print("")
    print("# 2. 添加库检查")
    print("if not HAS_DASHSCOPE:")
    print('    return json.dumps({"error": True, "message": "DashScope library not available..."}, ensure_ascii=False)')
    print("")
    print("# 3. 强制JSON格式")
    print('{"role": "system", "content": prompt + """')
    print('严格按照JSON格式返回，不要包含任何解释文字。')
    print('确保返回的JSON包含"一级行业"和"二级行业"字段。')
    print('示例格式：{"一级行业": "信息技术", "二级行业": "云计算服务"}"""}')
    print("```")


def main():
    """主函数"""
    file_path = '/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py'
    
    print("🚀 修复 ai_industry_classification 函数")
    print("="*60)
    
    # 应用修复
    fixes = fix_industry_classification(file_path)
    
    # 创建测试脚本
    create_test_script()
    
    # 显示对比
    show_before_after()
    
    print("\n🎯 修复完成！")
    print("\n🔄 下一步：")
    print("1. 运行测试: python test_industry_classification.py YOUR_API_KEY")
    print("2. 验证修复效果")
    print("3. 运行完整测试: python test_complete_coverage.py YOUR_API_KEY")
    
    print("\n📌 预期效果：")
    print("• 不提供 model_name 时自动使用 'qwen-plus'")
    print("• 返回标准的行业分类 JSON 格式")
    print("• 数据大小应该 <400 字节")
    print("• 没有 dashscope 库时返回友好错误")


if __name__ == '__main__':
    main()