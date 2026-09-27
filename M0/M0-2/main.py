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
        
    denom = math.sqrt(dx*dy)#修改错误的公式
    if denom ==0:
        raise ValueError("方差为0,无法计算相关系数")
    #增加除零保护
    r = prod / denom
    return n, mean_x, mean_y, r

def main():
    # 1. 接收命令行的 --config 参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True, help="配置文件路径")
    args = parser.parse_args()

    try:
        # 2. 调用函数执行流程
            cfg = load_config(args.config)
            csv_path = cfg["input_csv"]
            col_x = cfg["columns"]["x"]
            col_y = cfg["columns"]["y"]
            
            xs, ys = load_data(csv_path, col_x, col_y)
            n, mean_x, mean_y, r = calculate_correlation(xs, ys)
            
            
            # 3. 打印结果
            print(f"r = {r}")        
        # 只有 verbose 为 true 才打印中间量
            if cfg.get("task", {}).get("verbose") is True:
                print("n =", n)
                print("mean_x =", mean_x)
                print("mean_y =", mean_y)
    except FileNotFoundError:
            print("错误：配置文件或数据文件不存在，请检查路径。")
            sys.exit(1)
    except KeyError as e:
            print(f"错误：配置或数据中缺少必需的列名，具体缺失: {e}")
            sys.exit(1)
    except ValueError as e:
            print(f"错误：数据格式错误（如空文件或零方差），具体原因: {e}")
            sys.exit(1)
    except Exception as e:
            print(f"错误：发生了未预料的异常：{e}")
            sys.exit(1)
 
if __name__ == '__main__':
    main()