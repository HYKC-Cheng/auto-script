from paddleocr import PaddleOCR, draw_ocr
import json
from loguru import logger

# ocr推理模型
# 模型下载链接 https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md
det_model_dir = 'model/det'  # 文本检测模型
rec_model_dir = 'model/rec'  # 文本识别模型
cls_model_dir = 'model/cls'  # 文本角度模型

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="ch",
    det_model_dir=det_model_dir,
    rec_model_dir=rec_model_dir,
    cls_model_dir=cls_model_dir,
    show_log=False,
    use_gpu=False,
    enable_mkldnn=True,  # 是否启用 MKL-DNN 加速（仅 CPU）
    return_word_box=False)


def getOCR(imgPath: str) -> list:
    """获取图片中的文字

    Args:
        imgPath (str): 图片路径

    Returns:
        list: 返回文字的坐标
    """
    return ocr.ocr(imgPath, cls=False)


def getTargetPosition(img, target: str) -> list:
    """获取图片中的文字

    Args:
        img: 识别图片
        target (str): 目标文字

    Returns:
        position: 返回文字的坐标
        wordList: 返回文字的内容
    """

    ocrResult = ocr.ocr(img, cls=False)
    # ocrResult转换为json并保存为test.json
    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(ocrResult, f, ensure_ascii=False, indent=4)

    position = []
    wordList = []

    if len(ocrResult) == 0 or ocrResult[0] == None:
        return position

    for res in ocrResult:
        for line in res:
            if target in line[1][0]:
                logger.debug(f"识别结果 {line[1]}")
                position.append(line[0])
                wordList.append(line[1][0])

    return position, wordList
