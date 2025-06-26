# ClickZetta AI SQL Functions 测试指南

## 📋 目录

1. [测试概述](#测试概述)
2. [测试环境准备](#测试环境准备)
3. [测试工具介绍](#测试工具介绍)
4. [运行测试](#运行测试)
5. [测试策略](#测试策略)
6. [测试用例设计](#测试用例设计)
7. [性能测试](#性能测试)
8. [测试报告解读](#测试报告解读)
9. [持续集成](#持续集成)
10. [故障排查](#故障排查)

## 测试概述

ClickZetta AI Functions 测试体系包含：
- **功能测试**：验证30个AI函数的正确性
- **性能测试**：确保响应时间和数据大小符合要求
- **回归测试**：防止新修改破坏现有功能
- **集成测试**：验证与ClickZetta平台的兼容性

### 测试指标
- **功能覆盖率**：100%（所有30个函数）
- **成功率目标**：≥90%
- **性能目标**：平均响应时间 <5秒
- **数据优化**：符合JIRA-001要求（67%压缩率）

## 测试环境准备

### 1. 安装测试依赖

```bash
# 基础测试环境
pip install pytest pytest-asyncio pytest-timeout

# 性能测试工具
pip install memory_profiler line_profiler

# 测试报告
pip install pytest-html pytest-json-report
```

### 2. 配置测试环境

```bash
# 设置API密钥（必需）
export TEST_DASHSCOPE_API_KEY="sk-xxxxxxx"

# 可选：设置测试模式
export TEST_MODE="quick"  # quick/full/performance

# 可选：设置测试输出目录
export TEST_OUTPUT_DIR="./test_results"
```

### 3. 准备测试数据

```bash
# 生成测试数据
python tests/prepare_test_data.py

# 验证测试数据
ls -la data/
# 应该看到：
# - test_config.json
# - batch_test_data.json
# - test_images.json
# - test_documents.json
```

## 测试工具介绍

### 1. test_complete_coverage.py
完整的功能测试套件，测试所有30个函数。

```bash
# 运行完整测试
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY

# 测试特定类别
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY --category 文本处理

# 测试单个函数
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY --function ai_text_summarize
```

### 2. quick_validation.py
快速验证核心功能（10个最常用函数）。

```bash
# 快速验证（2-3分钟）
python tests/quick_validation.py $TEST_DASHSCOPE_API_KEY

# 输出简化报告
python tests/quick_validation.py $TEST_DASHSCOPE_API_KEY --simple
```

### 3. smart_analyzer.py
智能分析测试结果，识别问题模式。

```bash
# 分析最新测试结果
python tests/smart_analyzer.py

# 分析特定测试报告
python tests/smart_analyzer.py --report test_report_20250614.json

# 生成优化建议
python tests/smart_analyzer.py --suggest-optimizations
```

### 4. 批量测试工具

```bash
# 批量测试所有函数
python tests/run_batch_tests.py $TEST_DASHSCOPE_API_KEY

# 并行测试（加速）
python tests/run_batch_tests.py $TEST_DASHSCOPE_API_KEY --parallel 4

# 生成测试矩阵
python tests/run_batch_tests.py $TEST_DASHSCOPE_API_KEY --matrix
```

## 运行测试

### 基础测试流程

```bash
# 1. 快速验证环境
python tests/check_test_env.py

# 2. 运行核心测试
python tests/quick_validation.py $TEST_DASHSCOPE_API_KEY

# 3. 运行完整测试
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY

# 4. 分析结果
python tests/smart_analyzer.py
```

### 高级测试选项

```bash
# 详细日志模式
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY --verbose

# 保存原始响应
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY --save-responses

# 重试失败的测试
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY --retry-failed

# 跳过慢速测试
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY --skip-slow
```

### 持续测试

```bash
# 监视模式（文件变化时自动测试）
python tests/watch_and_test.py

# 定时测试（每小时）
python tests/scheduled_test.py --interval 3600
```

## 测试策略

### 1. 分层测试策略

```
┌─────────────────────────┐
│    E2E集成测试（10%）    │  <- 完整的ClickZetta部署测试
├─────────────────────────┤
│    功能测试（60%）       │  <- 每个函数的功能验证
├─────────────────────────┤
│    单元测试（30%）       │  <- 辅助函数和工具类
└─────────────────────────┘
```

### 2. 测试优先级

**P0 - 关键路径**（必须通过）
- 文本摘要、情感分析、实体提取
- 文本向量化、语义相似度
- 图片描述、OCR

**P1 - 重要功能**（应该通过）
- 翻译、关键词提取
- 聚类准备、向量搜索
- 视频分析、语音转文字

**P2 - 辅助功能**（可以失败）
- 高级业务场景函数
- 需要特殊配额的函数

### 3. 测试数据策略

```python
# 测试数据分类
test_data_types = {
    "edge_cases": [
        "",  # 空字符串
        " ",  # 纯空格
        "a" * 10000,  # 超长文本
        "🎉😀",  # 表情符号
        "<script>alert()</script>",  # 特殊字符
    ],
    "normal_cases": [
        "正常的中文文本",
        "Normal English text",
        "混合文本 with English",
    ],
    "business_cases": [
        # 真实业务场景数据
    ]
}
```

## 测试用例设计

### 1. 功能测试用例模板

```python
def test_ai_function_template():
    """测试用例模板"""
    # Arrange - 准备测试数据
    test_input = {
        "text": "测试文本",
        "api_key": TEST_API_KEY,
        "model_name": "qwen-plus"
    }
    
    # Act - 执行测试
    result = ai_function_impl([[
        test_input["text"],
        test_input["api_key"],
        test_input["model_name"]
    ]])
    
    # Assert - 验证结果
    assert len(result) == 1
    response = json.loads(result[0])
    
    # 验证必需字段
    assert "result" in response or "error" in response
    if "result" in response:
        assert len(response["result"]) > 0
    
    # 验证响应格式
    assert isinstance(response, dict)
```

### 2. 边界测试

```python
# 空输入测试
def test_empty_input():
    result = ai_text_summarize_impl([["", api_key]])
    response = json.loads(result[0])
    assert "error" in response
    assert "空" in response["error"] or "empty" in response["error"].lower()

# 超长输入测试
def test_large_input():
    large_text = "测试" * 5000  # 10000字符
    result = ai_text_summarize_impl([[large_text, api_key]])
    response = json.loads(result[0])
    # 应该成功处理或返回合理的错误
    assert "result" in response or "error" in response

# 特殊字符测试
def test_special_characters():
    special_text = "测试\n\t\r特殊\"字符'<>&"
    result = ai_text_summarize_impl([[special_text, api_key]])
    response = json.loads(result[0])
    assert len(result[0]) > 0  # 确保不会崩溃
```

### 3. 性能测试用例

```python
import time

def test_performance():
    """性能测试"""
    start_time = time.time()
    
    # 执行函数
    result = ai_text_summarize_impl([[test_text, api_key]])
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # 验证性能指标
    assert execution_time < 5.0, f"执行时间 {execution_time}s 超过限制"
    
    # 验证响应大小
    response_size = len(result[0])
    assert response_size < 10000, f"响应大小 {response_size} 超过限制"
```

## 性能测试

### 1. 响应时间测试

```bash
# 运行性能测试套件
python tests/performance_test.py $TEST_DASHSCOPE_API_KEY

# 生成性能报告
python tests/performance_test.py $TEST_DASHSCOPE_API_KEY --report

# 压力测试（并发）
python tests/performance_test.py $TEST_DASHSCOPE_API_KEY --concurrent 10
```

### 2. 内存使用测试

```bash
# 内存分析
python -m memory_profiler tests/memory_test.py

# 生成内存使用图表
python tests/memory_test.py --plot
```

### 3. 数据大小优化测试（JIRA-001 验证）

#### 响应大小测试框架
```python
# test_response_optimization.py
import json
import sys
from collections import defaultdict

class ResponseOptimizationTester:
    """响应优化效果测试器"""
    
    def __init__(self):
        self.results = defaultdict(list)
        self.target_compression = 0.67  # JIRA-001 目标
        
    def test_function_optimization(self, func_name, test_input, api_key):
        """测试单个函数的优化效果"""
        # 获取函数响应
        response = call_function(func_name, test_input, api_key)
        response_json = json.loads(response)
        
        # 分析响应
        analysis = self.analyze_response(response_json)
        
        # 检测冗余内容
        redundancy = self.detect_redundancy(response_json)
        
        # 计算优化潜力
        optimization_potential = self.calculate_optimization_potential(
            response, redundancy
        )
        
        self.results[func_name].append({
            "original_size": len(response),
            "redundancy_score": redundancy["score"],
            "optimization_potential": optimization_potential,
            "issues": redundancy["issues"]
        })
        
        return analysis
    
    def detect_redundancy(self, response_obj):
        """检测响应中的冗余内容"""
        issues = []
        redundancy_bytes = 0
        
        # 检查礼貌用语
        politeness_patterns = [
            "感谢您", "希望对您有帮助", "请问还有什么",
            "根据您的要求", "我已经为您", "以下是"
        ]
        
        response_str = json.dumps(response_obj, ensure_ascii=False)
        for pattern in politeness_patterns:
            if pattern in response_str:
                issues.append(f"包含冗余礼貌用语: {pattern}")
                redundancy_bytes += len(pattern) * response_str.count(pattern)
        
        # 检查过度嵌套
        nesting_depth = self.get_nesting_depth(response_obj)
        if nesting_depth > 3:
            issues.append(f"过度嵌套: 深度{nesting_depth}")
            redundancy_bytes += 50 * (nesting_depth - 3)
        
        # 检查空值和null
        empty_count = self.count_empty_values(response_obj)
        if empty_count > 0:
            issues.append(f"包含{empty_count}个空值")
            redundancy_bytes += empty_count * 10
        
        # 检查重复的字段名
        if self.has_redundant_keys(response_obj):
            issues.append("存在冗余的字段结构")
            redundancy_bytes += 100
        
        return {
            "score": redundancy_bytes / len(response_str),
            "bytes": redundancy_bytes,
            "issues": issues
        }
    
    def get_nesting_depth(self, obj, depth=0):
        """计算JSON嵌套深度"""
        if isinstance(obj, dict):
            return max([self.get_nesting_depth(v, depth + 1) 
                       for v in obj.values()], default=depth)
        elif isinstance(obj, list) and obj:
            return max([self.get_nesting_depth(item, depth + 1) 
                       for item in obj])
        return depth
    
    def count_empty_values(self, obj):
        """统计空值数量"""
        count = 0
        if isinstance(obj, dict):
            for v in obj.values():
                if v is None or v == "" or v == []:
                    count += 1
                else:
                    count += self.count_empty_values(v)
        elif isinstance(obj, list):
            for item in obj:
                count += self.count_empty_values(item)
        return count
    
    def generate_report(self):
        """生成优化测试报告"""
        print("\n📊 响应优化测试报告")
        print("=" * 60)
        
        total_functions = len(self.results)
        optimized_functions = 0
        
        for func_name, tests in self.results.items():
            avg_size = sum(t["original_size"] for t in tests) / len(tests)
            avg_redundancy = sum(t["redundancy_score"] for t in tests) / len(tests)
            
            print(f"\n{func_name}:")
            print(f"  平均大小: {avg_size:.0f} bytes")
            print(f"  冗余度: {avg_redundancy:.1%}")
            
            # 显示主要问题
            all_issues = []
            for t in tests:
                all_issues.extend(t["issues"])
            
            issue_counts = defaultdict(int)
            for issue in all_issues:
                issue_counts[issue] += 1
            
            print("  主要问题:")
            for issue, count in sorted(issue_counts.items(), 
                                      key=lambda x: x[1], 
                                      reverse=True)[:3]:
                print(f"    - {issue} (出现{count}次)")
            
            # 判断是否需要优化
            if avg_redundancy > 0.3:
                print("  ⚠️  建议优化")
                optimized_functions += 1
            else:
                print("  ✅ 已优化")
        
        print(f"\n总结: {optimized_functions}/{total_functions} 个函数需要优化")
```

#### 批量优化测试脚本
```python
# batch_optimization_test.py
def test_all_functions_optimization():
    """批量测试所有函数的优化情况"""
    tester = ResponseOptimizationTester()
    
    # 测试配置
    test_cases = {
        "ai_text_summarize": {
            "input": "这是一段很长的测试文本...",
            "expected_max_size": 3000
        },
        "ai_text_sentiment_analyze": {
            "input": "这个产品非常好用",
            "expected_max_size": 500
        },
        # ... 其他函数
    }
    
    for func_name, config in test_cases.items():
        print(f"测试 {func_name}...")
        
        # 测试原始版本
        result = tester.test_function_optimization(
            func_name, 
            config["input"], 
            api_key
        )
        
        # 验证大小限制
        if result["size"] > config["expected_max_size"]:
            print(f"  ❌ 超出预期大小: {result['size']} > {config['expected_max_size']}")
        else:
            print(f"  ✅ 大小符合预期: {result['size']} bytes")
    
    # 生成报告
    tester.generate_report()
```

#### 优化前后对比测试
```python
def compare_before_after_optimization():
    """对比优化前后的效果"""
    
    # 模拟优化前的响应
    before = {
        "status": "success",
        "message": "处理成功",
        "data": {
            "result": {
                "content": "根据您的要求，我已经为您分析了这段文本。这段文本表达了正面情感。希望这个结果对您有所帮助。",
                "sentiment": "正面",
                "score": 0.95,
                "confidence": "high",
                "details": {
                    "positive": 0.95,
                    "negative": 0.03,
                    "neutral": 0.02
                }
            },
            "metadata": {
                "model": "qwen-plus",
                "version": "1.0",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }
    }
    
    # 优化后的响应
    after = {
        "sentiment": "正面",
        "score": 0.95
    }
    
    # 计算压缩率
    before_size = len(json.dumps(before, ensure_ascii=False))
    after_size = len(json.dumps(after, ensure_ascii=False))
    compression = 1 - (after_size / before_size)
    
    print(f"优化前: {before_size} bytes")
    print(f"优化后: {after_size} bytes")
    print(f"压缩率: {compression:.1%}")
    print(f"达到JIRA-001目标: {'✅' if compression >= 0.67 else '❌'}")
```

#### 向量函数特殊测试
```python
def test_vector_functions_should_not_compress():
    """验证向量函数不应该被压缩"""
    vector_functions = [
        "ai_text_to_embedding",
        "ai_text_clustering_prepare",
        "ai_image_to_embedding"
    ]
    
    for func_name in vector_functions:
        response = call_function(func_name, test_input, api_key)
        data = json.loads(response)
        
        # 检查向量维度
        if "embedding" in data:
            vector_size = len(data["embedding"])
            vector_bytes = len(json.dumps(data["embedding"]))
            
            print(f"{func_name}:")
            print(f"  向量维度: {vector_size}")
            print(f"  数据大小: {vector_bytes} bytes")
            print(f"  判定: {'✅ 正常' if vector_bytes > 10000 else '❌ 可能被错误压缩'}")
```

## 测试报告解读

### 1. 测试报告结构

```json
{
    "summary": {
        "total_functions": 30,
        "successful": 28,
        "failed": 2,
        "success_rate": 0.933,
        "average_response_time": 3.44,
        "test_duration": 245.6
    },
    "details": {
        "ai_text_summarize": {
            "status": "success",
            "response_time": 2.3,
            "response_size": 1248,
            "output_sample": "..."
        }
    },
    "failures": [
        {
            "function": "ai_image_to_embedding",
            "error": "需要更高API配额",
            "suggestion": "升级API套餐"
        }
    ]
}
```

### 2. 关键指标解读

- **成功率**：>90% 优秀，80-90% 良好，<80% 需改进
- **响应时间**：<3s 优秀，3-5s 良好，>5s 需优化
- **数据大小**：根据函数类型判断
  - 文本函数：<5KB
  - 向量函数：20-30KB（正常）
  - 多模态函数：<10KB

### 3. 问题分类

```python
# smart_analyzer.py 的问题分类
problem_categories = {
    "api_errors": ["AuthenticationError", "RateLimitError"],
    "input_errors": ["空输入", "格式错误"],
    "timeout_errors": ["超时", "响应慢"],
    "size_errors": ["响应过大", "内存溢出"]
}
```

## 分阶段部署测试策略

### 🎯 经过验证的最佳实践

基于实际项目经验，分阶段部署测试是定位"函数找不到"等部署问题的最有效方法。

### 测试阶段设计

```bash
# 创建测试目录
mkdir deployment_tests
cd deployment_tests
```

#### 第1阶段：基础环境测试
```python
# test_stage1_basic.py
from clickzetta.external_function.annotate import annotate

@annotate("stage1_echo", 
    [{"name": "message", "type": "string"}],
    {"type": "string"})
def stage1_echo_impl(rows):
    """最基础的测试，无任何依赖"""
    return [f"Echo: {row[0]}" for row in rows]

# SQL测试
# SELECT stage1_echo('Hello ClickZetta');
# 预期输出: "Echo: Hello ClickZetta"
```

#### 第2阶段：Python标准库测试
```python
# test_stage2_stdlib.py
import json
import datetime
from clickzetta.external_function.annotate import annotate

@annotate("stage2_stdlib", 
    [{"name": "data", "type": "string"}],
    {"type": "string"})
def stage2_stdlib_impl(rows):
    """测试Python标准库功能"""
    results = []
    for row in rows:
        result = {
            "input": row[0],
            "timestamp": datetime.datetime.now().isoformat(),
            "json_works": True
        }
        results.append(json.dumps(result))
    return results
```

#### 第3阶段：第三方依赖测试
```python
# test_stage3_dependencies.py
import json
import dashscope
import requests
from clickzetta.external_function.annotate import annotate

@annotate("stage3_check_deps", 
    [{"name": "check_type", "type": "string"}],
    {"type": "string"})
def stage3_check_deps_impl(rows):
    """验证第三方包是否正确加载"""
    results = []
    for row in rows:
        deps_info = {
            "dashscope_version": getattr(dashscope, '__version__', 'unknown'),
            "requests_version": requests.__version__,
            "dashscope_module": str(type(dashscope)),
            "check_type": row[0]
        }
        results.append(json.dumps(deps_info))
    return results
```

#### 第4阶段：网络连接测试
```python
# test_stage4_network.py
import json
import requests
from clickzetta.external_function.annotate import annotate

@annotate("stage4_network", 
    [{"name": "url", "type": "string"}],
    {"type": "string"})
def stage4_network_impl(rows):
    """测试网络连接能力"""
    results = []
    for row in rows:
        try:
            response = requests.get(row[0], timeout=5)
            result = {
                "url": row[0],
                "status_code": response.status_code,
                "network": "connected"
            }
        except Exception as e:
            result = {
                "url": row[0],
                "error": str(e),
                "network": "failed"
            }
        results.append(json.dumps(result))
    return results
```

#### 第5阶段：API密钥测试
```python
# test_stage5_api.py
import json
import dashscope
from clickzetta.external_function.annotate import annotate

@annotate("stage5_api_test", 
    [{"name": "api_key", "type": "string"}],
    {"type": "string"})
def stage5_api_test_impl(rows):
    """测试API密钥有效性"""
    results = []
    for row in rows:
        try:
            # 设置API密钥
            dashscope.api_key = row[0]
            
            # 尝试最小化的API调用
            from dashscope import Tokenization
            resp = Tokenization.call(
                model='qwen-turbo',
                messages=[{"role": "user", "content": "test"}]
            )
            
            result = {
                "api_status": "valid",
                "token_count": resp.usage.input_tokens
            }
        except Exception as e:
            result = {
                "api_status": "invalid",
                "error": str(e)[:100]  # 截断错误信息
            }
        results.append(json.dumps(result))
    return results
```

### 执行测试流程

```bash
# 1. 打包每个阶段
python package_stage_test.py stage1
python package_stage_test.py stage2
# ... 依次类推

# 2. 部署并测试每个阶段
# 上传 stage1.zip
PUT 'file://stage1.zip' TO 'volume://tests/stage1.zip';

# 创建函数
CREATE EXTERNAL FUNCTION stage1_echo(message STRING)
RETURNS STRING
AS 'volume://tests/stage1.zip'
CONNECTION = test_connection
RUNTIME = 'python3.8'
HANDLER = 'test_stage1_basic.stage1_echo_impl';

# 测试
SELECT stage1_echo('test');
```

### 问题定位指南

| 失败阶段 | 可能原因 | 解决方案 |
|---------|---------|---------|
| 阶段1 | Handler路径错误、装饰器问题 | 检查模块名.函数名格式 |
| 阶段2 | Python版本不兼容 | 确认使用python3.8 |
| 阶段3 | 依赖包未打包 | 检查ZIP包内容 |
| 阶段4 | 网络限制 | 检查VPC配置、安全组 |
| 阶段5 | API密钥无效 | 验证密钥、检查配额 |

### 自动化测试脚本

```python
# auto_stage_test.py
import subprocess
import time

stages = [
    ("stage1_echo", "SELECT stage1_echo('test')"),
    ("stage2_stdlib", "SELECT stage2_stdlib('test')"),
    ("stage3_check_deps", "SELECT stage3_check_deps('all')"),
    ("stage4_network", "SELECT stage4_network('https://httpbin.org/get')"),
    ("stage5_api_test", "SELECT stage5_api_test('sk-xxx')")
]

for func_name, test_sql in stages:
    print(f"\n🧪 Testing {func_name}...")
    
    # 执行SQL测试
    result = execute_sql(test_sql)
    
    if "error" in result.lower():
        print(f"❌ {func_name} failed!")
        print(f"   Error: {result}")
        print("   Stopping at this stage for debugging.")
        break
    else:
        print(f"✅ {func_name} passed!")
        time.sleep(2)  # 避免过快执行

print("\n📊 测试完成!")
```

## 持续集成

### 1. GitHub Actions 配置

```yaml
# .github/workflows/test.yml
name: AI Functions Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 */6 * * *'  # 每6小时

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-html
    
    - name: Run tests
      env:
        TEST_DASHSCOPE_API_KEY: ${{ secrets.DASHSCOPE_API_KEY }}
      run: |
        python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: test_results/
```

### 2. 本地CI脚本

```bash
#!/bin/bash
# scripts/run_ci_tests.sh

echo "🚀 开始CI测试流程"

# 1. 代码质量检查
echo "📝 检查代码质量..."
flake8 src/ tests/ || exit 1

# 2. 运行测试
echo "🧪 运行测试套件..."
python tests/test_complete_coverage.py $TEST_DASHSCOPE_API_KEY || exit 1

# 3. 生成报告
echo "📊 生成测试报告..."
python tests/smart_analyzer.py --ci-mode

# 4. 检查覆盖率
echo "📈 检查测试覆盖率..."
python tests/check_coverage.py --threshold 90

echo "✅ CI测试完成!"
```

## 故障排查

### 1. 常见问题诊断

```bash
# 诊断脚本
python tests/diagnose.py

# 检查特定问题
python tests/diagnose.py --check api-connection
python tests/diagnose.py --check response-format
python tests/diagnose.py --check performance
```

### 2. 调试技巧

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 保存中间结果
def debug_function(input_data):
    # 保存输入
    with open("debug_input.json", "w") as f:
        json.dump(input_data, f, ensure_ascii=False)
    
    # 执行函数
    result = ai_function(input_data)
    
    # 保存输出
    with open("debug_output.json", "w") as f:
        json.dump(result, f, ensure_ascii=False)
    
    return result
```

### 3. 问题修复流程

1. **识别问题**
   ```bash
   python tests/identify_failures.py
   ```

2. **隔离测试**
   ```bash
   python tests/test_single_function.py ai_function_name
   ```

3. **应用修复**
   ```bash
   python scripts/fix_function.py ai_function_name
   ```

4. **验证修复**
   ```bash
   python tests/verify_fix.py ai_function_name
   ```

## 测试最佳实践

### 1. 测试原则
- **独立性**：每个测试应该独立运行
- **可重复**：测试结果应该一致
- **快速反馈**：优先运行快速测试
- **有意义的断言**：验证业务逻辑，不只是技术细节

### 2. 测试组织
```
tests/
├── unit/              # 单元测试
├── functional/        # 功能测试
├── performance/       # 性能测试
├── integration/       # 集成测试
└── fixtures/          # 测试数据
```

### 3. 测试命名
```python
# 好的命名
def test_text_summarize_returns_summary_with_key_points():
def test_empty_input_returns_error():
def test_large_text_processed_within_timeout():

# 避免的命名
def test_1():
def test_function():
def test_it_works():
```

---

*最后更新：2025-06-14*