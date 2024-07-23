from loguru import logger
from ocr import getTargetPosition
from utils import reduce_resolution
import time

if __name__ == '__main__':
    img = 'imgs/1.png'

    start_time = time.time()

    # img = reduce_resolution(img, 0.3) # 降低图像清晰度
    position = getTargetPosition(img, '栅格')

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"识别完成，总用时: {elapsed_time:.2f}s")
    logger.info(f"目标位置: {position}")
