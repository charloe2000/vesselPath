import random
from cv2 import cv2
import config as cfg
import numpy as np

class Location:

    def __init__(self):
        pass

    def get_cur_loc(self, cur_img):
        # cur_img = cv2.imread('images/cur_img.jpg')
        # cur_img = cv2.resize(cur_img ,(cfg.image_width, cfg.image_height), interpolation = cv2.INTER_AREA)
        # 转换到hsv空间
        img_hsv = cv2.cvtColor(cur_img, cv2.COLOR_BGR2HSV)
        # route mask
        mask = cv2.inRange(img_hsv, cfg.head_lower_color, cfg.head_upper_color)
        # cv2.imshow("mask", mask)
        points = [(0, 0)]
        for i in range(0, cfg.image_height):
            for j in range(0, cfg.image_width):
                if (mask[i, j] > 0):
                    points.append((i, j))
        location = np.array(points).mean(axis=0)
        location = tuple((int(location[1]), int(location[0])))
        return location
    

# location = Location()
# location.get_cur_loc()