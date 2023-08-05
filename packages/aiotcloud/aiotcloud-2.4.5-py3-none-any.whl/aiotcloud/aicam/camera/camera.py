#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：esp_server.py
import cv2 
import logging
import numpy as np
from aiotcloud.aicam.file import read
from aiotcloud.aicam.camera.esp_server import EspCam
from aiotcloud.aicam import tools

class AiCam:
    ORIGIN_CAM = 0
    WEB_MJPEG = 1
    ESP_CAM = 2

    COLOR_GRAY=0
    COLOR_COLOR=1
    def __init__(self,protocol=ORIGIN_CAM,params_file=None,color=COLOR_GRAY):
        self.protocal = protocol
        self.params = None
        self.color = color
        if params_file is not None:
            config = read.yaml_read(params_file)
            dist = np.array(config['dist']).reshape((1,5))
            mtx = np.array(config['matrix']).reshape((3,3))
            self.params = {"dist": dist, "mtx": mtx}
            logging.info("load camera params success:"+params_file)

    def connect(self, address=0):
        self.address = address
        if self.protocal == AiCam.WEB_MJPEG:
            self.camera = cv2.VideoCapture(self.address)
            if self.camera.isOpened():
                return True
        elif self.protocal == AiCam.ESP_CAM:
            self.camera = EspCam()
        else:
            raise(TypeError("没有找到相关协议"))

    
    def is_connected(self):
        return self.camera.isOpened()


    def get_picture(self):
        ret,frame =  self.camera.read()
        if ret:
            if self.color == AiCam.COLOR_GRAY:
                return cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) 
            return frame
        else:
            return False

    def show(self,picture,name="picture",long=1):
        cv2.imshow(name,picture)
        key = cv2.waitKey(long) & 0xFF
        return key

    def disconnct(self):
        if self.protocal == AiCam.ESP_CAM:
            tools.stop_thread(self.camera)
        else:
            self.camera.release()
