import random
import argparse
import yaml
import sys
import json
import os
import time

def load_config(config_path):
    if not os.path.isfile(config_path):
        print(f"错误：配置文件路径 '{config_path}' 不存在，或是一个目录")
        sys.exit(1)
    
    try:
        if config_path.endswith(('.yaml', '.yml')):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        elif config_path.endswith('.json'):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"错误：不支持的文件格式 '{config_path}'，请使用 .yaml/.yml/.json")
            sys.exit(1)
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        print(f"错误：解析配置文件失败，存在语法错误 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：发生了未预料的异常：{e}")
        sys.exit(1)

def validate_tasks(config):
    tasks=config.get('tasks',[])
    if not tasks:
        print("错误，任务列表为空，没有可执行的tasks")
        sys.exit(1)

    task_map={}
    for task in tasks:
        name=task.get('name')
        if not name:
            print("错误：存在没有定义name的任务")
            sys.exit(1)
        if name in task_map:
            print(f"错误：任务名{name}重复，任务名须唯一")
            sys.exit(1)
        
        rate=task.get('success_rate',1.0)
        if not isinstance(rate,(int,float)) or not (0<=rate<=1):
            print(f"错误，任务{name}的success rate必须在0到1之间")
            sys.exit(1)

        deps=task.get('dependencies',[])
        if not isinstance(deps,list):
            print(f"错误，任务{name}的dependencies必须是列表")
            sys.exit(1)   

        task_map[name]=task

    Adjacency={name:[] for name in task_map}
    in_degree={name:0 for name in task_map}

    for name,task in task_map.items():
        for dep in task.get('dependencies',[]):
            if dep not in task_map: 
                print(f"错误：任务{name}依赖不存在的任务{dep}")
                sys.exit(1)
            Adjacency[dep].append(name)
            in_degree[name]+=1

    queue=[]
    for name in task_map:
        if in_degree[name]==0:
            queue.append(name)
    sorted_tasks=[]

    while queue:
        curr=queue.pop(0)
        sorted_tasks.append(curr)
        for neighbour in Adjacency[curr]:
            in_degree[neighbour]-=1
            if in_degree[neighbour]==0:
                queue.append(neighbour)

    if len(sorted_tasks)!=len(task_map):
        print("错误：检测到依赖环")
        sys.exit(1)

    return sorted_tasks,task_map

def print_status(status, name, attempts=None):
    colors = {
        "SUCCESS": "\033[92m", # 绿色（去掉了一个反斜杠）
        "FAILED": "\033[91m",  # 红色
        "RETRY": "\033[93m",   # 黄色
        "SKIPPED": "\033[94m", # 蓝色
        "TIMEOUT": "\033[91m"  # 红色（超时也用红色表示警告）
    }
    reset = "\033[0m"
    
    # 核心防护：如果是非 TTY 环境（比如重定向到文件），不要输出颜色代码
    if not sys.stdout.isatty():
        print(f"{status}: {name}" + (f" (尝试次数: {attempts})" if attempts is not None else ""))
        return

    # 正常终端环境：带颜色输出
    color = colors.get(status, "")
    msg = f"{color}{status}{reset}: {name}"
    if attempts is not None:
        msg += f" (尝试次数: {attempts})"
    print(msg)

def execute_tasks(task_map,sorted_tasks,timeout):
    start_time=time.time()
    total_duration=0.0  
    is_timeout=False  
    task_results=[]  
    status_map={}  

    for name in sorted_tasks:
        task=task_map[name]
        duration=task.get("duration",1.0)
        success_rate=task.get("success_rate",1.0)
        dependencies=task.get("dependencies",[])

        should_skip=False          
        for dep in dependencies:
            dep_status=status_map.get(dep)
            if dep_status in ["SKIPPED","FAILED","TIMEOUT"]:
                should_skip=True
                break
        
        if should_skip:
            task_results.append({
                "name":name,
                "status":"SKIPPED",
                "attempts":0,
                "duration":0.0,
                "started_at":None,
                "ended_at":None
            })
            status_map[name]="SKIPPED"
            print_status("SKIPPED",name,0)
            continue

        if timeout is not None and (time.time()-start_time)>timeout:
            is_timeout=True
            break

        task_start_time=time.time()
        attempts=0
        final_status="FAILED"     

        while attempts<3:
            attempts+=1
            time.sleep(duration)
            total_duration+=duration

            if timeout is not None and (time.time()-start_time)>timeout:
                is_timeout=True
                break

            if random.random()<success_rate:
                final_status="SUCCESS"
                print_status("SUCCESS",name,attempts)
                break
            else:
                if attempts<3:
                    print_status("FAILED","",attempts)
                    print_status("RETRY",name,attempts)
                else:
                    final_status="SKIPPED"
                    print_status("SKIPPED",name,attempts)

        if is_timeout:
            final_status="TIMEOUT"
            task_end_time=time.time()
            task_results.append({
                "name":name,
                "status":final_status,
                "attempts":attempts,
                "duration":round(task_end_time - task_start_time, 2), 
                "started_at":task_start_time,
                "ended_at":task_end_time
            })
            status_map[name]=final_status
            print_status("TIMEOUT",name,attempts)
            break

        task_end_time=time.time()
        task_results.append({
            "name":name,
            "status":final_status,
            "attempts":attempts,
            "duration":round(task_end_time - task_start_time, 2),
            "started_at":task_start_time,
            "ended_at":task_end_time
        })
        status_map[name]=final_status

    if is_timeout:
        for name in sorted_tasks:
            if name not in status_map:
                task_results.append({
                    "name":name,
                    "status":"TIMEOUT",
                    "attempts":0,
                    "duration":0.0,
                    "started_at":None,
                    "ended_at":None
                })
                status_map[name]="TIMEOUT"
                print_status("TIMEOUT",name,0)

    return task_results,total_duration,is_timeout

# 生成报告函数
def save_report(report_path, is_timeout, total_duration, task_results):
    report_data = {
        "timeout": is_timeout,
        "total_duration": round(total_duration, 2),
        "tasks": task_results
    }
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        print(f"\n报告已成功写入：{report_path}")
    except Exception as e:
        print(f"错误：写入报告文件失败 - {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Taskschedule - 任务调度模拟器")
    parser.add_argument("--config", type=str, required=True, help='任务配置文件路径(.yaml/.yml/.json)')
    parser.add_argument("--timeout", type=float, default=None, help="覆盖配置文件中的timeout值")
    parser.add_argument("--report", type=str, default="report.json", help="默认输出report.json")
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    args = parser.parse_args()

    random.seed(args.seed)

    config = load_config(args.config)
    sorted_tasks,task_map=validate_tasks(config)
    
    timeout = args.timeout if args.timeout is not None else config.get("timeout", 15.0)
    
    task_results, total_duration, is_timeout = execute_tasks(task_map, sorted_tasks, timeout)

    save_report(args.report, is_timeout, total_duration, task_results)

if __name__ == '__main__':
    main()