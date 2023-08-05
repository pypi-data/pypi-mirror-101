#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：esp_server.py
import cv2
import numpy as np
import threading

import cv2.aruco as aruco
font = cv2.FONT_HERSHEY_SIMPLEX

DICT_ARUCO_ORIGINAL = aruco.DICT_ARUCO_ORIGINAL


def detect(frame, camera_params,size=0.04,code = DICT_ARUCO_ORIGINAL):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(code)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)
    rvec, tvec = None, None
    if ids is not None:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners,size, camera_params['mtx'], camera_params['dist'])
        (rvec-tvec).any() # get rid of that nasty numpy value array error
        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, camera_params['mtx'], camera_params['dist'], rvec[i, :, :], tvec[i, :, :], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
        cv2.putText(frame, str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
    else:
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
    return frame, rvec, tvec
