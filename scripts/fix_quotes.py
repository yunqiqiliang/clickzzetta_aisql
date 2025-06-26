#!/usr/bin/env python3
"""
修复AI函数中的引号问题
"""

import re

# 读取文件
with open('/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open('/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py.backup_quotes', 'w', encoding='utf-8') as f:
    f.write(content)

# 修复引号问题 - 将 f"" 改为 f"""
patterns = [
    (r'{"role": "system", "content": f""([^"]*)""}', r'{"role": "system", "content": f"""\1"""}'),
]

for pattern, replacement in patterns:
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 特殊处理多行字符串的引号
content = content.replace('f""你是专业情感分析专家', 'f"""你是专业情感分析专家')
content = content.replace('keywords": ["关键词1"]}"}', 'keywords": ["关键词1"]}"""')

content = content.replace('f""你是专业信息提取专家', 'f"""你是专业信息提取专家')
content = content.replace('confidence": 0.95}]}"}', 'confidence": 0.95}]}"""')

content = content.replace('f"你是关键词提取专家', 'f"""你是关键词提取专家')
content = content.replace('category": "核心概念"}]}（最多提取{max_keywords}个关键词）"}', 'category": "核心概念"}]}（最多提取{max_keywords}个关键词）"""')

content = content.replace('f"你是文本分类专家', 'f"""你是文本分类专家')
content = content.replace('categories_considered": ["类别1", "类别2"]}（候选类别：{categories}）"}', 'categories_considered": ["类别1", "类别2"]}（候选类别：{categories}）"""')

content = content.replace('f"你是文本清洗专家', 'f"""你是文本清洗专家')
content = content.replace('changes_count": 5}（执行操作：{operations}）"}', 'changes_count": 5}（执行操作：{operations}）"""')

content = content.replace('f"你是智能标签生成专家', 'f"""你是智能标签生成专家')
content = content.replace('category": "主题"}]}（生成{max_tags}个标签）"}', 'category": "主题"}]}（生成{max_tags}个标签）"""')

content = content.replace('f"你是客户意图分析专家', 'f"""你是客户意图分析专家')
content = content.replace('action_required": "立即处理"}（业务背景：{business_context}）"}', 'action_required": "立即处理"}（业务背景：{business_context}）"""')

content = content.replace('f"你是销售线索评分专家', 'f"""你是销售线索评分专家')
content = content.replace('next_action": "立即跟进"}（评分标准：{scoring_criteria}）"}', 'next_action": "立即跟进"}（评分标准：{scoring_criteria}）"""')

content = content.replace('f"你是评论分析专家', 'f"""你是评论分析专家')
content = content.replace('key_issues": ["待改进点"]}（产品类型：{product_type}）"}', 'key_issues": ["待改进点"]}（产品类型：{product_type}）"""')

content = content.replace('f"你是风险检测专家', 'f"""你是风险检测专家')
content = content.replace('action_required": true}（风险类型：{risk_types}）"}', 'action_required": true}（风险类型：{risk_types}）"""')

content = content.replace('f"你是合同信息提取专家', 'f"""你是合同信息提取专家')
content = content.replace('risk_points": ["风险点"]}（提取字段：{extract_fields}）"}', 'risk_points": ["风险点"]}（提取字段：{extract_fields}）"""')

content = content.replace('f"你是简历解析专家', 'f"""你是简历解析专家')
content = content.replace('skills": ["技能1"]}（解析深度：{parse_depth}）"}', 'skills": ["技能1"]}（解析深度：{parse_depth}）"""')

content = content.replace('f"你是客户细分专家', 'f"""你是客户细分专家')
content = content.replace('retention_probability": 0.92}（使用模型：{segmentation_model}）"}', 'retention_probability": 0.92}（使用模型：{segmentation_model}）"""')

content = content.replace('f"你是产品文案专家', 'f"""你是产品文案专家')
content = content.replace('selling_points": ["卖点1"]}（文案风格：{style}）"}', 'selling_points": ["卖点1"]}（文案风格：{style}）"""')

# 写回文件
with open('/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("引号修复完成！")
print("备份文件: ai_functions_complete.py.backup_quotes")