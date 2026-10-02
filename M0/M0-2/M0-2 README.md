# M0-2相关性计算分析工具-README

## 1. 项目简介
本项目（main.py）是一个命令行数据处理工具。它通过读取 YAML 配置文件，提取指定的 CSV 文件中的两列数据，并计算这两列数据的皮尔逊相关系数,同时输出样本量及各自的均值。

## 2. 如何运行
在终端中，确保当前目录包含main.py、config.yaml和sample_data.csv,然后执行以下命令：
`python3 main.py --config config.yaml`
参数说明：--config 是必填参数（required=True），用于指定配置文件的路径。

本项目包含针对核心函数的单元测试，运行命令如下：
`PYTHONPATH=. uv run pytest tests/`

## 3. 输入文件格式要求
### 3.1 .yaml的字段规则要求
一.input_csv 必须是字符串，且路径准确。
二.columns 下的 x 和 y 必须与CSV文件中的表头名称一字不差，也要注意大小写区分。否则程序会报错提示缺失列名。
三.注意缩进。如果YAML文件缩进错误，yaml.safe_load 会解析失败。
四.task：包含 name 和 verbose 字段。verbose 控制是否输出中间结果（样本数 n 和均值 mean），值为 true 或 false。
### 3.2 .csv数据文件
一.CSV第一行必须是包含列名的表头（sensor_a,sensor_b）
二.columns.a,columns.b的指定列中，所有数据必须是数字（整数或浮点数）

## 4. 输出数据含义
n (样本数量)：成功读取并参与计算的配对数据的个数。通过 len(xs) 获取。
mean_x (X列均值)：X轴数据（sensor_a）的平均值。
mean_y (Y列均值)：Y轴数据（sensor_b）的平均值。
r (皮尔逊相关系数)：
取值与解读：r 的取值范围永远是 [-1, 1] 之间。
r > 0：正相关。
r < 0：负相关。
r = 1 / -1：完全正/负相关。
r = 0：无线性相关。

## 5. AI的使用
1.运用AI辅助我完成了numpy验证部分以及test检验部分的编写。
2.让AI对我完成的主代码(main.py)进行检查，并提出改良建议。
3.对于main.py的AI改良部分,和我不熟悉的numpy与pytest部分，我有逐行认真学习分析。