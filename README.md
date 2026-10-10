# 基于上市公司年报文本的数字化转型程度测度研究

**仓库地址**：https://github.com/eyiming/nlp-digital-transformation-paper

## 项目简介

本项目是「预演毕业论文」的完整可复现仓库，研究主题为**基于上市公司年报文本的数字化转型程度测度**。研究采用自然语言处理（NLP）方法，以沪深 A 股上市公司年报文本为分析对象，构建企业数字化转型程度综合测度指标，并通过描述性统计、信效度检验与回归分析验证测度的有效性。

## 仓库结构

```
.
├── data/                      # 数据文件
│   ├── simulated_panel.csv    # 企业-年份面板数据（含模拟年报文本）
│   └── data_source_note.md    # 数据来源说明
├── scripts/                   # Python 五步流水线
│   ├── 01_data_generation.py      # 第一步：生成模拟数据
│   ├── 02_text_preprocessing.py # 第二步：文本预处理
│   ├── 03_measure_construction.py # 第三步：测度构建
│   ├── 04_reliability_validity.py # 第四步：信效度检验
│   ├── 05_regression_analysis.py  # 第五步：回归分析
│   └── run_all.py                 # 一键运行全部流水线
├── results/                   # 测度结果与分析输出
│   ├── preprocessed_data.csv
│   ├── dti_results.csv
│   ├── descriptive_stats.csv
│   ├── correlation_matrix.csv
│   ├── reliability_validity.csv
│   ├── regression_rd.csv
│   └── regression_tfp.csv
├── paper/                     # 论文正文
│   ├── paper.md               # Markdown 版论文（约 8400 字）
│   └── 基于上市公司年报文本的数字化转型程度测度研究.docx  # Word 版论文（含封面、目录、参考文献）
├── figures/                   # 可视化图表
│   ├── dti_trend.png          # DTI 年度趋势
│   ├── dti_industry_box.png   # DTI 行业分布
│   └── correlation_heatmap.png # 相关系数热力图
├── scripts/06_visualization.py # 第六步：可视化
├── requirements.txt           # Python 依赖
└── README.md                  # 本文件
```

## 五步流水线说明

| 步骤 | 脚本 | 功能 |
|:----:|:----|:----|
| 1 | `01_data_generation.py` | 生成模拟的上市公司年报文本与企业-年份面板数据 |
| 2 | `02_text_preprocessing.py` | 文本清洗、中文分词、去停用词 |
| 3 | `03_measure_construction.py` | 基于关键词词典构建词频测度、TF-IDF 测度与综合指数 DTI |
| 4 | `04_reliability_validity.py` | 描述性统计、相关性分析、Cronbach's Alpha、KMO、Bartlett、PCA |
| 5 | `05_regression_analysis.py` | 检验 DTI 对未来研发投入强度与全要素生产率的影响 |
| 6 | `06_visualization.py` | 生成年度趋势、行业分布与相关系数热力图（输出至 `figures/`） |

## 环境配置与运行方式

### 1. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. 运行五步流水线

```bash
cd scripts
python run_all.py
```

或分步运行：

```bash
cd scripts
python 01_data_generation.py
python 02_text_preprocessing.py
python 03_measure_construction.py
python 04_reliability_validity.py
python 05_regression_analysis.py
```

### 3. 查看结果

运行完成后，所有结果文件将保存在 `results/` 目录下。

## 主要变量说明

| 变量 | 说明 |
|:----|:----|
| `dti` | 数字化转型综合指数（标准化后的词频与 TF-IDF 均值） |
| `dti_freq` | 数字化词频测度 |
| `dti_tfidf` | 数字化 TF-IDF 测度 |
| `dti_人工智能` | 人工智能子维度得分 |
| `dti_大数据` | 大数据子维度得分 |
| `dti_云计算` | 云计算子维度得分 |
| `dti_物联网与区块链` | 物联网与区块链子维度得分 |
| `rd` | 研发投入强度 |
| `tfp` | 全要素生产率 |

## 数据来源

- **年报文本**：巨潮资讯网（www.cninfo.com.cn）上市公司年度报告 PDF，通过 Python 批量下载并转为 TXT（本仓库使用模拟数据演示流程）。
- **财务数据**：CSMAR 国泰安数据库 / Wind 金融终端。
- **行业分类**：中国证监会 2012 年行业分类标准。

详见 [`data/data_source_note.md`](data/data_source_note.md)。

## 论文信息

- 标题：基于上市公司年报文本的数字化转型程度测度研究
- 字数：约 7000 字
- 结构：摘要、绪论、研究设计、测度方法、实验与结果分析、结论与展望、参考文献、附录
- 文件位置：[`paper/paper.md`](paper/paper.md)

## 作者信息

- 姓名：鄂一铭（E Yiming）
- 学校：大连财经学院 管理学院
- 专业：大数据管理与应用
- 联系方式：942873406@qq.com

## 许可说明

本项目仅用于学术学习与课程作业展示，数据为模拟生成，不代表任何真实企业。
