# -*- coding: utf-8 -*-
"""
主运行脚本：依次执行五步流水线。
"""
import sys
import os

# 将 scripts 目录加入路径
sys.path.insert(0, os.path.dirname(__file__))

import importlib

# Python 模块名不能以数字开头，因此使用 importlib 动态导入
step1 = importlib.import_module("01_data_generation")
step2 = importlib.import_module("02_text_preprocessing")
step3 = importlib.import_module("03_measure_construction")
step4 = importlib.import_module("04_reliability_validity")
step5 = importlib.import_module("05_regression_analysis")

if __name__ == "__main__":
    print("=" * 60)
    print("开始运行 NLP 测度构建五步流水线")
    print("=" * 60)
    step1.main()
    print()
    step2.main()
    print()
    step3.main()
    print()
    step4.main()
    print()
    step5.main()
    print()
    print("=" * 60)
    print("流水线运行完毕，请查看 results/ 目录下的输出文件。")
    print("=" * 60)
