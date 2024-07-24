from ocr import getTargetPosition
from utils import *
import time
from loguru import logger
import numpy as np


@logTime('图像识别')
@doUntil()
def main():
    logger.info('图像识别中...')

    # img = getScreenShot(handle='Chrome', area=[0, 364, 300, 600])
    img = getScreenShot(area=[0, 364, 300, 600])
    # img = crop_image(img, 0, 364, 300, 600)
    img = np.array(img)

    position = getTargetPosition(img, '栅格')

    position = None if len(position) == 0 else position[0]

    if position:
        logger.info(f"目标位置: {position}")
        return True

    return False


if __name__ == '__main__':
    main()
