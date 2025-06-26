#!/usr/bin/env python
"""
验证本地代码是否已正确更新
"""

import re

def check_mock_mode():
    """检查代码中是否还有模拟模式"""
    with open('ai_functions_complete.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找"模拟模式"
    mock_mode_matches = re.findall(r'模拟模式', content)
    if mock_mode_matches:
        print("❌ 发现模拟模式引用：", len(mock_mode_matches), "处")
        return False
    
    # 查找正确的错误处理
    error_handling = 'DashScope library not available. Please ensure the deployment package includes all dependencies.'
    if error_handling in content:
        print("✅ 错误处理已更新")
    else:
        print("❌ 未找到新的错误处理信息")
        return False
    
    # 统计HAS_DASHSCOPE检查
    has_dashscope_checks = len(re.findall(r'if not HAS_DASHSCOPE:', content))
    print(f"📊 找到 {has_dashscope_checks} 个 HAS_DASHSCOPE 检查")
    
    return True

def test_local_function():
    """测试本地函数行为"""
    from ai_functions_complete import ai_text_summarize
    
    # 创建实例并测试
    func = ai_text_summarize()
    result = func.evaluate("测试文本", "test-key")
    print("\n🧪 本地测试结果：")
    print(result)
    
    # 检查结果
    import json
    result_dict = json.loads(result)
    if "note" in result_dict and "模拟模式" in result_dict.get("note", ""):
        print("❌ 本地代码仍返回模拟模式")
        return False
    elif result_dict.get("error") == True:
        print("✅ 本地代码正确返回错误信息")
        return True
    else:
        print("⚠️ 未知的返回格式")
        return False

if __name__ == "__main__":
    print("🔍 验证本地代码...")
    print("=" * 50)
    
    # 检查代码
    code_ok = check_mock_mode()
    
    print("\n" + "=" * 50)
    
    # 测试函数
    test_ok = test_local_function()
    
    print("\n" + "=" * 50)
    
    if code_ok and test_ok:
        print("\n✅ 本地代码验证通过！")
        print("请确保：")
        print("1. 使用最新的 clickzetta_ai_functions_full.zip")
        print("2. 完全重新部署（删除旧函数后重建）")
    else:
        print("\n❌ 本地代码仍有问题，请检查！")