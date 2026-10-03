# M0-3任务

## 一、项目简介
本项目是对学长遗留的 `sensor_analyzer.py` 脚本进行缺陷排查与修复。脚本原本意图是读取 `sensor_data.csv`，计算平均值与标准差，剔除离群值，并输出清洗后的 `cleaned_data.csv`。

## 二、代码分析表格
| 缺陷位置(原代码) |       缺陷分析       |    报错现象/有什么问题    |  解决方案  |
| :--- | :---: | :---: | :--- |
| 第37行 | CSV中文件表头是小写的value，代码读取时写成大写，导致字典取不到value值 | 程序报错崩溃，抛出KeyError:'Value' | 将"Value"改为"value" |
| 第61行 | 普通用户没有权限再Linux根目录/下创建和写入out文件夹的权限；且写死绝对路径，不合要求 | 报错PermissionError,无法在根目录写文件 | 移除多余的 "/"，改用相对路径 os.path.join(OUTPUT_DIR, OUTPUT_FILE)并在写入前添加 os.makedirs(OUTPUT_DIR, exist_ok=True) |
| 第51-53行 | 标准差公式写错，acc+=(v-mean)没有对偏差求平方，且最后acc/len(data)没有开根号 | 算出来的是错误的标准差 | 先引入math,再修改为acc+=(v-mean)**2，并在最后使用std=math.sqrt(acc/ len(data)) |
| 第57行 |  判断条件写成了 if v>mean+2*std，只考虑了单侧（偏大）情况 | 只能剔除偏大的离群值，遗漏了偏小的离群值 |  改为绝对值判定：if abs(v - mean) <= 2 * std: |
| 第58行 | 在for循环中直接用 data.remove(v) 删除元素 | 数据清洗不彻底，有遗漏，甚至漏掉相邻数据 | 改为使用for t, v in zip(times, data): 同时遍历时间和数值，将合格数据cleaned.append((t, v))追加到新列表。 |
| 第68行 | writer.writerow([v]) 生成的CSV文件缺少time列，不符合time,value要求 | 写入时只传入了数值v，没有把与之绑定的时间t一起写入 | 修改为writer.writerow([t, v]),确保输出完整两列 |
| 第33,64行 | 未使用上下文管理器，文件句柄在异常时无法释放；未指定 utf-8 编码 | 读写文件没有指定编码，且发生异常时文件无法自动关闭,易乱码 | 使用with open(INPUT_FILE,"r",encoding="utf-8")as f:及with open(output_path, "w", encoding="utf-8") as f:替换原有写法 |
| 整体逻辑 | 缺少异常处理机制 | 遇到文件不存在、空文件、非数值等异常输入时，抛出红色Traceback崩溃;不接收参数 | 引入argparse接收--input和--output带默认值）。用try...except包裹主流程，捕获 FileNotFoundError、KeyError、ValueError等，并统一用sys.exit(1)退出。 |

## 三、AI使用
1.由于对os库不熟悉，os.path.join()部分的函数使用由AI完成
2.完成整体代码修复后交给AI检查与补充
3.每一行代码(尤其是我不懂的与AI补充的)都已认真了解并学习
