#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy as np

def _hf_line(img,minLineLength=300, maxLineGap=40):
    """
      cv2.HoughLinesP
          作用：标准霍夫线变换， 找到图像中的所有直线
          参数：
              1 二值图
              2 半径精度
              3 角度精度
              4 最短检测长度
              5 允许的最大缺口
          返回：
              一个列表，每一项是一个四元组，分别是直线两个端点的坐标
      """
    lines = cv2.HoughLinesP(img, 1, np.pi/180, 10, minLineLength, maxLineGap)
    # lines = cv2.HoughLines(img, 1, np.pi/2, 1, minLineLength, maxLineGap)
    return lines

#局部阈值
def local_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  #把输入图像灰度化
    #自适应阈值化能够根据图像不同区域亮度分布，改变阈值
    binary =  cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 25, 10)
    kernel = np.ones((5, 5), np.uint8)
    # kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return binary

def detect(img):
    # 转为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    dst = cv2.dilate(dst, None, iterations=2)
    edges = cv2.Canny(dst, 50, 100)
    lines = _hf_line(edges)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                # 在图片上画直线
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
    return img, edges, lines


def detect_black(picture):
    gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # 膨胀，白区域变大
    dst = cv2.dilate(dst, None, iterations=2)
    # # 腐蚀，白区域变小
    # dst = cv2.erode(dst, None, iterations=6)
    result = _hf_line(dst)
    return result, dst