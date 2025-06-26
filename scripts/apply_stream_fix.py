#!/usr/bin/env python3
"""
应用流式修复到 ai_functions_complete.py
将流式响应处理改为非流式响应处理
"""

import re

# 读取文件
with open('ai_functions_complete.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份原内容
with open('ai_functions_complete.py.before_fix', 'w', encoding='utf-8') as f:
    f.write(content)

# 替换所有的 responses 为 response（针对非流式调用）
content = re.sub(r'responses = dashscope\.Generation\.call', 'response = dashscope.Generation.call', content)

# 替换流式处理循环
# 原始模式：
# for response in responses:
#     if response.status_code == HTTPStatus.OK:
#         if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
#             content = response.output.choices[0].message.content
#             if content: full_content += content

# 新模式（移除循环）：
# if response.status_code == HTTPStatus.OK:
#     if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
#         if hasattr(response.output.choices[0].message, 'content'):
#             full_content = response.output.choices[0].message.content or ""

lines = content.split('\n')
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # 检测 "for response in responses:" 模式
    if 'for response in responses:' in line:
        # 获取缩进
        indent = len(line) - len(line.lstrip())
        base_indent = ' ' * indent
        
        # 跳过 for 循环行
        i += 1
        
        # 处理循环体（移除一层缩进）
        while i < len(lines) and lines[i].strip() != '':
            next_line = lines[i]
            
            # 如果是循环体内的内容
            if next_line.startswith(base_indent + '    '):
                # 移除额外的4个空格缩进
                unindented_line = base_indent + next_line[len(base_indent) + 4:]
                
                # 特殊处理：将 += 改为 =
                if 'full_content += content' in unindented_line:
                    # 替换整个content获取和赋值逻辑
                    new_lines.append(base_indent + '        if hasattr(response.output.choices[0].message, \'content\'):')
                    new_lines.append(base_indent + '            full_content = response.output.choices[0].message.content or ""')
                    new_lines.append(base_indent + '        else:')
                    new_lines.append(base_indent + '            full_content = ""')
                    # 跳过原来的content赋值行
                    i += 1
                    continue
                elif 'content = response.output.choices[0].message.content' in unindented_line:
                    # 跳过这一行，因为我们已经在上面处理了
                    i += 1
                    continue
                else:
                    new_lines.append(unindented_line)
            else:
                # 不是循环体的内容，正常添加
                new_lines.append(next_line)
                # 如果遇到了非缩进行，说明循环体结束
                if not next_line.startswith(base_indent):
                    break
            
            i += 1
        continue
    
    new_lines.append(line)
    i += 1

# 重新组合内容
content = '\n'.join(new_lines)

# 写回文件
with open('ai_functions_complete.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("修复完成！")
print("原文件已备份到: ai_functions_complete.py.before_fix")
print("请测试修改后的功能是否正常。")