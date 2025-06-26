#!/usr/bin/env python3
"""
复制已打包的文件到Downloads目录
"""

import os
import shutil
from datetime import datetime

def main():
    """主函数"""
    print("📂 ClickZetta AI Functions 复制到Downloads")
    print("="*60)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(current_dir, 'dist', 'clickzetta_ai_functions_full.zip')
    
    # 检查源文件是否存在
    if not os.path.exists(source_file):
        print(f"❌ 错误: 找不到打包文件 {source_file}")
        print("请先运行打包脚本: python3 scripts/package_with_deps.py")
        return 1
    
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
        file_time = os.path.getmtime(source_file)
        package_time = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n📊 文件信息:")
        print(f"   大小: {file_size:.2f} MB")
        print(f"   打包时间: {package_time}")
        print(f"   复制时间: {timestamp}")
        
    except Exception as e:
        print(f"❌ 复制失败: {e}")
        return 1
    
    # 显示后续步骤
    print("\n✨ 完成！后续步骤：")
    print("1. 打开 ~/Downloads 目录查看文件")
    print("2. 上传到云存储（OSS/COS/S3）")
    print("3. 在ClickZetta中创建外部函数")
    print("\n💡 提示: 文件已准备好，可以直接上传！")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())