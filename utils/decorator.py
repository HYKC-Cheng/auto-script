import time
from loguru import logger


def logTime(logTitle: str):
    """
    记录函数运行时间的装饰器
    :param logTitle: 日志标题
    """

    def decorator(fuc):

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = fuc(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(f"{logTitle} 用时: {elapsed_time:.2f}s")
            return result

        return wrapper

    return decorator
