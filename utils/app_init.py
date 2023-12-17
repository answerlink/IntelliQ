# encoding=utf-8
from config.log_config import setup_logging


def before_init():
    """
    app主程序启动初始化
    """
    # 在程序主入口处调用设置日志的函数
    setup_logging()
