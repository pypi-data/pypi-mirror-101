#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：esp_server.py
import cv2
import numpy as np
import socket  # 导入 socket 模块
import time
import threading
from queue import Queue


class EspCam(threading.Thread):
    def __init__(self,ip="0.0.0.0",port=8848):
        threading.Thread.__init__(self)
        self.queue = Queue()
        self.server = socket.socket()  # 创建 socket 对象
        self.server.bind((ip, port))  # 绑定端口
        self.server.listen(5)  # 等待客户端连接
        self.start()


    def read(self):
        if self.queue.qsize()>0:
            return True,self.queue.get()
        else:
            return False,None


    def run(self):
        sock, addr = self.server.accept()
        print("接收到来自",addr)
        stream_bytes = b' '
        count = 0
        last_time = time.time()
        while getattr(sock, '_closed') == False:
            stream_bytes += sock.recv(1024)
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')
            if first != -1 and last != -1:
                if last < first:
                    stream_bytes = stream_bytes[last + 2:]
                else:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    nimage = np.frombuffer(jpg, dtype=np.uint8)
                    image = cv2.imdecode(nimage, cv2.IMREAD_COLOR)
                    count += 1
                    while self.queue.qsize() > 0:
                        self.queue.get()
                    self.queue.put(image)
                    if int(time.time() - last_time) >= 2:
                        print("ESP_CAM平均帧率:%s" % str(int(count / (time.time() - last_time))))
                        last_time = time.time()
                        count = 0