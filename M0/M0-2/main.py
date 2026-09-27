import argparse
import yaml
import csv
import math
import sys

def load_config(config_path):
    """读取 yaml 配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    return cfg

def load_data(csv_path, col_x, col_y):
    """读取 csv 并提取两列数据"""
    xs = []
    ys = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            xs.append(float(row[col_x]))
            ys.append(float(row[col_y]))
    return xs, ys

def calculate_correlation(xs, ys):
    """计算相关系数"""
    n = len(xs)
    sum_x = sum(xs)
    sum_y = sum(ys)
    
    mean_x = sum_x / n
    mean_y = sum_y / n
    
    dx = 0.0
    dy = 0.0
    prod = 0.0
    for i in range(n):
        a = xs[i] - mean_x
        b = ys[i] - mean_y
        dx = dx + a * a
        dy = dy + b * b
        prod = prod + a * b
        
    denom = dx * dy 
    r = prod / denom
    return n, mean_x, mean_y, r

def main():
    # 1. 接收命令行的 --config 参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True, help="配置文件路径")
    args = parser.parse_args()
    
    # 2. 调用函数执行流程
    cfg = load_config(args.config)
    csv_path = cfg["input_csv"]
    col_x = cfg["columns"]["x"]
    col_y = cfg["columns"]["y"]
    
    xs, ys = load_data(csv_path, col_x, col_y)
    n, mean_x, mean_y, r = calculate_correlation(xs, ys)
    
    # 3. 打印结果（暂时不管 verbose）
    print("n =", n)
    print("mean_x =", mean_x)
    print("mean_y =", mean_y)
    print("r =", r)

if __name__ == '__main__':
    main()