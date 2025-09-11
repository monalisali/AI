# 配置log
import logging
from datetime import datetime
import os

def setup_logging():
    """配置日志系统（仅需调用一次）"""
    # 确保日志目录存在
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # 日志文件名称（包含日期和目录）
    log_filename = f"{log_dir}/app_{datetime.now().strftime('%Y%m%d')}.log"
    
    # 日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 基础配置
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format=log_format,
        datefmt=date_format
    )
    
    # 添加控制台输出（可选）
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    # logging.getLogger().addHandler(console_handler)