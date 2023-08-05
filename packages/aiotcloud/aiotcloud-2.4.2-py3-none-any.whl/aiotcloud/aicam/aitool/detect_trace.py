#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import math
import numpy as np


#全局阈值
def global_threshold(gray):
    # gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  #把输入图像灰度化
    #直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    print("threshold value %s"%ret)
    return binary

#局部阈值
def local_threshold(gray):
    # gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)  #把输入图像灰度化
    #自适应阈值化能够根据图像不同区域亮度分布，改变阈值
    binary =  cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 25, 10)
    kernel = np.ones((9, 9), np.uint8)
    erosion = cv2.erode(binary, kernel, iterations=1)
    # erosion = cv2.dilate(erosion, kernel, iterations=1)
    return erosion


def get_lines(img,size=2):
    h,w = img.shape
    lines = []
    for d in range(int(h/(size+1)),h-size,int(h/(size+1))):
        roi = img[d:d+1,0:w]
        lines.append((roi,d))
    return lines

def get_points(lines):
    result = []
    for l,x in lines:
        left,right = 0,0
        count = 0
        l = l[0]
        len_l = len(l)
        for i in range(len_l):
            if l[i]==0:
                count += 1
            elif l[i]==255:
                if count > 0:
                    count = 0
                    if left == 0:
                        left = i
                    else:
                        right = i

        if left == 0 or right == 0:
            right = x

        if left != 0 and right != 0:
            result.append((int((left+right)/2),x))
    return result


def draw_lines(ret,lines):
    for i in range(len(lines)-1):
        (x1,y1),(x2,y2) = lines[i],lines[i+1]
        ret = cv2.line(ret,(x1,y1),(x2,y2),(0,0,0),8)
    return ret


def decide(lines,percent=0.5,w=480):
    if len(lines) == 0: return "fail"
    left ,cennter, right = 0, 0, 0
    for line,_ in lines:
        min = 0.5*w*(1-percent)
        max = 0.5*w*(1+percent)
        if line < min: left += 1
        elif line > max: right += 1
        else: cennter += 1
    if left>cennter and left>right: return "left"
    if cennter>left and cennter>right: return "center"
    if right>cennter and right>left: return "right"
    if right==cennter==left: return "center"

def detect(img,size=2,percent=0.35):
    edges = local_threshold(img)
    lines = get_lines(edges, size=size)
    lines = get_points(lines)
    return draw_lines(img, lines), edges, decide(lines,percent,w=img.shape[1])
