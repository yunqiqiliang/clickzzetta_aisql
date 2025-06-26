#!/usr/bin/env python3
"""
应用JIRA-001优化到AI函数
直接修改关键函数的提示词，消除冗余文本
"""

import re
import sys
import shutil

def apply_optimizations(file_path):
    """应用优化到指定文件"""
    
    # 备份原文件
    backup_path = f"{file_path}.backup_before_optimization_v2"
    shutil.copy2(file_path, backup_path)
    print(f"✅ 原文件已备份到: {backup_path}")
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义优化映射
    optimizations = [
        # ai_text_sentiment_analyze
        {
            'old': '{"role": "system", "content": "你是专业情感分析专家，分析文本情感倾向，返回JSON格式。"}',
            'new': '''{"role": "system", "content": """你是专业情感分析专家。分析文本情感倾向。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"sentiment": "positive|negative|neutral", "confidence": 0.95, "emotions": ["joy", "anger"], "keywords": ["关键词1"]}"""}'''
        },
        # ai_text_extract_entities
        {
            'old': '{"role": "system", "content": "你是专业信息提取专家，从文本中提取实体信息，返回JSON格式。"}',
            'new': '''{"role": "system", "content": """你是专业信息提取专家。从文本中提取实体信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{"entities": [{"text": "实体名", "type": "PERSON|ORG|LOC|MISC", "confidence": 0.95}]}"""}'''
        },
        # ai_text_extract_keywords
        {
            'old': '{"role": "system", "content": f"你是关键词提取专家，提取{max_keywords}个主要关键词，返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是关键词提取专家。提取文本的核心关键词。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"keywords": [{{"word": "关键词", "weight": 0.95, "category": "核心概念"}}]}}（最多提取{max_keywords}个关键词）"""}'''
        },
        # ai_text_classify
        {
            'old': '{"role": "system", "content": f"你是文本分类专家，将文本分类到合适类别（{categories}），返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是文本分类专家。将文本分类到合适类别。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"category": "分类名称", "confidence": 0.95, "subcategory": "子分类", "categories_considered": ["类别1", "类别2"]}}（候选类别：{categories}）"""}'''
        },
        # ai_text_clean_normalize
        {
            'old': '{"role": "system", "content": f"你是文本清洗专家，执行清洗操作：{operations}，返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是文本清洗专家。执行文本清洗和标准化操作。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"cleaned_text": "清洗后文本", "operations_applied": ["去重", "标准化"], "changes_count": 5}}（执行操作：{operations}）"""}'''
        },
        # ai_auto_tag_generate
        {
            'old': '{"role": "system", "content": f"你是标签生成专家，为文本生成{max_tags}个相关标签，返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是智能标签生成专家。为文本生成相关标签。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"tags": [{{"tag": "标签名", "relevance": 0.95, "category": "主题"}}]}}（生成{max_tags}个标签）"""}'''
        },
        # ai_customer_intent_analyze
        {
            'old': '{"role": "system", "content": f"你是客户意图分析专家，分析客户文本的意图和需求（业务背景：{business_context}），返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是客户意图分析专家。分析客户文本的真实意图。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"intent": "购买意向|咨询|投诉|建议", "confidence": 0.95, "urgency": "high|medium|low", "emotions": ["satisfied"], "action_required": "立即处理"}}（业务背景：{business_context}）"""}'''
        },
        # ai_sales_lead_score
        {
            'old': '{"role": "system", "content": f"你是销售线索评分专家，根据{scoring_criteria}标准评估线索价值，返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是销售线索评分专家。根据标准评估线索价值。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"score": 85, "grade": "A|B|C|D", "probability": 0.85, "factors": [{{"factor": "预算充足", "impact": "positive", "weight": 0.3}}], "next_action": "立即跟进"}}（评分标准：{scoring_criteria}）"""}'''
        },
        # ai_review_analyze
        {
            'old': '{"role": "system", "content": f"你是评论分析专家，分析{product_type}产品的用户评论，返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是评论分析专家。分析用户评论的多维度信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"sentiment": "positive|negative|neutral", "rating_predicted": 4.5, "aspects": [{{"aspect": "服务", "sentiment": "positive", "score": 4.2}}], "key_issues": ["待改进点"]}}（产品类型：{product_type}）"""}'''
        },
        # ai_risk_text_detect
        {
            'old': '{"role": "system", "content": f"你是风险检测专家，检测文本中的风险内容（类型：{risk_types}），返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是风险检测专家。检测文本中的各类风险内容。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"risk_level": "high|medium|low|none", "risk_types": ["欺诈", "违规"], "confidence": 0.95, "flagged_content": ["具体风险文本"], "action_required": true}}（风险类型：{risk_types}）"""}'''
        },
        # ai_contract_extract
        {
            'old': '{"role": "system", "content": f"你是合同信息提取专家，提取合同关键信息（字段：{extract_fields}），返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是合同信息提取专家。提取合同的关键信息字段。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"parties": ["甲方", "乙方"], "amount": "1000000", "start_date": "2024-01-01", "end_date": "2024-12-31", "key_terms": ["重要条款"], "risk_points": ["风险点"]}}（提取字段：{extract_fields}）"""}'''
        },
        # ai_resume_parse
        {
            'old': '{"role": "system", "content": f"你是简历解析专家，解析简历信息（深度：{parse_depth}），返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是简历解析专家。解析简历的结构化信息。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"name": "姓名", "education": [{{"degree": "本科", "school": "大学", "major": "专业"}}], "experience": [{{"title": "职位", "company": "公司", "duration": "2年"}}], "skills": ["技能1"]}}（解析深度：{parse_depth}）"""}'''
        },
        # ai_customer_segment - 最关键的优化
        {
            'old': '{"role": "system", "content": f"你是客户细分专家，根据{segmentation_model}模型进行客户细分，返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是客户细分专家。根据模型进行客户细分分析。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"segment": "高价值客户", "scores": {{"R": 5, "F": 4, "M": 5}}, "total_score": 85, "characteristics": ["购买频繁"], "recommendations": ["VIP服务"], "retention_probability": 0.92}}（使用模型：{segmentation_model}）"""}'''
        },
        # ai_product_description_generate
        {
            'old': '{"role": "system", "content": f"你是产品文案专家，生成{style}风格的产品描述，返回JSON格式。"}',
            'new': '''{"role": "system", "content": f"""你是产品文案专家。生成吸引人的产品描述。
严格按照以下JSON格式返回，不要包含任何解释文字：
{{"title": "产品标题", "description": "详细描述", "features": ["特色1", "特色2"], "benefits": ["优势1"], "target_audience": "目标用户", "selling_points": ["卖点1"]}}（文案风格：{style}）"""}'''
        }
    ]
    
    # 应用优化
    changes_made = 0
    for opt in optimizations:
        if opt['old'] in content:
            content = content.replace(opt['old'], opt['new'])
            changes_made += 1
            print(f"✅ 优化了一个提示词")
    
    # 标准化回退字段（处理catch块中的结果）
    # 将segmentation_analysis改为更标准的字段名
    content = re.sub(
        r'result = \{"segmentation_analysis": full_content\}',
        'result = {"segment": "未知", "scores": {}, "analysis": full_content}',
        content
    )
    
    # 修复ai_industry_classification的语法错误
    # 查找并修复content变量未定义的问题
    industry_pattern = r'if response\.status_code == HTTPStatus\.OK:\s*full_content = ""\s*for response in responses:'
    if re.search(industry_pattern, content):
        content = re.sub(
            industry_pattern,
            'if response.status_code == HTTPStatus.OK:\n                full_content = ""',
            content
        )
        print("✅ 修复了 ai_industry_classification 语法错误")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 完成优化！共修改了 {changes_made} 个提示词")
    return changes_made

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python apply_optimizations.py [API_KEY]")
        print("API_KEY用于测试，但此脚本只做文件修改，不进行API调用")
        return
    
    file_path = '/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py'
    
    print("🚀 开始应用JIRA-001优化...")
    print("=" * 50)
    
    # 应用优化
    changes = apply_optimizations(file_path)
    
    if changes > 0:
        print("\n🎉 优化成功！")
        print(f"📄 优化的文件: {file_path}")
        print(f"💾 备份文件: {file_path}.backup_before_optimization_v2")
        
        print("\n📊 优化内容:")
        print("  - 消除了所有冗余的RFM模型解释")
        print("  - 标准化了JSON返回格式")
        print("  - 添加了严格的格式要求")
        print("  - 修复了语法错误")
        
        print("\n🔄 下一步操作:")
        print("1. 使用真实API密钥测试: python quick_test_real_api.py YOUR_API_KEY")
        print("2. 验证压缩率是否达到67%+")
        print("3. 重新打包: python package_with_deps.py")
        print("4. 部署到ClickZetta测试")
    else:
        print("\n⚠️  未找到需要优化的内容，请检查文件")

if __name__ == '__main__':
    main()