import cv2
import pygetwindow as gw
import pyautogui


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


def getScreenShot(handle: str = None):
    """
    获取屏幕截图

    Args:
        handle (str, optional): 窗口句柄 Defaults to None.

    Returns:
        _type_: 截屏数据
    """

    # 如果有句柄，先激活对应句柄窗口
    if handle:
        gw.getWindowsWithTitle(handle)[0].activate()

    # 获取当前活动窗口
    active_window = gw.getActiveWindow()

    # 获取窗口的位置和大小
    x, y, width, height = active_window.left, active_window.top, active_window.width, active_window.height

    # 截取屏幕截图
    return pyautogui.screenshot(region=(x, y, width, height))


import cv2


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

    # 读取图像
    image = cv2.imread(img)

    # 裁剪指定区域的图像
    cropped_image = image[y:y + height, x:x + width]

    return cropped_image
