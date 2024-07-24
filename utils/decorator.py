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
            logger.info(f"{logTitle} 完成，用时: {elapsed_time:.2f}s")
            return result

        return wrapper

    return decorator


def doUntil(timeout: float | None = None, delay: float = 0.1):
    """
    重复执行函数直到返回结果的装饰器
    :param timeout: 超时时间，单位秒
    :param delay: 延迟时间，单位秒
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            start_time = time.time()
            while True:
                result = func(*args, **kwargs)
                if result:
                    return result

                if timeout and time.time() - start_time > timeout:
                    logger.error(f"函数 {func.__name__} 运行 {timeout} 秒 已超时 结束运行")
                    return None

                time.sleep(delay)

            return None

        return wrapper

    return decorator
