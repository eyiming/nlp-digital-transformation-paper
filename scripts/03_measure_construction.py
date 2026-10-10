# -*- coding: utf-8 -*-
"""
第三步：测度构建
基于数字化关键词词典，分别计算词频测度、TF-IDF 测度与综合指数。
"""
import os
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

# 路径设置
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")

# 数字化关键词词典
DIGITAL_KEYWORDS = {
    "人工智能": [
        "人工智能", "AI", "机器学习", "深度学习", "神经网络", "自然语言处理",
        "计算机视觉", "智能算法", "机器人流程自动化", "专家系统", "智能语音", "智能客服"
    ],
    "大数据": [
        "大数据", "数据挖掘", "数据分析", "数据仓库", "数据治理", "商业智能",
        "用户画像", "精准营销", "海量数据", "实时数据", "数据驱动", "数据资产"
    ],
    "云计算": [
        "云计算", "云服务", "云平台", "云存储", "边缘计算", "分布式计算",
        "容器化", "微服务", "SaaS", "PaaS", "IaaS", "公有云", "私有云", "混合云"
    ],
    "物联网与区块链": [
        "物联网", "工业互联网", "智能制造", "传感器", "RFID", "区块链",
        "去中心化", "智能合约", "供应链溯源", "万物互联", "工业 4.0", "智能工厂"
    ]
}

ALL_KEYWORDS = []
for dim_words in DIGITAL_KEYWORDS.values():
    ALL_KEYWORDS.extend(dim_words)
ALL_KEYWORDS = list(set(ALL_KEYWORDS))


def count_keywords(tokens, keywords):
    """统计关键词在分词文本中的出现次数"""
    token_list = tokens.split()
    counter = Counter(token_list)
    return sum(counter[k] for k in keywords if k in counter)


def compute_freq_measure(df):
    """词频测度"""
    df["dti_freq"] = df["tokens"].apply(lambda x: np.log1p(count_keywords(x, ALL_KEYWORDS)))
    # 子维度
    for dim, words in DIGITAL_KEYWORDS.items():
        col = f"dti_{dim}"
        df[col] = df["tokens"].apply(lambda x: np.log1p(count_keywords(x, words)))
    return df


def compute_tfidf_measure(df):
    """TF-IDF 测度"""
    # 使用 sklearn 计算 TF-IDF
    vectorizer = TfidfVectorizer(
        vocabulary={k: i for i, k in enumerate(ALL_KEYWORDS)},
        lowercase=False,
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=False
    )
    tfidf_matrix = vectorizer.fit_transform(df["tokens"].fillna(""))
    # 对每个文档的数字化关键词 TF-IDF 值求和
    scores = tfidf_matrix.sum(axis=1).A1
    df["dti_tfidf"] = np.log1p(scores)
    return df, vectorizer


def standardize(series):
    """Z-score 标准化"""
    return (series - series.mean()) / series.std()


def main():
    input_path = os.path.join(RESULTS_DIR, "preprocessed_data.csv")
    df = pd.read_csv(input_path, encoding="utf-8-sig")

    print("开始构建测度指标...")
    df = compute_freq_measure(df)
    df, vectorizer = compute_tfidf_measure(df)

    # 综合指数：标准化后取平均
    df["dti"] = 0.5 * (standardize(df["dti_freq"]) + standardize(df["dti_tfidf"]))

    # 输出测度结果表
    output_path = os.path.join(RESULTS_DIR, "dti_results.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"测度结果已保存：{output_path}")
    print("测度变量：dti, dti_freq, dti_tfidf, dti_人工智能, dti_大数据, dti_云计算, dti_物联网与区块链")


if __name__ == "__main__":
    main()
