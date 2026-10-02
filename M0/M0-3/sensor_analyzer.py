#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sensor_analyzer.py —— 上一届学长留下的"能用"的脚本

注释（学长原话）：
    "处理一下传感器数据就能用"

原本意图：
    1. 读取 sensor_data.csv（列：time, value）
    2. 计算 value 的平均值、标准差
    3. 剔除离群值（|value - mean| > 2 * std）
    4. 把清洗后的数据保存为 cleaned_data.csv
    5. 打印一份统计摘要

现状：跑不通 / 跑出来数不对。就交给你了。
"""

import csv
import os
import math
import argparse
import sys

def main():
    parser=argparse.ArgumentParser()#错误8修正
    parser.add_argument('--input',default="sensor_data.csv",help="输入CSV文件路径")
    parser.add_argument('--output',default="cleaned_data.csv",help="输出CSV文件路径")
    args=parser.parse_args()

    INPUT_FILE = args.input
    OUTPUT_FILE = args.output
    OUTPUT_DIR = "out" # 输出目录

    try:
        data = []
        times = []
        cleaned = []

        print("=== 传感器数据分析 ===")

    # --- 读取数据 ---
        with open(INPUT_FILE,"r",encoding="utf-8")as f:#错误7修正
            reader=csv.DictReader(f)

            for row in reader:
                t = float(row["time"])
                v = float(row["value"])#错误1修正
                times.append(t)
                data.append(v)

        print("共读取 %d 条数据" % len(data))
        
    # --- 计算平均值 ---
        if len(data)==0:
            print("错误：输入文件中没有有效数据")
            sys.exit(1)
        total = 0
        for v in data:
            total += v
        mean = total / len(data)

    # --- 计算标准差 ---
        acc = 0
        for v in data:
            acc += (v - mean)**2#错误3修正
        std =math.sqrt( acc / len(data))

    # --- 剔除离群值 ---
        for t,v in zip(times,data):
            if abs(v-mean)<=2*std:#错误4修正
                cleaned.append((t,v))#错误5修正

    # --- 输出清洗后的数据 ---
        os.makedirs(OUTPUT_DIR,exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)#错误2修正
        with open(output_path, "w", encoding="utf-8") as f:#错误7修正
            writer = csv.writer(f)
            writer.writerow(["time", "value"])
            for t,v in cleaned:
                writer.writerow([t,v])#错误6修正

        print("均值 mean = %.4f" % mean)
        print("标准差 std = %.4f" % std)
        print("清洗后剩余 %d 条" % len(cleaned))
        print("已保存到 %s" % output_path)
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {args.input}")
        sys.exit(1)
    except KeyError as e:
        print(f"错误：CSV 中缺失所需的列名: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"错误：数据格式错误（如非数值内容）: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：程序运行异常: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

