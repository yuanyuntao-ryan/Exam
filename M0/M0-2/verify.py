import numpy as np
from main import load_config, load_data, calculate_correlation

def main():
    print("开始验证手写算法与 numpy 的一致性...\n")
    
    # 1. 读取测试数据
    cfg = load_config('config.yaml')
    csv_path = cfg["input_csv"]
    col_x = cfg["columns"]["x"]
    col_y = cfg["columns"]["y"]
    xs, ys = load_data(csv_path, col_x, col_y)
    
    # 2. 调用手写的核心算法
    n, mean_x, mean_y, r_hand = calculate_correlation(xs, ys)
    
    # 3. 调用 numpy 的标准算法
    r_numpy = np.corrcoef(xs, ys)[0, 1]
    
    # 4. 计算差值并打印
    diff = abs(r_hand - r_numpy)
    print(f"样本数量 (n): {n}")
    print(f"手写相关系数 (r_hand): {r_hand:.10f}")
    print(f"NumPy 相关系数 (r_numpy): {r_numpy:.10f}")
    print(f"绝对误差 (diff): {diff:.2e}\n")
    
    # 5. 误差必须小于 1e-6
    if diff < 1e-6:
        print("✅ 验证通过！手写算法与 numpy 完全一致。")
    else:
        print("❌ 验证失败！误差过大，请检查手写公式。")

if __name__ == '__main__':
    main()