# -*- coding: utf-8 -*-
"""
第二步：文本预处理
对模拟年报文本进行清洗、分词、去停用词等处理。
"""
import os
import re
import jieba
import pandas as pd

# 路径设置
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# 自定义词典（数字化关键词）
CUSTOM_WORDS = [
    "人工智能", "机器学习", "深度学习", "神经网络", "自然语言处理", "计算机视觉",
    "智能算法", "机器人流程自动化", "专家系统", "智能语音", "智能客服",
    "大数据", "数据挖掘", "数据分析", "数据仓库", "数据治理", "商业智能",
    "用户画像", "精准营销", "海量数据", "实时数据", "数据驱动", "数据资产",
    "云计算", "云服务", "云平台", "云存储", "边缘计算", "分布式计算",
    "容器化", "微服务", "公有云", "私有云", "混合云",
    "物联网", "工业互联网", "智能制造", "供应链溯源", "智能合约",
    "去中心化", "万物互联", "智能工厂", "工业 4.0"
]
for word in CUSTOM_WORDS:
    jieba.add_word(word)

# 停用词表（简化版）
STOPWORDS = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也",
    "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这", "那",
    "公司", "本年度", "报告期", "我们", "将", "与", "及", "等", "之", "中", "为", "以", "通过",
    "进行", "实现", "持续", "进一步", "不断", "积极", "完善", "加强", "建立", "提升",
    "推动", "促进", "随着", "根据", "关于", "以及", "从而", "因此", "同时", "并且"
])


def clean_text(text):
    """清洗文本：去除特殊符号、数字编号、空白等"""
    # 去除英文标点和特殊字符
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9\s]", " ", text)
    # 去除连续空格
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text):
    """分词并去除停用词"""
    words = jieba.lcut(text)
    words = [w.strip() for w in words if len(w.strip()) > 1 and w.strip() not in STOPWORDS]
    return " ".join(words)


def main():
    input_path = os.path.join(DATA_DIR, "simulated_panel.csv")
    df = pd.read_csv(input_path, encoding="utf-8-sig")

    print("开始文本预处理...")
    df["clean_text"] = df["report_text"].apply(clean_text)
    df["tokens"] = df["clean_text"].apply(tokenize)

    output_path = os.path.join(RESULTS_DIR, "preprocessed_data.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"预处理完成：{output_path}")
    print(f"示例分词结果：{df['tokens'].iloc[0][:120]}...")


if __name__ == "__main__":
    main()
