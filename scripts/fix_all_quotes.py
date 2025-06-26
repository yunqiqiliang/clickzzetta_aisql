#!/usr/bin/env python3
"""
批量修复所有引号和JSON格式问题
"""

import re

# 读取文件
with open('/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open('/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py.backup_final', 'w', encoding='utf-8') as f:
    f.write(content)

# 修复JSON格式中的花括号转义问题
# 找到所有包含JSON示例的系统提示词，将其中的 { 和 } 转义为 {{ 和 }}
def fix_json_in_prompt(match):
    content_part = match.group(1)
    # 在JSON示例中转义花括号
    if '{"' in content_part and '"}' in content_part:
        # 查找JSON模式并转义
        json_pattern = r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})'
        def escape_json(json_match):
            json_str = json_match.group(1)
            # 将单个花括号转义为双花括号
            escaped = json_str.replace('{', '{{').replace('}', '}}')
            return escaped
        content_part = re.sub(json_pattern, escape_json, content_part)
    return f'f"""{content_part}"""'

# 应用修复
content = re.sub(r'f"""([^"]*\{[^"]*\}[^"]*)"""', fix_json_in_prompt, content, flags=re.DOTALL)

# 修复其他格式问题
content = re.sub(r'{"([^"]*"}[^"]*)}([^"]*)"""', r'{{\1}}\2"""', content)

# 写回文件
with open('/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("所有引号和JSON格式问题修复完成！")
print("备份文件: ai_functions_complete.py.backup_final")