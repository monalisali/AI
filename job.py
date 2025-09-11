#配置和启动定时job
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
import test
import log_config as log

# 要执行的任务方法
def job_function(job_name):
    log.logging.info("开始执行job_function")
    """定时执行的任务函数"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] 执行任务: {job_name}")

def job_function_noArg():
    log.logging.info("job_function_noArg")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] 执行方法: {job_function_noArg}")

# 任务配置列表
job_configs = [
    #{
    #   "name": "每日任务",
    #    "trigger": "cron",  # cron触发器，类似Linux的crontab
    #    "hour": 8,          # 每天8点
    #    "minute": 30        # 30分
    #},
    {
        "function":job_function,
        "name": "每10秒任务",
        "trigger": "interval",  # 间隔触发器
        "seconds": 10,           # 每30秒
        "args": ["每10秒任务"]
    },
     {
        "function":job_function_noArg,
        "name": "每10秒任务",
        "trigger": "interval",  # 间隔触发器
        "seconds": 10,           # 每30秒
    },
    #{
    #  "function":"job_function"
    #  "name": "Test.Print ",
    #  "trigger": "interval",  # 间隔触发器
    #  "seconds": 10           # 每30秒
    #},
    #{
    #    "name": "特定时间点任务",
    #    "trigger": "date",      # 日期触发器（只执行一次）
    #    "run_date": datetime.now() + time delta(seconds=10)  # 10秒后执行
    #}

]


def configAndStart_job():
    # 创建调度器
    scheduler = BlockingScheduler()
    # 根据配置添加任务
    for config in job_configs:
        function_name = config["function"]
        job_args = config.get("args", []) # 有参数就用"args"属性的值，没有参数就传空数组
        scheduler.add_job(
            function_name,
            #args=[config["name"],],  # 传递参数给任务函数
            args = job_args,
            trigger=config["trigger"],
            **{k: v for k, v in config.items() if k not in ["function","name", "trigger","args"]}
        )


    print("定时任务已启动，按Ctrl+C停止...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("定时任务已停止")

"""
if __name__ == "__main__":
    log.setup_logging()
    # 创建调度器
    scheduler = BlockingScheduler()

    # 根据配置添加任务
    for config in job_configs:
        function_name = config["function"]
        job_args = config.get("args", []) # 有参数就用"args"属性的值，没有参数就传空数组
        scheduler.add_job(
            function_name,
            #args=[config["name"],],  # 传递参数给任务函数
            args = job_args,
            trigger=config["trigger"],
            **{k: v for k, v in config.items() if k not in ["function","name", "trigger","args"]}
        )


    print("定时任务已启动，按Ctrl+C停止...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("定时任务已停止")
"""
