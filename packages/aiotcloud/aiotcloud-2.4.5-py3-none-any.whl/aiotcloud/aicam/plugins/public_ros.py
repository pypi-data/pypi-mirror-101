#!/usr/bin/python3
#-*- coding:UTF-8 -*-

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class ImagePublisher:
    def __init__(self,name="aicam_publisher",topic="/aicam/raw"):
        rospy.init_node(name, anonymous=True)
        self.pub = rospy.Publisher(topic, Image)
        self.bridge = CvBridge()


    def convertmag(self,img):
        return self.bridge.cv2_to_imgmsg(img, encoding="passthrough")


    def publish(self,img):
        self.pub.publish(self.convertmag(img))

