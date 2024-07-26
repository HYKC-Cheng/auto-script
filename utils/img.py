import cv2
import pygetwindow as gw
import pyautogui
import time, io
from PIL import Image
import numpy as np
from loguru import logger
from .decorator import logTime, doUntil
from ocr import getTargetPosition
import pydirectinput


def reduce_resolution(image, scale_factor):
    """按比例重新设置图像分辨率

    Args:
        image: 图像，可以是路径，也可以是图像数据
        scale_factor: 压缩比例
    
    Returns:
        resized_image: 压缩后的图像数据
    """

    # 读取图像
    image = cv2.imread(image)

    # 获取原始图像的高度和宽度
    height, width = image.shape[:2]

    # 计算新的宽度和高度
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # 降低分辨率
    resized_image = cv2.resize(image, (new_width, new_height))

    # 保存
    # cv2.imwrite(image, resized_image)

    return resized_image


def getScreenShot(handle: str = None, area: list = None):
    """
    获取屏幕截图

    Args:
        handle (str, optional): 窗口句柄 Defaults to None.
        area (list, optional): 区域坐标，[x, y, width, height]. Defaults to None.

    Returns:
        _type_: 截屏数据
    """

    # 如果有句柄，先激活对应句柄窗口
    if handle:
        gw.getWindowsWithTitle(handle)[0].activate()
        time.sleep(0.5)

    # 截取屏幕截图
    return np.array(pyautogui.screenshot(region=area))


def crop_image(img, x, y, width, height):
    """
    裁剪图像
    :param img: 图像路径
    :param x: 裁剪区域左上角x坐标
    :param y: 裁剪区域左上角y坐标
    :param width: 裁剪区域宽度
    :param height: 裁剪区域高度
    :return: 裁剪后的图像
    """

    cropped_image = img.crop([x, y, x + width, y + height])

    # 保存
    # cropped_image.save('cropped_image.png')

    return cropped_image


def calculate_center(points: list):
    """计算中心点"""
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    return int(center_x), int(center_y)


def template_matching(image: str | np.ndarray, template: str | np.ndarray):
    """
    模板匹配

    Args:
        image: 图像，可以是路径，也可以是图像数据
        template: 模板，可以是路径，也可以是图像数据
    """
    # 如果是字符串路径，先读取
    if isinstance(image, str):
        image = cv2.imread(image)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if isinstance(template, str):
        template = cv2.imread(template)
    # 灰度处理
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # 进行模板匹配
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    # 查找匹配结果中的最大值和最小值及其位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 如果使用的是 CV_TM_CCOEFF_NORMED ，则最大值位置为最佳匹配位置
    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1],
                    top_left[1] + template.shape[0])
    return top_left, bottom_right, max_val


def click_text_until_find(text: str, area: list = None, title: str = ''):
    """
    直到找到文本后点击
    Args:
        text (str): 文本
        area (list, optional): 区域坐标，[x, y, width, height]. Defaults to None.
        title (str, optional): 任务名称. Defaults to ''.
    """
    title = title or '未命名'

    @logTime(title)
    @doUntil(timeout=30)
    def find_text():
        logger.info(f'正在进行 {title} ...')

        img = getScreenShot(area=area)

        position, _ = getTargetPosition(img, text)

        position = None if len(position) == 0 else position[0]

        if position:
            x, y = calculate_center(position)
            logger.success(f"{title} 识别成功，目标位置: {position}")

            if area:
                pydirectinput.moveTo(x + area[0], y + area[1])
            else:
                pydirectinput.moveTo(x, y)

            pydirectinput.click()

            return True

        return False

    find_text()


def click_img_until_find(tempPath: str, area: list = None, title: str = ''):
    """
    直到找到图像后点击
    Args:
        tempPath (str): 模板图片路径
        area (list, optional): 区域坐标，[x, y, width, height]. Defaults to None.
        title (str, optional): 任务名称. Defaults to ''.
    """
    title = title or '未命名'

    @logTime(title)
    @doUntil(timeout=30)
    def find_img():
        logger.info(f'正在进行 {title} ...')

        img = getScreenShot(area=area)

        top_left, bottom_right, max_val = template_matching(img, tempPath)

        if max_val > 0.9:
            logger.success(
                f"{title} 匹配成功，目标位置：{top_left} - {bottom_right} max_val: {max_val}"
            )

            # 取中心点
            x = (top_left[0] + bottom_right[0]) // 2
            y = (top_left[1] + bottom_right[1]) // 2

            if area:
                pydirectinput.moveTo(x + area[0], y + area[1])
            else:
                pydirectinput.moveTo(x, y)

            pydirectinput.click()
            return True
        return False

    find_img()
