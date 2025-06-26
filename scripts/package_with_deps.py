#!/usr/bin/env python
"""
云器Lakehouse AI Functions 完整打包脚本
包含所有依赖，生成自包含的部署包
"""

import os
import sys
import zipfile
import shutil
import subprocess
from datetime import datetime

def create_full_package():
    """创建包含依赖的完整部署包"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(current_dir, 'temp_package')
    output_file = os.path.join(os.path.dirname(current_dir), 'dist', 'clickzetta_ai_functions_full.zip')
    
    try:
        # 1. 创建临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # 2. 复制主文件
        src_file = os.path.join(os.path.dirname(current_dir), 'src', 'ai_functions_complete.py')
        shutil.copy(src_file, temp_dir)
        
        # 3. 安装依赖到临时目录
        print("📦 安装依赖包...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            'dashscope>=1.23.4',
            '--target', temp_dir
            # 移除 --no-deps，安装所有必要的传递依赖
        ], check=True)
        
        # 4. 清理不必要的文件
        for root, dirs, files in os.walk(temp_dir):
            # 删除 __pycache__
            if '__pycache__' in dirs:
                shutil.rmtree(os.path.join(root, '__pycache__'))
            # 删除 .dist-info 目录（可选，保留可能更好）
            for d in dirs[:]:
                if d.endswith('.dist-info'):
                    shutil.rmtree(os.path.join(root, d))
                    dirs.remove(d)
        
        # 5. 创建ZIP文件
        print("\n📦 创建ZIP包...")
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if not file.endswith('.pyc'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
                        print(f"✓ 添加: {arcname}")
        
        # 6. 获取文件大小
        size_mb = os.path.getsize(output_file) / 1024 / 1024
        
        print(f"\n✅ 打包完成!")
        print(f"📦 输出文件: {output_file}")
        print(f"📊 文件大小: {size_mb:.1f} MB")
        print(f"📅 打包时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 7. 清理临时目录
        shutil.rmtree(temp_dir)
        
        return output_file
        
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise

def create_minimal_package():
    """创建最小包（不含依赖）"""
    os.system('python package.py')

if __name__ == "__main__":
    print("🚀 云器Lakehouse AI Functions 完整打包工具")
    print("=" * 50)
    
    # 直接创建完整包
    create_full_package()