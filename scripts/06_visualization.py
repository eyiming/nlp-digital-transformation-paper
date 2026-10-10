# -*- coding: utf-8 -*-
"""
第六步（可选）：可视化
生成描述性统计图表与数字化转型趋势图。
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体（Windows 优先 Microsoft YaHei / SimHei）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def plot_dti_trend():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "dti_results.csv"), encoding="utf-8-sig")
    trend = df.groupby("year")["dti"].mean().reset_index()

    plt.figure(figsize=(8, 5))
    sns.lineplot(data=trend, x="year", y="dti", marker="o", linewidth=2)
    plt.title("企业数字化转型指数年均趋势（2015—2022）")
    plt.xlabel("年份")
    plt.ylabel("数字化转型综合指数 DTI")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "dti_trend.png"), dpi=300)
    plt.close()
    print("趋势图已保存：figures/dti_trend.png")


def plot_industry_box():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "dti_results.csv"), encoding="utf-8-sig")

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="industry", y="dti")
    plt.xticks(rotation=45, ha="right")
    plt.title("各行业数字化转型指数分布")
    plt.xlabel("行业")
    plt.ylabel("数字化转型综合指数 DTI")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "dti_industry_box.png"), dpi=300)
    plt.close()
    print("行业分布图已保存：figures/dti_industry_box.png")


def plot_corr_heatmap():
    corr = pd.read_csv(os.path.join(RESULTS_DIR, "correlation_matrix.csv"), encoding="utf-8-sig", index_col=0)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlOrRd", square=True)
    plt.title("数字化转型测度相关性热力图")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "correlation_heatmap.png"), dpi=300)
    plt.close()
    print("相关性热力图已保存：figures/correlation_heatmap.png")


def main():
    print("开始生成可视化图表...")
    plot_dti_trend()
    plot_industry_box()
    plot_corr_heatmap()
    print("可视化完成")


if __name__ == "__main__":
    main()
