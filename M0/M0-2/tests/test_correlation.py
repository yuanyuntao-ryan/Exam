import sys
import os
import pytest

from main import calculate_correlation

# 测试用例 1：完全正相关
def test_perfect_positive_correlation():
    xs = [1, 2, 3]
    ys = [2, 4, 6]
    n, mean_x, mean_y, r = calculate_correlation(xs, ys)
    # 断言结果等于 1.0，使用 pytest.approx 处理浮点数精度
    assert r == pytest.approx(1.0)

# 测试用例 2：完全负相关
def test_perfect_negative_correlation():
    xs = [1, 2, 3]
    ys = [6, 4, 2]
    n, mean_x, mean_y, r = calculate_correlation(xs, ys)
    # 断言结果等于 -1.0
    assert r == pytest.approx(-1.0)

# 测试用例 3：异常输入（零方差）
def test_zero_variance():
    xs = [1, 1, 1]
    ys = [2, 3, 4]
    with pytest.raises(ValueError):
        calculate_correlation(xs, ys)

# 测试用例 4：异常输入（空列表）
def test_empty_list():
    xs = []
    ys = []
    with pytest.raises(Exception): 
        calculate_correlation(xs, ys)