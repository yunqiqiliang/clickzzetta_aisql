#!/usr/bin/env python
"""
云器Lakehouse AI Functions 完整打包脚本 (uv兼容版)
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
    project_dir = os.path.dirname(current_dir)
    temp_dir = os.path.join(current_dir, 'temp_package')
    output_file = os.path.join(project_dir, 'dist', 'clickzetta_ai_functions_full.zip')
    
    try:
        # 1. 创建临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # 2. 复制主文件
        src_file = os.path.join(project_dir, 'src', 'ai_functions_complete.py')
        shutil.copy(src_file, temp_dir)
        
        # 3. 检查是否在uv环境中
        is_uv = 'UV_PROJECT_ROOT' in os.environ or os.path.exists(os.path.join(project_dir, 'uv.lock'))
        
        if is_uv:
            print("📦 使用 uv 安装依赖包...")
            # 使用 uv pip 安装
            subprocess.run([
                'uv', 'pip', 'install',
                'dashscope>=1.23.4',
                '--target', temp_dir
            ], check=True)
        else:
            print("📦 使用 pip 安装依赖包...")
            # 尝试使用常规pip
            subprocess.run([
                sys.executable, '-m', 'pip', 'install',
                'dashscope>=1.23.4',
                '--target', temp_dir
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
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
                    print(f"✓ 添加: {arcname}")
        
        # 6. 清理临时目录
        shutil.rmtree(temp_dir)
        
        # 7. 显示结果
        file_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"\n✅ 打包完成!")
        print(f"📦 输出文件: {output_file}")
        print(f"📊 文件大小: {file_size:.1f} MB")
        print(f"📅 打包时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        if 'No module named pip' in str(e):
            print("\n💡 提示: 检测到pip模块缺失")
            print("请尝试以下方法之一:")
            print("1. 使用系统Python: python3 scripts/package_with_deps.py")
            print("2. 安装pip到uv环境: uv pip install pip")
            print("3. 直接使用预打包的文件: dist/clickzetta_ai_functions_full.zip")
        raise
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        raise

if __name__ == "__main__":
    print("🚀 云器Lakehouse AI Functions 完整打包工具")
    print("==================================================")
    create_full_package()