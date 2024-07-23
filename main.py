from ocr import getTargetPosition
from utils import *
import time
from loguru import logger


@logTime('图像识别')
def main():
    logger.info('开始运行')

    img = getScreenShot('Chrome')
    img = crop_image(img, 0, 364, 300, 600)
    img = getPIL(img)

    position = getTargetPosition(img, '栅格')

    logger.info(f"目标位置: {position}")


if __name__ == '__main__':
    main()
