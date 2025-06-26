#!/usr/bin/env python3
"""
修复 ai_functions_complete.py 中的流式响应问题
将 stream=True 改为 stream=False
"""

import re
import shutil
from datetime import datetime

def fix_stream_in_file(file_path):
    """修复文件中的流式调用"""
    
    # 备份原文件
    backup_path = f"{file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"已备份到: {backup_path}")
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计修改前的stream=True数量
    stream_true_count = len(re.findall(r'stream\s*=\s*True', content))
    print(f"找到 {stream_true_count} 处 stream=True")
    
    # 1. 将所有 stream=True 改为 stream=False
    content = re.sub(
        r'stream\s*=\s*True',
        'stream=False',
        content
    )
    
    # 2. 修改流式响应处理代码
    # 原始模式：
    # responses = dashscope.Generation.call(...)
    # full_content = ""
    # for response in responses:
    #     ...
    
    # 新模式：
    # response = dashscope.Generation.call(...)
    # if response.status_code == HTTPStatus.OK:
    #     ...
    
    # 定义替换模式
    pattern = r'''(responses = dashscope\.Generation\.call\([^)]+\))
(\s+full_content = "")
(\s+for response in responses:)
(\s+if response\.status_code == HTTPStatus\.OK:)
(\s+if hasattr\(response\.output, 'choices'\) and len\(response\.output\.choices\) > 0:)
(\s+)content = response\.output\.choices\[0\]\.message\.content
(\s+)if content: full_content \+= content'''
    
    replacement = r'''response = dashscope.Generation.call\1
\2if response.status_code == HTTPStatus.OK:
\3    if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
\4        if hasattr(response.output.choices[0].message, 'content'):
\5            full_content = response.output.choices[0].message.content or ""
\6        else:
\7            full_content = ""'''
    
    # 执行替换
    # 由于模式复杂，我们采用更简单的方法：直接替换关键部分
    
    # 将 responses 改为 response
    content = re.sub(
        r'responses = dashscope\.Generation\.call',
        'response = dashscope.Generation.call',
        content
    )
    
    # 将 for response in responses: 改为单次处理
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检测流式处理模式
        if 'for response in responses:' in line:
            # 找到了流式处理循环
            indent = line[:len(line) - len(line.lstrip())]
            
            # 跳过for循环行
            i += 1
            
            # 处理循环体
            while i < len(lines) and lines[i].startswith(indent + '    '):
                inner_line = lines[i]
                
                # 移除一层缩进
                if inner_line.startswith(indent + '    '):
                    new_line = inner_line[4:]  # 移除4个空格
                    new_lines.append(new_line)
                
                i += 1
                
                # 特殊处理：将 += 改为 =
                if 'full_content += content' in new_lines[-1]:
                    new_lines[-1] = new_lines[-1].replace('full_content += content', 'full_content = content')
            
            # 添加获取content的完整逻辑
            if new_lines and 'if response.status_code == HTTPStatus.OK:' in new_lines[-5]:
                # 在合适的位置插入完整的content获取逻辑
                insert_pos = len(new_lines) - 2
                new_lines.insert(insert_pos, indent + '            if hasattr(response.output.choices[0].message, \'content\'):')
                new_lines.insert(insert_pos + 1, indent + '                full_content = response.output.choices[0].message.content or ""')
                new_lines.insert(insert_pos + 2, indent + '            else:')
                new_lines.insert(insert_pos + 3, indent + '                full_content = ""')
                # 移除原来的简单赋值
                new_lines = [line for line in new_lines if 'content = response.output.choices[0].message.content' not in line and 'if content: full_content' not in line]
            
            continue
        
        new_lines.append(line)
        i += 1
    
    content = '\n'.join(new_lines)
    
    # 3. 添加输出长度保护（可选）
    # 在每个返回result之前添加检查
    content = re.sub(
        r'(result = \{[^}]+\})\n(\s+return json\.dumps\(result)',
        r'''\1
\2        # 输出保护：确保不会过长
\2        if "summary" in result and len(result["summary"]) > len(text) * 2:
\2            result["summary"] = result["summary"][:max_length]
\2return json.dumps(result''',
        content
    )
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 统计修改后的stream=False数量
    stream_false_count = len(re.findall(r'stream\s*=\s*False', content))
    print(f"修改后有 {stream_false_count} 处 stream=False")
    
    print(f"\n修改完成！")
    print(f"原文件已备份到: {backup_path}")
    print(f"请检查修改后的文件: {file_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "/Users/liangmo/Documents/GitHub/clickzetta_aisql/ai_functions_complete.py"
    
    print(f"正在修复文件: {file_path}")
    fix_stream_in_file(file_path)