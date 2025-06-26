#!/usr/bin/env python3
"""
验证目录重组后的结构是否正确
"""

import os
import sys

def verify_directory_structure():
    """验证目录结构"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🔍 验证目录重组结果")
    print("="*60)
    
    # 定义期望的目录结构
    expected_structure = {
        "src": ["ai_functions_complete.py", "__init__.py"],
        "tests": ["test_complete_coverage.py", "quick_validation.py", "smart_analyzer.py"],
        "scripts": ["package_with_deps.py", "fix_industry_classification.py", "optimize_ai_functions.py"],
        "user_docs": ["01_QUICK_START.md", "02_USER_GUIDE.md", "07_FUNCTION_REFERENCE.md"],
        "data": ["test_config.json", "batch_test_data.json"],
        "dist": ["clickzetta_ai_functions_full.zip"],
        "archive": ["backups", "archive_dev_files", "dev_files"],
        "dev_docs": ["REORGANIZE_PLAN.md"]
    }
    
    # 检查根目录文件
    root_files = ["README.md", "requirements.txt", ".gitignore", "DIRECTORY_ORGANIZATION_SUMMARY.md"]
    
    all_good = True
    
    # 验证根目录文件
    print("📁 根目录文件:")
    for file in root_files:
        path = os.path.join(base_dir, file)
        if os.path.exists(path):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
            all_good = False
    
    # 验证子目录
    print("\n📂 目录结构:")
    for dir_name, expected_files in expected_structure.items():
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"\n✅ {dir_name}/")
            # 检查关键文件
            for file in expected_files[:3]:  # 只检查前3个关键文件
                file_path = os.path.join(dir_path, file)
                if os.path.exists(file_path):
                    print(f"  ✅ {file}")
                else:
                    # 文件可能在子目录中
                    found = False
                    for root, dirs, files in os.walk(dir_path):
                        if file in files:
                            print(f"  ✅ {file} (在子目录)")
                            found = True
                            break
                    if not found:
                        print(f"  ⚠️  {file} (未找到)")
            
            # 统计文件数量
            file_count = sum(len(files) for _, _, files in os.walk(dir_path))
            print(f"  📊 共 {file_count} 个文件")
        else:
            print(f"\n❌ {dir_name}/ (目录不存在)")
            all_good = False
    
    # 检查不应该在根目录的文件
    print("\n🧹 根目录清理检查:")
    unwanted_patterns = ["*.py.backup*", "*.bak", "test_*.py", "fix_*.py", "optimize_*.py"]
    root_files_actual = os.listdir(base_dir)
    unwanted_found = []
    
    for file in root_files_actual:
        if file.startswith('.') or file in ['__pycache__']:
            continue
        for pattern in unwanted_patterns:
            if pattern.startswith('*'):
                if file.endswith(pattern[1:]):
                    unwanted_found.append(file)
            elif pattern.endswith('*'):
                if file.startswith(pattern[:-1]):
                    unwanted_found.append(file)
    
    if unwanted_found:
        print("  ⚠️  发现应该归档的文件:")
        for file in unwanted_found[:5]:  # 只显示前5个
            print(f"    - {file}")
        if len(unwanted_found) > 5:
            print(f"    ... 还有 {len(unwanted_found) - 5} 个文件")
    else:
        print("  ✅ 根目录已清理干净")
    
    # 总结
    print("\n" + "="*60)
    if all_good and not unwanted_found:
        print("✅ 目录重组验证通过！")
        print("   所有文件都在正确的位置")
    else:
        print("⚠️  目录重组基本完成，但有一些小问题")
        print("   建议手动检查并调整")
    
    # 提供导入路径建议
    print("\n💡 导入路径提示:")
    print("   测试文件中导入源代码:")
    print("   sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))")
    print("   或")
    print("   from src.ai_functions_complete import *")


if __name__ == "__main__":
    verify_directory_structure()