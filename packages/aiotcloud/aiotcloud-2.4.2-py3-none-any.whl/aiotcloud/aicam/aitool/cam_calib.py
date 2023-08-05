#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：esp_server.py
import cv2
import numpy as np
import threading
from queue import Queue
import aiotcloud
from aiotcloud.aicam import tools
from aiotcloud.aicam.file import save
from shutil import copyfile
import sys

def calibkd(queue,h,w):
    print("start calibkd",h,w)
    font = cv2.FONT_HERSHEY_SIMPLEX #font
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)
    objp = np.zeros((h * w, 3), np.float32)
    objp[:, :2] = np.mgrid[0:h, 0:w].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
    obj_points = []  # 存储3D点
    img_points = []  # 存储2D点
    length = 0
    while True:
        img = queue.get()
        while queue.qsize()>0:
            img = queue.get()
        gray = img
        size = gray.shape[::-1]
        ret, corners = cv2.findChessboardCorners(gray, (h, w), None)
        if ret:
            cv2.drawChessboardCorners(img, (h, w), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值
        cv2.imshow('calibkd', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') and ret:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
            print(type(corners2))
            if [corners2]:
                img_points.append(corners2)
            else:
                img_points.append(corners)
            cv2.waitKey(300)
            length += 1
        elif length > 3:
            break

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)
    print("ret:",ret)
    print("mtx:", mtx.flatten().tolist()) # 内参数矩阵
    print("dist:", dist.flatten().tolist())  # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
    save.yaml_save({"ret":ret,"matrix":mtx.flatten().tolist(),"dist":dist.flatten().tolist()})
    # print("rvecs:\n", rvecs)  # 旋转向量  # 外参数
    # print("tvecs:\n", tvecs ) # 平移向量  # 外参数
    cv2.destroyAllWindows()


def calib_from_queue(queue,h=7,w=10):
    t = threading.Thread(target=calibkd, args=(queue,h,w))
    t.start()



def calib_cam(cam,h=7,w=10):
    queue = Queue()
    t = threading.Thread(target=calibkd, args=(queue, h, w))
    t.start()
    while t.is_alive():
        frame = cam.get_picture()
        if frame is not False:
            queue.put(frame)
    tools.stop_thread(t)


def get_calibboard():
    path = aiotcloud.__file__
    path = path[:path.rfind("/")]+"/aicam/data/calib.io_checker_A4_8x11_20.pdf"
    try:
        copyfile(path,"calib.io_checker_A4_8x11_20.pdf")
        print("生成标定板成功，标定板大小8*11个方格，每个方格边长20mm，请使用A4一比一打印，不要页边距。标定板文件为当前目录：calib.io_checker_A4_8x11_20.pdf")
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)
