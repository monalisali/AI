# main.py
import logging
from log_config import setup_logging
import job
import WeixinArticalSpider as spider

#系统入口
if __name__ == "__main__":
    setup_logging()  
    # 主程序日志
    logger = logging.getLogger(__name__)  # 获取当前模块的日志器
    logger.info("主程序启动")
    #job.configAndStart_job()   
    urlFileName = spider.startToReadArtical()
    if urlFileName is not None and len(urlFileName) > 0:
        spider.GetArticalConetent(urlFileName)

