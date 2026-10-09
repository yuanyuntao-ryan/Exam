# M0-4包含参数说明和运行示例的README

## 一、参数说明
| 参数 | 必填 | 说明 |
| :--- | :--- | :--- |
| --config <path> | 是 | 任务配置文件（.yaml / .yml / .json）|
| --timeout <float> | 否 | 覆盖配置文件中的超时时间（秒）|
| --report <path> | 否 | 报告输出路径，默认 report.json |
| --seed <int> | 否 | 随机种子，用于复现同一随机结果（强烈建议添加）|

## 二、运行示例
### 示例一：正常执行
终端输入:`python3 scheduler.py --config tasks_demo.yaml --seed 42`
预期结果：终端生成彩色SUCCESS日志,所有任务按照依赖顺序执行，输出report.json

### 示例二：超时
终端输入：`python3 scheduler.py --config tasks_demo.yaml --timeout 5 --seed 42`
预期结果：程序在运行到某个任务时触发全局超时，状态变为 TIMEOUT，未执行的任务也会记录为 TIMEOUT，终端显示红色警告。

### 示例三：任务失败与级联跳过（SKIPPED）
演示任务失败重试 3 次后转为 SKIPPED，并且其下游依赖任务也会立刻被标记为 SKIPPED（不执行、不耗时）。
终端输入：`python3 scheduler.py --config tasks_fail_demo.yaml --seed 42`
预期结果：Navigate 尝试 3 次均失败，状态最终记为 SKIPPED（蓝色终端输出）。
依赖 Navigate 的 DetectQR、Grasp、Place 状态也会瞬间变为 SKIPPED，尝试次数为 0。
总耗时只有 Init 和 Navigate 重试的耗时总和（0.5 + 2.5*3 = 8.0 秒）。