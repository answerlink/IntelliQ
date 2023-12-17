import logging


def setup_logging():
    # 设置日志的配置
    logging.basicConfig(
        level=logging.DEBUG,  # 设置日志级别为 DEBUG，也可以设置为 INFO, WARNING, ERROR, CRITICAL
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
        filename='app.log',  # 日志输出到文件，不设置这个参数则输出到标准输出（控制台）
        filemode='a'  # 'w' 表示写模式，'a' 表示追加模式
    )

    # 如果还想要将日志输出到控制台，可以添加一个 StreamHandler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 设置控制台的日志级别
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)
    logging.info('logging start...')


# 示例：记录一条信息
# logging.info("This is an info message")
