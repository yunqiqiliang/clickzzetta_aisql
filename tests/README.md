# 云器Lakehouse AI Functions 测试集

## 📋 测试文件说明

### 单元测试
- **minimal_test.py** - 最小化测试，验证基本功能
- **test_dashscope_simple.py** - DashScope API简单测试

### 结构测试
- **test_clickzetta_aisql_structure.py** - 包结构和导入测试
- **test_external_function_format.py** - 外部函数SQL格式测试

### 辅助脚本
- **create_minimal_test.py** - 创建最小化测试函数
- **create_simple_test_function.py** - 创建简单测试函数

## 🚀 运行测试

```bash
# 运行单个测试
python tests/minimal_test.py

# 运行所有测试
python -m pytest tests/
```

## 📝 测试要求

1. 需要有效的DashScope API密钥
2. Python环境需要安装requirements.txt中的依赖
3. 确保ai_functions_complete.py在正确路径

## 🔧 添加新测试

新测试文件应该：
- 使用描述性的文件名
- 包含文档字符串说明测试目的
- 遵循Python测试最佳实践
- 考虑添加到CI/CD流程中