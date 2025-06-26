#!/usr/bin/env python3
"""
一键打包并复制到Downloads目录
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime

def main(force_rebuild=False):
    """主函数"""
    print("🚀 ClickZetta AI Functions 打包和复制工具")
    print("="*60)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] in ['--rebuild', '-r', '--force']:
        force_rebuild = True
        print("🔄 强制重新打包模式")
    
    # 1. 检查是否在uv环境中
    is_uv = 'UV_PROJECT_ROOT' in os.environ or os.path.exists(os.path.join(current_dir, '.venv'))
    
    source_file = os.path.join(current_dir, 'dist', 'clickzetta_ai_functions_full.zip')
    
    if is_uv and os.path.exists(source_file) and not force_rebuild:
        # 在uv环境中，如果已有打包文件且不强制重建，直接使用
        print("\n📦 步骤1: 使用已存在的打包文件...")
        print(f"✅ 找到打包文件: {source_file}")
        
        # 显示文件信息
        file_size = os.path.getsize(source_file) / (1024 * 1024)
        file_time = os.path.getmtime(source_file)
        package_time = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"   📊 文件大小: {file_size:.1f} MB")
        print(f"   📅 打包时间: {package_time}")
        print("\n💡 提示: 使用 --rebuild 参数强制重新打包")
    else:
        # 运行打包脚本
        print("\n📦 步骤1: 运行打包脚本...")
        package_script = os.path.join(current_dir, 'scripts', 'package_with_deps.py')
        
        # 如果在uv环境中且需要重新打包，使用系统python3
        if is_uv and force_rebuild:
            print("🔧 在uv环境中使用系统Python3进行打包...")
            python_cmd = 'python3'  # 使用系统python3
        else:
            python_cmd = sys.executable
        
        try:
            result = subprocess.run([python_cmd, package_script], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            print("✅ 打包成功！")
            
            # 显示打包脚本的最后几行输出
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines[-5:]:
                if line.strip():
                    print(f"   {line}")
        except subprocess.CalledProcessError as e:
            print(f"❌ 打包失败: {e}")
            print(f"错误输出: {e.stderr}")
            if 'No module named pip' in str(e.stderr):
                print("\n💡 提示: 在uv环境中检测到pip缺失")
                print("建议使用: python3 copy_to_downloads.py")
            return 1
    
    # 2. 复制到Downloads目录
    print("\n📂 步骤2: 复制到Downloads目录...")
    
    # 获取用户的Downloads目录
    downloads_dir = os.path.expanduser('~/Downloads')
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dest_filename = f'clickzetta_ai_functions_full_{timestamp}.zip'
    dest_file = os.path.join(downloads_dir, dest_filename)
    
    # 同时保留一个不带时间戳的副本
    latest_file = os.path.join(downloads_dir, 'clickzetta_ai_functions_full_latest.zip')
    
    try:
        # 复制带时间戳的文件
        shutil.copy2(source_file, dest_file)
        print(f"✅ 已复制到: {dest_file}")
        
        # 复制最新版本（覆盖）
        shutil.copy2(source_file, latest_file)
        print(f"✅ 最新版本: {latest_file}")
        
        # 显示文件信息
        file_size = os.path.getsize(dest_file) / (1024 * 1024)  # MB
        print(f"\n📊 文件信息:")
        print(f"   大小: {file_size:.2f} MB")
        print(f"   时间戳: {timestamp}")
        
    except Exception as e:
        print(f"❌ 复制失败: {e}")
        return 1
    
    # 3. 显示后续步骤
    print("\n✨ 完成！后续步骤：")
    print("1. 打开 ~/Downloads 目录查看文件")
    print("2. 上传到云器Lakehouse的Volume上")
    print("3. 在云器Lakehouse中创建外部函数")
    print("\n💡 提示: 文件已准备好，可以直接上传！")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())