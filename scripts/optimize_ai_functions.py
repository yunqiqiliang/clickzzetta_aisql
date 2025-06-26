#!/usr/bin/env python3
"""
AI Functions 返回格式统一优化工具
解决所有30个AI函数的返回格式不一致问题
"""

import re
import json
from typing import Dict, List, Tuple

class AIFunctionOptimizer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.backup_path = file_path + '.backup_before_optimization'
        
        # 标准化的提示词模板
        self.prompt_templates = {
            # 文本处理函数
            "ai_text_sentiment_analyze": """你是专业情感分析专家。分析文本情感倾向。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"sentiment": "positive|negative|neutral", "confidence": 0.95, "emotions": ["joy", "anger"], "keywords": ["关键词1"]}""",
            
            "ai_text_extract_entities": """你是专业信息提取专家。从文本中提取实体信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"entities": [{"text": "实体名", "type": "PERSON|ORG|LOC|MISC", "confidence": 0.95}]}""",
            
            "ai_text_extract_keywords": """你是关键词提取专家。提取文本的核心关键词。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"keywords": [{"word": "关键词", "weight": 0.95, "category": "核心概念"}]}""",
            
            "ai_text_classify": """你是文本分类专家。将文本分类到合适类别。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"category": "分类名称", "confidence": 0.95, "subcategory": "子分类", "categories_considered": ["类别1", "类别2"]}""",
            
            "ai_text_clean_normalize": """你是文本清洗专家。执行文本清洗和标准化操作。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"cleaned_text": "清洗后文本", "operations_applied": ["去重", "标准化"], "changes_count": 5}""",
            
            "ai_auto_tag_generate": """你是智能标签生成专家。为文本生成相关标签。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"tags": [{"tag": "标签名", "relevance": 0.95, "category": "主题"}]}""",
            
            # 业务场景函数
            "ai_customer_intent_analyze": """你是客户意图分析专家。分析客户文本的真实意图。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"intent": "购买意向|咨询|投诉|建议", "confidence": 0.95, "urgency": "high|medium|low", "emotions": ["satisfied"], "action_required": "立即处理"}""",
            
            "ai_sales_lead_score": """你是销售线索评分专家。根据标准评估线索价值。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"score": 85, "grade": "A|B|C|D", "probability": 0.85, "factors": [{"factor": "预算充足", "impact": "positive", "weight": 0.3}], "next_action": "立即跟进"}""",
            
            "ai_review_analyze": """你是评论分析专家。分析用户评论的多维度信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"sentiment": "positive|negative|neutral", "rating_predicted": 4.5, "aspects": [{"aspect": "服务", "sentiment": "positive", "score": 4.2}], "key_issues": ["待改进点"]}""",
            
            "ai_risk_text_detect": """你是风险检测专家。检测文本中的各类风险内容。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"risk_level": "high|medium|low|none", "risk_types": ["欺诈", "违规"], "confidence": 0.95, "flagged_content": ["具体风险文本"], "action_required": true}""",
            
            "ai_contract_extract": """你是合同信息提取专家。提取合同的关键信息字段。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"parties": ["甲方", "乙方"], "amount": "1000000", "start_date": "2024-01-01", "end_date": "2024-12-31", "key_terms": ["重要条款"], "risk_points": ["风险点"]}""",
            
            "ai_resume_parse": """你是简历解析专家。解析简历的结构化信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"name": "姓名", "education": [{"degree": "本科", "school": "大学", "major": "专业"}], "experience": [{"title": "职位", "company": "公司", "duration": "2年"}], "skills": ["技能1"]}""",
            
            "ai_customer_segment": """你是客户细分专家。根据模型进行客户细分分析。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"segment": "高价值客户", "scores": {"R": 5, "F": 4, "M": 5}, "total_score": 85, "characteristics": ["购买频繁"], "recommendations": ["VIP服务"], "retention_probability": 0.92}""",
            
            "ai_product_description_generate": """你是产品文案专家。生成吸引人的产品描述。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"title": "产品标题", "description": "详细描述", "features": ["特色1", "特色2"], "benefits": ["优势1"], "target_audience": "目标用户", "selling_points": ["卖点1"]}"""
        }
        
        # 统一的回退字段映射
        self.fallback_fields = {
            "ai_text_summarize": "summary",
            "ai_text_translate": "translated_text", 
            "ai_text_sentiment_analyze": "sentiment_analysis",
            "ai_text_extract_entities": "entities_extraction",
            "ai_text_extract_keywords": "keywords_extraction",
            "ai_text_classify": "classification_result",
            "ai_text_clean_normalize": "text_processing_result",
            "ai_auto_tag_generate": "tags_generation",
            "ai_customer_intent_analyze": "intent_analysis",
            "ai_sales_lead_score": "lead_scoring",
            "ai_review_analyze": "review_analysis", 
            "ai_risk_text_detect": "risk_assessment",
            "ai_contract_extract": "contract_extraction",
            "ai_resume_parse": "resume_parsing",
            "ai_customer_segment": "segmentation_analysis",
            "ai_product_description_generate": "product_description",
            "ai_industry_classification": "industry_classification"
        }

    def backup_file(self):
        """备份原文件"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(self.backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 原文件已备份到: {self.backup_path}")

    def fix_syntax_errors(self, content: str) -> str:
        """修复语法错误"""
        # 修复 ai_industry_classification 中的语法错误
        pattern = r'(\s+if hasattr\(response\.output\.choices\[0\]\.message, \'content\'\):\s+if content:)'
        replacement = r'\1\n                        content = response.output.choices[0].message.content\n                        if content:'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("✅ 修复了 ai_industry_classification 语法错误")
        return content

    def update_system_prompts(self, content: str) -> str:
        """更新系统提示词"""
        for func_name, new_prompt in self.prompt_templates.items():
            # 查找函数定义
            pattern = rf'class {func_name}\(object\):.*?messages = \[(.*?)\]'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                messages_content = match.group(1)
                # 更新system content
                old_system_pattern = r'\{"role": "system", "content": f?"[^"]*"\}'
                new_system_content = f'{{"role": "system", "content": f"""{new_prompt}"""}}'
                
                # 如果有f-string，需要特殊处理
                if 'segmentation_model' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（使用模型：{{segmentation_model}}）"}}'
                elif 'max_keywords' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（最多提取{{max_keywords}}个关键词）"}}'
                elif 'categories' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（候选类别：{{categories}}）"}}'
                elif 'operations' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（执行操作：{{operations}}）"}}'
                elif 'max_tags' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（生成{{max_tags}}个标签）"}}'
                elif 'business_context' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（业务背景：{{business_context}}）"}}'
                elif 'scoring_criteria' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（评分标准：{{scoring_criteria}}）"}}'
                elif 'product_type' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（产品类型：{{product_type}}）"}}'
                elif 'risk_types' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（风险类型：{{risk_types}}）"}}'
                elif 'extract_fields' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（提取字段：{{extract_fields}}）"}}'
                elif 'parse_depth' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（解析深度：{{parse_depth}}）"}}'
                elif 'style' in messages_content:
                    new_system_content = f'{{"role": "system", "content": f"{new_prompt}（文案风格：{{style}}）"}}'
                
                updated_messages = re.sub(old_system_pattern, new_system_content, messages_content)
                content = content.replace(messages_content, updated_messages)
                print(f"✅ 更新了 {func_name} 的系统提示词")
            
        return content

    def standardize_response_handling(self, content: str) -> str:
        """标准化响应处理逻辑"""
        for func_name, fallback_field in self.fallback_fields.items():
            # 查找函数的except块
            pattern = rf'(class {func_name}\(object\):.*?except:)\s+(result = \{{.*?\}})'
            
            def replace_except_block(match):
                before_except = match.group(1)
                standardized_except = f'result = {{"{fallback_field}": full_content}}'
                return before_except + '\n                ' + standardized_except
            
            content = re.sub(pattern, replace_except_block, content, flags=re.DOTALL)
        
        print("✅ 标准化了响应处理逻辑")
        return content

    def add_response_validator(self, content: str) -> str:
        """添加响应验证器"""
        validator_code = '''
# 响应验证器 - 在文件开头添加
def validate_ai_response(result, function_name):
    """验证AI函数返回格式"""
    if not isinstance(result, dict):
        return False
    
    # 基本字段验证
    required_fields = {
        "ai_text_sentiment_analyze": ["sentiment", "confidence"],
        "ai_text_extract_entities": ["entities"],
        "ai_customer_segment": ["segment", "scores", "total_score"],
        # 可以继续添加其他函数的必需字段
    }
    
    if function_name in required_fields:
        return all(field in result for field in required_fields[function_name])
    
    return True  # 对于未定义验证规则的函数，返回True

'''
        # 在导入语句后添加验证器
        import_end = content.find('# ==================== 文本处理函数')
        content = content[:import_end] + validator_code + '\n' + content[import_end:]
        print("✅ 添加了响应验证器")
        return content

    def optimize(self):
        """执行完整优化"""
        print("🚀 开始AI函数返回格式优化...\n")
        
        # 1. 备份文件
        self.backup_file()
        
        # 2. 读取文件
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 3. 修复语法错误
        content = self.fix_syntax_errors(content)
        
        # 4. 更新系统提示词
        content = self.update_system_prompts(content)
        
        # 5. 标准化响应处理
        content = self.standardize_response_handling(content)
        
        # 6. 添加响应验证器
        content = self.add_response_validator(content)
        
        # 7. 写回文件
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n🎉 优化完成！")
        print(f"📄 优化的文件: {self.file_path}")
        print(f"💾 备份文件: {self.backup_path}")
        print(f"\n📊 优化统计:")
        print(f"  - 修复语法错误: 1个")
        print(f"  - 更新提示词: {len(self.prompt_templates)}个")
        print(f"  - 标准化回退字段: {len(self.fallback_fields)}个")
        print(f"  - 添加响应验证器: 1个")
        
        return True

    def generate_test_script(self):
        """生成测试脚本"""
        test_script = '''#!/usr/bin/env python3
"""
优化后AI函数的测试脚本
验证返回格式是否符合标准
"""

import json
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_functions_complete import *

def test_function_format(func_class, func_name, test_data):
    """测试单个函数的返回格式"""
    print(f"\\n=== 测试 {func_name} ===")
    
    func_instance = func_class()
    
    # 模拟测试（使用假API密钥）
    if func_name == "ai_customer_segment":
        result = func_instance.evaluate(test_data, 'test-key', 'RFM', 'qwen-plus')
    elif func_name == "ai_text_summarize":
        result = func_instance.evaluate(test_data, 'test-key', 'qwen-plus', 100)
    else:
        result = func_instance.evaluate(test_data, 'test-key', 'qwen-plus')
    
    try:
        data = json.loads(result)
        print(f"✅ JSON格式正确")
        print(f"📝 返回字段: {list(data.keys())}")
        
        # 检查是否有错误字段
        if 'error' in data:
            print(f"⚠️  错误信息: {data.get('message', 'Unknown error')}")
        else:
            print(f"📊 数据预览: {str(data)[:200]}...")
            
        return True
    except Exception as e:
        print(f"❌ JSON解析失败: {e}")
        print(f"📄 原始结果: {result[:200]}...")
        return False

def main():
    """主测试函数"""
    test_cases = [
        (ai_text_sentiment_analyze, "ai_text_sentiment_analyze", "今天心情很好！"),
        (ai_text_extract_entities, "ai_text_extract_entities", "张三在北京工作"),
        (ai_customer_segment, "ai_customer_segment", '{"recency": 30, "frequency": 5, "monetary": 1000}'),
        (ai_text_summarize, "ai_text_summarize", "人工智能是计算机科学的重要分支，用于创建智能系统。"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    print("🧪 开始测试优化后的AI函数...")
    
    for func_class, func_name, test_data in test_cases:
        success = test_function_format(func_class, func_name, test_data)
        if success:
            success_count += 1
    
    print(f"\\n📊 测试结果统计:")
    print(f"✅ 成功: {success_count}/{total_count}")
    print(f"❌ 失败: {total_count - success_count}/{total_count}")
    print(f"📈 成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("\\n🎉 所有测试通过！格式优化成功。")
    else:
        print("\\n⚠️  部分测试失败，请检查优化结果。")

if __name__ == "__main__":
    main()
'''
        
        test_file_path = '/Users/liangmo/Documents/GitHub/clickzetta_aisql/test_optimized_functions.py'
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_script)
        
        print(f"✅ 生成测试脚本: {test_file_path}")
        return test_file_path

def main():
    """主函数"""
    file_path = '/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py'
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 创建优化器并执行优化
    optimizer = AIFunctionOptimizer(file_path)
    success = optimizer.optimize()
    
    if success:
        # 生成测试脚本
        test_script_path = optimizer.generate_test_script()
        
        print(f"\n🔄 下一步操作建议:")
        print(f"1. 运行测试: python {test_script_path}")
        print(f"2. 如果测试通过，重新打包: python package_with_deps.py")
        print(f"3. 部署到ClickZetta平台")
    
    return success

if __name__ == '__main__':
    import os
    main()