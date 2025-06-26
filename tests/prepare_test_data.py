#!/usr/bin/env python3
"""
准备测试数据文件
为AI函数测试创建必要的数据文件
"""

import json
import os

def create_test_data_files():
    """创建测试数据文件"""
    data_dir = "/Users/liangmo/Documents/GitHub/clickzetta_aisql/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. 创建示例文本文件
    test_texts = {
        "long_article.txt": """人工智能的发展历程与未来展望

人工智能（Artificial Intelligence，AI）作为计算机科学的一个重要分支，正在深刻改变着我们的世界。
从20世纪50年代的图灵测试开始，AI经历了多次起伏，如今终于迎来了爆发式增长。

深度学习的突破
近年来，深度学习技术的突破成为AI发展的关键转折点。通过模拟人脑神经网络的工作方式，
深度学习算法在图像识别、语音识别、自然语言处理等领域取得了前所未有的成果。
特别是2012年AlexNet在ImageNet竞赛中的胜利，标志着深度学习时代的到来。

应用领域的扩展
AI技术已经渗透到各个行业：
- 医疗健康：AI辅助诊断、药物研发、个性化治疗
- 金融科技：风险评估、反欺诈、智能投顾
- 智能制造：预测性维护、质量控制、供应链优化
- 自动驾驶：感知、决策、控制系统的智能化

未来展望
随着计算能力的提升和数据量的增长，AI将继续向通用人工智能（AGI）迈进。
量子计算、脑机接口等新技术的发展，可能为AI带来新的突破。
同时，AI伦理、隐私保护、算法公平性等问题也需要我们共同关注和解决。""",
        
        "customer_reviews.json": [
            {
                "id": "001",
                "text": "产品质量非常好，超出预期！包装精美，物流速度快。客服态度很好，解答问题很耐心。",
                "rating": 5
            },
            {
                "id": "002", 
                "text": "功能基本满足需求，但是价格偏高。希望能有更多优惠活动。",
                "rating": 3
            },
            {
                "id": "003",
                "text": "收到货发现有轻微瑕疵，联系客服后很快解决了。整体体验还不错。",
                "rating": 4
            }
        ],
        
        "product_catalog.json": [
            {
                "id": "P001",
                "name": "智能手表Pro",
                "category": "电子产品",
                "features": ["心率监测", "GPS定位", "50米防水", "7天续航"],
                "price": 2999
            },
            {
                "id": "P002",
                "name": "无线降噪耳机",
                "category": "音频设备",
                "features": ["主动降噪", "30小时续航", "快速充电", "多设备连接"],
                "price": 1599
            }
        ],
        
        "contracts_sample.json": [
            {
                "contract_id": "CTR-2024-001",
                "text": """销售合同

合同编号：CTR-2024-001
签订日期：2024年1月15日

甲方（卖方）：北京科技发展有限公司
统一社会信用代码：91110108MA01XXXX
地址：北京市海淀区中关村大街1号

乙方（买方）：上海创新贸易有限公司  
统一社会信用代码：91310115MA1K4XXX
地址：上海市浦东新区张江高科技园区

一、产品信息
产品名称：企业级AI分析平台
产品型号：AI-ENT-V3.0
数量：1套
单价：人民币100万元整

二、交付时间
交付日期：2024年3月1日前

三、付款方式
签订合同后7个工作日内支付30%预付款
产品交付验收合格后30日内支付剩余70%"""
            }
        ],
        
        "resumes_sample.json": [
            {
                "id": "R001",
                "text": """个人简历

基本信息
姓名：张三
性别：男
年龄：28岁
电话：138****5678
邮箱：zhangsan@example.com

教育背景
2014.09-2018.06  北京大学  计算机科学与技术  本科
主修课程：数据结构、算法设计、机器学习、数据库系统

工作经历
2021.03-至今  阿里巴巴集团  高级算法工程师
- 负责推荐系统算法优化，CTR提升15%
- 主导实时特征工程平台建设
- 带领3人团队完成千万级用户画像系统

2018.07-2021.02  字节跳动  算法工程师
- 参与短视频推荐算法开发
- 优化模型训练流程，效率提升40%

专业技能
编程语言：Python, Java, C++
机器学习：TensorFlow, PyTorch, Scikit-learn
大数据：Spark, Hadoop, Flink"""
            }
        ]
    }
    
    # 保存文本文件
    for filename, content in test_texts.items():
        filepath = os.path.join(data_dir, filename)
        if filename.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        print(f"✅ 创建文件: {filepath}")
    
    # 2. 创建测试配置文件
    test_config = {
        "test_scenarios": {
            "text_processing": {
                "description": "文本处理场景测试",
                "test_cases": [
                    {
                        "name": "长文本摘要",
                        "function": "ai_text_summarize",
                        "data_file": "long_article.txt",
                        "params": {"max_length": 200}
                    },
                    {
                        "name": "批量情感分析",
                        "function": "ai_text_sentiment_analyze",
                        "data_file": "customer_reviews.json"
                    }
                ]
            },
            "business_analysis": {
                "description": "业务分析场景测试",
                "test_cases": [
                    {
                        "name": "合同信息提取",
                        "function": "ai_contract_extract",
                        "data_file": "contracts_sample.json"
                    },
                    {
                        "name": "简历解析",
                        "function": "ai_resume_parse",
                        "data_file": "resumes_sample.json"
                    }
                ]
            },
            "multimodal": {
                "description": "多模态场景测试",
                "test_images": [
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/images/ocr_test.jpg"
                ]
            }
        },
        "performance_targets": {
            "response_time": {
                "text_functions": 2.0,  # 秒
                "vector_functions": 3.0,
                "multimodal_functions": 5.0
            },
            "compression_rate": 67,  # 百分比
            "success_rate": 95  # 百分比
        }
    }
    
    config_file = os.path.join(data_dir, "test_config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(test_config, f, ensure_ascii=False, indent=2)
    print(f"✅ 创建配置文件: {config_file}")
    
    # 3. 创建批量测试数据
    batch_test_data = {
        "batch_translation": {
            "texts": [
                "Hello, how are you?",
                "Artificial Intelligence is changing the world.",
                "Machine learning algorithms are powerful tools."
            ],
            "target_language": "中文"
        },
        "batch_sentiment": {
            "reviews": [
                "这个产品太棒了，强烈推荐！",
                "质量一般，价格偏高。",
                "客服态度恶劣，非常失望。",
                "物流很快，包装完好。"
            ]
        },
        "batch_classification": {
            "texts": [
                "最新的量子计算技术突破",
                "今日股市大涨，创历史新高",
                "新冠疫苗研发取得重大进展",
                "世界杯决赛精彩回顾"
            ],
            "categories": ["科技", "财经", "医疗", "体育", "其他"]
        }
    }
    
    batch_file = os.path.join(data_dir, "batch_test_data.json")
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(batch_test_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 创建批量测试数据: {batch_file}")
    
    print(f"\n✅ 所有测试数据文件已创建在: {data_dir}")
    return data_dir


def create_performance_test_script():
    """创建性能测试脚本"""
    script_content = '''#!/usr/bin/env python3
"""
性能测试脚本
测试AI函数的并发性能和批量处理能力
"""

import json
import sys
import time
import asyncio
import concurrent.futures
from datetime import datetime

sys.path.insert(0, '/Users/liangmo/Documents/GitHub/clickzetta_aisql')

def test_batch_processing(func_name, test_data, api_key):
    """测试批量处理性能"""
    from ai_functions_complete import ai_text_sentiment_analyze
    
    start_time = time.time()
    results = []
    
    # 创建函数实例
    func = ai_text_sentiment_analyze()
    
    # 批量处理
    for text in test_data:
        result = func.evaluate(text=text, api_key=api_key)
        results.append(result)
    
    end_time = time.time()
    
    return {
        "total_time": end_time - start_time,
        "avg_time": (end_time - start_time) / len(test_data),
        "count": len(test_data),
        "results": results
    }


def test_concurrent_requests(func_name, test_data, api_key, max_workers=5):
    """测试并发请求性能"""
    from ai_functions_complete import ai_text_sentiment_analyze
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 创建函数实例
        func = ai_text_sentiment_analyze()
        
        # 提交并发任务
        futures = []
        for text in test_data:
            future = executor.submit(func.evaluate, text=text, api_key=api_key)
            futures.append(future)
        
        # 等待所有任务完成
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    end_time = time.time()
    
    return {
        "total_time": end_time - start_time,
        "avg_time": (end_time - start_time) / len(test_data),
        "count": len(test_data),
        "max_workers": max_workers
    }


def main():
    if len(sys.argv) < 2:
        print("使用方法: python performance_test.py YOUR_API_KEY")
        return
    
    api_key = sys.argv[1]
    
    # 加载测试数据
    with open('data/batch_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    reviews = test_data['batch_sentiment']['reviews']
    
    print("🚀 开始性能测试")
    print("=" * 50)
    
    # 1. 顺序处理测试
    print("\\n1️⃣ 顺序处理测试")
    seq_result = test_batch_processing('ai_text_sentiment_analyze', reviews, api_key)
    print(f"  总耗时: {seq_result['total_time']:.2f}秒")
    print(f"  平均耗时: {seq_result['avg_time']:.2f}秒/请求")
    
    # 2. 并发处理测试
    print("\\n2️⃣ 并发处理测试")
    for workers in [2, 5, 10]:
        conc_result = test_concurrent_requests(
            'ai_text_sentiment_analyze', reviews, api_key, max_workers=workers
        )
        print(f"  {workers}并发: 总耗时{conc_result['total_time']:.2f}秒, "
              f"平均{conc_result['avg_time']:.2f}秒/请求")
    
    print("\\n✅ 性能测试完成!")


if __name__ == '__main__':
    main()
'''
    
    perf_script = "/Users/liangmo/Documents/GitHub/clickzetta_aisql/performance_test.py"
    with open(perf_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    print(f"✅ 创建性能测试脚本: {perf_script}")


if __name__ == '__main__':
    print("📁 创建测试数据文件...")
    data_dir = create_test_data_files()
    
    print("\n📝 创建性能测试脚本...")
    create_performance_test_script()
    
    print("\n✅ 测试准备完成!")
    print("\n下一步:")
    print("1. 运行完整测试: python test_complete_coverage.py YOUR_API_KEY")
    print("2. 运行性能测试: python performance_test.py YOUR_API_KEY")