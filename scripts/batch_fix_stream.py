#!/usr/bin/env python3
"""
批量修复所有流式调用代码
"""

import re

# 文件路径
import os
base_dir = '/Users/liangmo/Documents/GitHub/clickzetta_aisql'
source_file = os.path.join(base_dir, 'ai_functions_complete.py')
backup_file = os.path.join(base_dir, 'ai_functions_complete.py.backup_stream_fix')

# 读取文件
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(content)

# 1. 将所有 responses 变量名改为 response
content = re.sub(r'\bresponses = dashscope\.Generation\.call', 'response = dashscope.Generation.call', content)

# 2. 处理流式循环
lines = content.split('\n')
new_lines = []
i = 0

def process_stream_loop(lines, start_idx):
    """处理一个流式循环块"""
    result_lines = []
    i = start_idx
    
    # 获取缩进级别
    indent_line = lines[i]
    indent = len(indent_line) - len(indent_line.lstrip())
    base_indent = ' ' * indent
    
    # 跳过 for 行
    i += 1
    
    # 处理循环体
    while i < len(lines):
        line = lines[i]
        
        # 如果到达非缩进行，循环结束
        if line.strip() and not line.startswith(base_indent + '    '):
            break
        
        # 移除一层缩进（4个空格）
        if line.startswith(base_indent + '    '):
            new_line = base_indent + line[len(base_indent) + 4:]
            
            # 特殊处理内容获取逻辑
            if 'content = response.output.choices[0].message.content' in line:
                # 跳过这行
                i += 1
                continue
            elif 'if content: full_content += content' in line:
                # 替换为正确的内容获取逻辑
                result_lines.append(base_indent + '        if hasattr(response.output.choices[0].message, \'content\'):')
                result_lines.append(base_indent + '            full_content = response.output.choices[0].message.content or ""')
                result_lines.append(base_indent + '        else:')
                result_lines.append(base_indent + '            full_content = ""')
                i += 1
                continue
            else:
                result_lines.append(new_line)
        else:
            # 空行或其他，保持原样
            result_lines.append(line)
        
        i += 1
    
    return result_lines, i

# 处理文件
i = 0
while i < len(lines):
    line = lines[i]
    
    if 'for response in responses:' in line:
        # 找到流式循环，处理它
        processed_lines, next_i = process_stream_loop(lines, i)
        new_lines.extend(processed_lines)
        i = next_i
    else:
        new_lines.append(line)
        i += 1

# 重新组合
content = '\n'.join(new_lines)

# 3. 额外的清理：确保没有遗漏的 responses
content = re.sub(r'\bresponses\b', 'response', content)

# 写回文件
with open(source_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("批量修复完成！")
print("备份文件：ai_functions_complete.py.backup_stream_fix")
print("\n建议步骤：")
print("1. 检查修改是否正确：diff ai_functions_complete.py.backup_stream_fix ai_functions_complete.py")
print("2. 测试函数功能")
print("3. 重新打包：python package_with_deps.py")
print("4. 部署到ClickZetta")