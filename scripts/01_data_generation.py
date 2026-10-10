# -*- coding: utf-8 -*-
"""
第一步：数据生成
根据真实数据的统计特征生成模拟的上市公司年报文本与企业-年份面板数据。
"""
import os
import random
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

# 输出路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 参数设置
N_FIRMS = 400
YEARS = list(range(2015, 2023))
INDUSTRIES = [
    "制造业", "信息技术", "金融业", "房地产业", "批发零售",
    "交通运输", "公用事业", "医药生物", "文化传媒", "机械设备"
]

# 数字化转型关键词词典（按维度划分）
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

# 模板化文本片段，用于构建年报
TEMPLATES = [
    "公司始终坚持技术创新驱动发展战略，持续推进{keyword}相关技术的应用与落地。",
    "报告期内，公司加大对{keyword}领域的研发投入，形成了较强的技术积累。",
    "公司积极布局{keyword}，通过数据赋能业务流程优化与管理效率提升。",
    "未来三年，公司将围绕{keyword}打造核心竞争力，推动业务数字化转型。",
    "公司建立了完善的{keyword}技术体系，为业务创新提供坚实支撑。",
]

# 非数字化模板句
GENERAL_TEMPLATES = [
    "公司坚持以客户为中心，持续提升产品与服务质量。",
    "报告期内，公司营业收入保持稳定增长，盈利能力持续改善。",
    "公司不断优化治理结构，加强风险管控与合规管理。",
    "面对复杂多变的市场环境，公司积极调整经营策略，保持稳健发展。",
    "公司重视人才队伍建设，持续完善激励机制。",
]


def generate_annual_report(firm_id, year, industry, digital_level):
    """
    根据企业数字化水平生成模拟年报文本。
    digital_level: 0-1 之间的数值，越高代表数字化程度越强
    """
    paragraphs = []
    # 开篇段落
    paragraphs.append(
        f"{year}年，公司全体员工团结一心，积极应对市场挑战，"
        f"实现营业收入同比增长，持续推动高质量发展。公司所属行业为{industry}。"
    )

    # 数字化相关段落数量与数字化水平相关
    n_digital_paras = max(1, int(digital_level * 8))
    for _ in range(n_digital_paras):
        # 数字化水平越高，段落同时涉及的维度越多，增强维度间共现与内部一致性
        if digital_level < 0.3:
            n_dims = 1
        elif digital_level < 0.6:
            n_dims = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2])[0]
        else:
            n_dims = random.choices([2, 3, 4], weights=[0.3, 0.5, 0.2])[0]
        selected_dims = random.sample(list(DIGITAL_KEYWORDS.keys()), k=n_dims)
        keywords = [random.choice(DIGITAL_KEYWORDS[d]) for d in selected_dims]
        keyword_str = "、".join(keywords)
        template = random.choice(TEMPLATES)
        paragraphs.append(template.format(keyword=keyword_str))

    # 普通段落
    n_general = random.randint(3, 6)
    for _ in range(n_general):
        paragraphs.append(random.choice(GENERAL_TEMPLATES))

    # 结尾段落
    paragraphs.append(
        "展望未来，公司将继续深化改革创新，努力实现可持续发展和股东价值最大化。"
    )

    return "\n".join(paragraphs)


def main():
    records = []
    for firm_id in range(1, N_FIRMS + 1):
        # 企业固定效应
        industry = random.choice(INDUSTRIES)
        # 基础数字化水平：不同行业有差异
        industry_base = {
            "信息技术": 0.55, "制造业": 0.45, "机械设备": 0.40,
            "医药生物": 0.35, "文化传媒": 0.35, "金融业": 0.30,
            "交通运输": 0.25, "公用事业": 0.25, "批发零售": 0.30,
            "房地产业": 0.20
        }[industry]

        # 企业个体异质性
        firm_effect = np.random.normal(0, 0.08)

        for year in YEARS:
            # 随时间递增的数字化趋势
            time_trend = (year - 2015) * 0.03
            # 综合数字化水平
            digital_level = np.clip(
                industry_base + firm_effect + time_trend + np.random.normal(0, 0.05),
                0.05, 0.95
            )

            # 生成年报文本
            report_text = generate_annual_report(firm_id, year, industry, digital_level)

            # 生成财务变量，与数字化水平有一定正相关
            size = np.random.normal(22, 1.2)
            lev = np.clip(np.random.normal(0.45, 0.18), 0.08, 0.85)
            roa = np.clip(np.random.normal(0.04, 0.03), -0.05, 0.15)
            age = np.clip(np.random.normal(2.5, 0.7), 1.0, 3.8)

            # 研发投入强度与未来生产率受数字化水平正向影响
            rd = np.clip(
                0.02 + 0.015 * digital_level + np.random.normal(0, 0.01),
                0.0, 0.18
            )
            tfp = np.clip(
                2.8 + 0.6 * digital_level + 0.08 * (size - 22) + np.random.normal(0, 0.35),
                1.2, 6.5
            )

            records.append({
                "firm_id": f"F{str(firm_id).zfill(4)}",
                "year": year,
                "industry": industry,
                "digital_level_true": round(digital_level, 4),
                "report_text": report_text,
                "size": round(size, 4),
                "lev": round(lev, 4),
                "roa": round(roa, 4),
                "age": round(age, 4),
                "rd": round(rd, 4),
                "tfp": round(tfp, 4),
            })

    df = pd.DataFrame(records)
    output_path = os.path.join(DATA_DIR, "simulated_panel.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"模拟数据已生成：{output_path}")
    print(f"样本量：{len(df)}（{N_FIRMS} 家企业 × {len(YEARS)} 年）")


if __name__ == "__main__":
    main()
