#!/usr/bin/env python
"""
检查clickzetta_aisql包中所有Python文件的语法
"""

import os
import py_compile
import ast

def check_python_syntax():
    """检查所有Python文件的语法"""
    print("=== 检查Python语法 ===\n")
    
    # 需要检查的目录和文件
    paths_to_check = [
        'clickzetta_aisql',
        'bailian_llm.py'
    ]
    
    error_count = 0
    file_count = 0
    
    for path in paths_to_check:
        if os.path.isfile(path) and path.endswith('.py'):
            # 单个文件
            file_count += 1
            print(f"检查文件: {path}")
            if check_file(path):
                print(f"  ✓ 语法正确")
            else:
                error_count += 1
                
        elif os.path.isdir(path):
            # 目录
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        file_count += 1
                        print(f"检查文件: {file_path}")
                        if check_file(file_path):
                            print(f"  ✓ 语法正确")
                        else:
                            error_count += 1
    
    print(f"\n=== 检查完成 ===")
    print(f"总文件数: {file_count}")
    print(f"语法错误: {error_count}")
    
    if error_count == 0:
        print("\n✅ 所有文件语法检查通过！")
        return True
    else:
        print(f"\n❌ 发现 {error_count} 个语法错误，请修复后再打包。")
        return False

def check_file(file_path):
    """检查单个文件的语法"""
    try:
        # 编译检查
        py_compile.compile(file_path, doraise=True)
        
        # AST解析检查
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        
        return True
        
    except SyntaxError as e:
        print(f"  ❌ 语法错误: 第 {e.lineno} 行")
        print(f"     {e.msg}")
        if e.text:
            print(f"     {e.text.strip()}")
            print(f"     {' ' * (e.offset - 1)}^")
        return False
        
    except Exception as e:
        print(f"  ❌ 其他错误: {str(e)}")
        return False

def check_specific_issues():
    """检查特定的常见问题"""
    print("\n=== 检查特定问题 ===")
    
    # 检查text_functions.py中的问题
    text_functions_path = "clickzetta_aisql/text_functions.py"
    if os.path.exists(text_functions_path):
        with open(text_functions_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 检查第308行附近
        for i in range(max(0, 307-5), min(len(lines), 307+5)):
            line = lines[i].rstrip()
            if 'text_' in line and (line.count('"') % 2 != 0 or line.count("'") % 2 != 0):
                print(f"  ⚠️  第 {i+1} 行可能有未闭合的引号: {line}")
    
    # 检查所有文件中的常见语法问题
    issues = []
    for root, dirs, files in os.walk('clickzetta_aisql'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                        lines = content.split('\n')
                        
                        for i, line in enumerate(lines):
                            # 检查未闭合的引号
                            if line.count('"""') % 2 != 0:
                                issues.append(f"{file_path}:{i+1} - 可能有未闭合的三引号")
                            elif line.strip() and not line.strip().startswith('#'):
                                # 排除注释行
                                single_quotes = line.count("'") - line.count("\\'")
                                double_quotes = line.count('"') - line.count('\\"')
                                if single_quotes % 2 != 0:
                                    issues.append(f"{file_path}:{i+1} - 可能有未闭合的单引号")
                                if double_quotes % 2 != 0:
                                    issues.append(f"{file_path}:{i+1} - 可能有未闭合的双引号")
                    except:
                        pass
    
    if issues:
        print("\n发现潜在问题:")
        for issue in issues[:10]:  # 只显示前10个
            print(f"  ⚠️  {issue}")
    else:
        print("  ✓ 未发现明显的语法问题")

if __name__ == "__main__":
    # 运行语法检查
    syntax_ok = check_python_syntax()
    
    # 运行特定问题检查
    check_specific_issues()
    
    # 返回状态
    exit(0 if syntax_ok else 1)