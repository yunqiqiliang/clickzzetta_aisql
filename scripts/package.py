#!/usr/bin/env python
"""
云器Lakehouse AI Functions 打包脚本
生成用于部署的 clickzetta_ai_functions_complete.zip
"""

import os
import zipfile
from datetime import datetime

def create_deployment_package():
    """创建部署包"""
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 输出文件名
    output_file = os.path.join(current_dir, 'clickzetta_ai_functions_complete.zip')
    
    # 需要打包的文件
    files_to_package = [
        'ai_functions_complete.py'
    ]
    
    # 创建ZIP文件
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_name in files_to_package:
            file_path = os.path.join(current_dir, file_name)
            if os.path.exists(file_path):
                # 添加文件到ZIP，不包含目录结构
                zipf.write(file_path, file_name)
                print(f"✓ 添加: {file_name}")
            else:
                print(f"✗ 文件不存在: {file_name}")
    
    # 获取文件大小
    size_kb = os.path.getsize(output_file) / 1024
    
    print(f"\n✅ 打包完成!")
    print(f"📦 输出文件: {output_file}")
    print(f"📊 文件大小: {size_kb:.1f} KB")
    print(f"📅 打包时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return output_file

if __name__ == "__main__":
    print("🚀 云器Lakehouse AI Functions 打包工具")
    print("=" * 50)
    create_deployment_package()