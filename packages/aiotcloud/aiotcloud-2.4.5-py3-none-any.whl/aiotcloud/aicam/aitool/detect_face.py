'''
Author: 桑欣
Email: sangxin@infore.com
Date: 2021-03-17 19:51:32
LastEditTime: 2021-04-02 15:35:41
LastEditors: 桑欣
Description: 
FilePath: /Sdk-Python/aiotcloud/aicam/aitool/detect_face.py
'''
import face_recognition
import cv2
import random
import numpy as np

def locate(picture):
    """
    定位人脸的位置，返回位置数据
    """
    f_location = face_recognition.face_locations(picture)
    faces = []
    for (top, right, bottom, left) in f_location:
        faces.append(picture[left:top, right:bottom])
        cv2.rectangle(picture, (left, top), (right, bottom), (0, 0, 255), 2)

    return picture,faces,f_location


def face_encode(imgs_path="people/sangxin.png",name="SangXin"):
    '''
    @description: 获取人脸的编码
    @param {参数：图片路径}
    @return {返回人脸编码128*1}
    '''
    total_face_encoding = {}
    temp = face_recognition.face_encodings(face_recognition.load_image_file(imgs_path))
    if len(temp) > 0:
        total_face_encoding[name] = temp[0]
    return total_face_encoding


def face_distance(face_encodings, face_to_compare):
    """
    Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
    for each comparison face. The distance tells you how similar the faces are.

    :param faces: List of face encodings to compare
    :param face_to_compare: A face encoding to compare against
    :return: A numpy ndarray with the distance for each face in the same order as the 'faces' array
    """
    if len(face_encodings) == 0:
        return np.empty((0))
    return np.linalg.norm(face_encodings - face_to_compare, axis=1)

    
def face_compare(picture,location,face_encode,tolerance=0.5):
    '''
    @description: 人脸对比，表示两个人脸的编码
    @param {*}
    @return {*}
    '''
    if len(location)==0:
        return "UnKnow Face"
    face_encodings = face_recognition.face_encodings(picture, location)
    for myencode in face_encodings:
        for k in face_encode.keys():
            match = face_recognition.compare_faces(face_encode[k].reshape(1,128), myencode.reshape(1,128),tolerance=tolerance)
            if True in match:
                return k
    return "UnKnow Face"