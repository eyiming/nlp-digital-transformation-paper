# -*- coding: utf-8 -*-
"""
第五步：回归分析
检验数字化转型指数对未来研发投入强度与全要素生产率的影响。
"""
import os
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")


def winsorize(series, lower=0.01, upper=0.99):
    """1% 与 99% 分位缩尾"""
    q_low = series.quantile(lower)
    q_high = series.quantile(upper)
    return series.clip(q_low, q_high)


def main():
    input_path = os.path.join(RESULTS_DIR, "dti_results.csv")
    df = pd.read_csv(input_path, encoding="utf-8-sig")

    # 生成下一期变量
    df = df.sort_values(["firm_id", "year"])
    df["rd_t1"] = df.groupby("firm_id")["rd"].shift(-1)
    df["tfp_t1"] = df.groupby("firm_id")["tfp"].shift(-1)

    # 缩尾处理
    for col in ["dti", "dti_freq", "dti_tfidf", "rd", "rd_t1", "tfp", "tfp_t1", "size", "lev", "roa", "age"]:
        df[col] = winsorize(df[col])

    # 删除缺失值
    df_reg = df.dropna(subset=["rd_t1", "tfp_t1", "dti", "size", "lev", "roa", "age"])

    # 生成虚拟变量
    df_reg = pd.get_dummies(df_reg, columns=["industry", "year"], drop_first=True)
    industry_dummies = [c for c in df_reg.columns if c.startswith("industry_")]
    year_dummies = [c for c in df_reg.columns if c.startswith("year_")]

    # 模型 1-2：研发投入强度
    model1 = smf.ols(
        "rd_t1 ~ dti",
        data=df_reg
    ).fit(cov_type="HC3")

    controls = " + ".join(["size", "lev", "roa", "age"] + industry_dummies + year_dummies)
    model2 = smf.ols(
        f"rd_t1 ~ dti + {controls}",
        data=df_reg
    ).fit(cov_type="HC3")

    # 模型 3-4：全要素生产率
    model3 = smf.ols(
        "tfp_t1 ~ dti",
        data=df_reg
    ).fit(cov_type="HC3")

    model4 = smf.ols(
        f"tfp_t1 ~ dti + {controls}",
        data=df_reg
    ).fit(cov_type="HC3")

    # 整理结果表格
    def make_table(models, var_names, y_names):
        rows = []
        for var in var_names:
            row = {"变量": var}
            for i, model in enumerate(models):
                if var in model.params.index:
                    coef = model.params[var]
                    se = model.bse[var]
                    pval = model.pvalues[var]
                    stars = "***" if pval < 0.01 else ("**" if pval < 0.05 else ("*" if pval < 0.1 else ""))
                    row[y_names[i]] = f"{coef:.4f}{stars}\n({se:.4f})"
                else:
                    row[y_names[i]] = "—"
            rows.append(row)
        # 添加 R2 与 N
        rows.append({"变量": "R²"})
        for i, model in enumerate(models):
            rows[-1][y_names[i]] = f"{model.rsquared:.4f}"
        rows.append({"变量": "观测值"})
        for i, model in enumerate(models):
            rows[-1][y_names[i]] = f"{int(model.nobs)}"
        return pd.DataFrame(rows)

    rd_table = make_table([model1, model2], ["dti", "size", "lev", "roa", "age"], ["(1) RD", "(2) RD"])
    rd_table.to_csv(os.path.join(RESULTS_DIR, "regression_rd.csv"), index=False, encoding="utf-8-sig")
    print("研发投入回归结果已保存")
    print(rd_table.to_string(index=False))

    tfp_table = make_table([model3, model4], ["dti", "size", "lev", "roa", "age"], ["(3) TFP", "(4) TFP"])
    tfp_table.to_csv(os.path.join(RESULTS_DIR, "regression_tfp.csv"), index=False, encoding="utf-8-sig")
    print("全要素生产率回归结果已保存")
    print(tfp_table.to_string(index=False))


if __name__ == "__main__":
    main()
