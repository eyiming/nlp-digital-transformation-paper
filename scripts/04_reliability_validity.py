# -*- coding: utf-8 -*-
"""
第四步：信效度检验
包括描述性统计、Cronbach's Alpha、KMO、Bartlett 检验与主成分分析。
"""
import os
import numpy as np
import pandas as pd
from factor_analyzer.factor_analyzer import calculate_kmo
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from sklearn.decomposition import PCA

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")


def cronbach_alpha(items):
    """计算 Cronbach's Alpha 系数"""
    items = np.array(items)
    n_items = items.shape[1]
    variances = items.var(axis=0, ddof=1)
    total_variance = items.sum(axis=1).var(ddof=1)
    alpha = (n_items / (n_items - 1)) * (1 - variances.sum() / total_variance)
    return alpha


def main():
    input_path = os.path.join(RESULTS_DIR, "dti_results.csv")
    df = pd.read_csv(input_path, encoding="utf-8-sig")

    # 主要变量
    main_vars = ["dti", "dti_freq", "dti_tfidf", "rd", "tfp", "size", "lev", "roa", "age"]
    desc = df[main_vars].describe().T
    desc["min"] = df[main_vars].min()
    desc["max"] = df[main_vars].max()
    desc = desc[["count", "mean", "std", "min", "50%", "max"]].round(4)
    desc.to_csv(os.path.join(RESULTS_DIR, "descriptive_stats.csv"), encoding="utf-8-sig")
    print("描述性统计已保存")

    # 相关性矩阵
    corr_vars = [
        "dti", "dti_freq", "dti_tfidf",
        "dti_人工智能", "dti_大数据", "dti_云计算", "dti_物联网与区块链"
    ]
    corr = df[corr_vars].corr(method="pearson").round(4)
    corr.to_csv(os.path.join(RESULTS_DIR, "correlation_matrix.csv"), encoding="utf-8-sig")
    print("相关性矩阵已保存")

    # 信效度检验
    sub_dims = ["dti_人工智能", "dti_大数据", "dti_云计算", "dti_物联网与区块链"]
    items = df[sub_dims].values

    alpha = cronbach_alpha(items)
    kmo_all, kmo_model = calculate_kmo(items)
    chi_square, p_value = calculate_bartlett_sphericity(items)

    # 主成分分析
    pca = PCA(n_components=4)
    pca.fit(items)
    explained_ratio = pca.explained_variance_ratio_[0]
    loadings = pca.components_[0] * np.sqrt(pca.explained_variance_[0])

    reliability_results = pd.DataFrame({
        "检验项目": [
            "Cronbach's Alpha",
            "KMO 值",
            "Bartlett 卡方值",
            "Bartlett p 值",
            "第一主成分方差解释率",
            "人工智能载荷",
            "大数据载荷",
            "云计算载荷",
            "物联网与区块链载荷",
        ],
        "统计量": [
            round(alpha, 4),
            round(kmo_model, 4),
            round(chi_square, 4),
            round(p_value, 6),
            round(explained_ratio, 4),
            round(loadings[0], 4),
            round(loadings[1], 4),
            round(loadings[2], 4),
            round(loadings[3], 4),
        ]
    })
    reliability_results.to_csv(
        os.path.join(RESULTS_DIR, "reliability_validity.csv"),
        index=False,
        encoding="utf-8-sig"
    )
    print("信效度检验结果已保存")
    print(reliability_results.to_string(index=False))


if __name__ == "__main__":
    main()
