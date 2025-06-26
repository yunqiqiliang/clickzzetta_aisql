#!/usr/bin/env python
"""
最终语法修复脚本 - 精确修复所有语法错误
"""

import re
import os

def fix_file_syntax(file_path):
    """修复单个文件的语法错误"""
    print(f"\n修复文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修复重复的return语句
    content = re.sub(r'return self\.format_success_respreturn self\.format_successreturn self\.format_success_response\(', 
                     'return self.format_success_response(', content)
    
    # 2. 修复断开的return语句
    content = re.sub(r'return self\.format_success_resp\s*\n\s*return self\.format_success_response\(result\)', 
                     'return self.format_success_response(result)', content)
    
    # 3. 修复其他重复的return
    content = re.sub(r'return self\.format_successreturn self\.format_success_response\(', 
                     'return self.format_success_response(', content)
    
    # 4. 修复断开的_error_response
    content = re.sub(r'return self\.format\s*\n\s*_error_response\(str\(e\)\)', 
                     'return self.format_error_response(str(e))', content)
    
    # 5. 修复断开的ror_response
    content = re.sub(r'return self\.format_er\s*\n\s*ror_response\(str\(e\)\)', 
                     'return self.format_error_response(str(e))', content)
    
    # 6. 修复重复的return self.format_success
    content = re.sub(r'return self\.format_success\s*\n\s*return self\.format_success_response\(result\)', 
                     'return self.format_success_response(result)', content)
    
    # 7. 修复断开的t_error_response
    content = re.sub(r'return self\.forma\s*\n\s*t_error_response\(str\(e\)\)', 
                     'return self.format_error_response(str(e))', content)
    
    # 8. 修复return语句后的else
    content = re.sub(r'return self\.format_success_response\(result\)else:', 
                     'return self.format_success_response(result)\n            else:', content)
    
    # 9. 修复特定的语法错误 - multimodal_functions.py
    if 'multimodal_functions.py' in file_path:
        # 修复第333行附近的错误
        content = re.sub(r'"length_requirement": length_configs\[length\],\s*\n\s*gth,', 
                         '"length_requirement": length_configs[length],', content)
        
        # 修复缩进问题
        content = re.sub(r'(\s+)"model": model_name,\s*\n\s*"confidence":', 
                         r'\1"model": model_name,\n\1"confidence":', content)
    
    # 10. 修复customer_data断行
    if 'business_functions.py' in file_path:
        content = re.sub(r'"customer_data": customer\s*\n\s*_data,', 
                         '"customer_data": customer_data,', content)
        
        content = re.sub(r'"analysis_timestamp":\s*\n\s*self\._get_timestamp\(\),', 
                         '"analysis_timestamp": self._get_timestamp(),', content)
    
    # 11. 清理多余的空格和换行
    content = re.sub(r'}\)\s*\n\s*\n\s*return', '})\n            \n            return', content)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ 完成修复")

def verify_syntax(file_path):
    """验证文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        compile(content, file_path, 'exec')
        return True, None
    except SyntaxError as e:
        return False, f"第 {e.lineno} 行: {e.msg}"
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    print("=== 最终语法修复 ===")
    
    # 需要修复的文件
    files_to_fix = [
        'clickzetta_aisql/vector_functions.py',
        'clickzetta_aisql/text_functions.py',
        'clickzetta_aisql/multimodal_functions.py',
        'clickzetta_aisql/business_functions.py'
    ]
    
    # 修复每个文件
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            fix_file_syntax(file_path)
    
    # 验证结果
    print("\n=== 验证语法 ===")
    all_valid = True
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            valid, error = verify_syntax(file_path)
            if valid:
                print(f"✓ {file_path} - 语法正确")
            else:
                print(f"✗ {file_path} - {error}")
                all_valid = False
    
    if all_valid:
        print("\n✅ 所有文件语法修复成功！")
    else:
        print("\n❌ 仍有语法错误需要手动修复")

if __name__ == "__main__":
    main()