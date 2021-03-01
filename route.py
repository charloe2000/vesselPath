"""
route class
计算路线
"""
from cv2 import cv2
import config as cfg
import numpy as np
import json

class Route:
    def __init__(self, img_origin_path, img_route_path, img_route_json):
        """
        img_orgin_path: 黑白图的文件路径
        img_route_path: 标有路线的黑白图的文件路径
        """
        img_origin = cv2.imread(img_origin_path)
        img_route = cv2.imread(img_route_path)
        # 拉伸大小
        self.img_origin = cv2.resize(img_origin ,(cfg.image_width, cfg.image_height), interpolation = cv2.INTER_AREA)
        self.img_route = cv2.resize(img_route ,(cfg.image_width, cfg.image_height), interpolation = cv2.INTER_AREA)
        # 转换到hsv空间
        img_route_hsv = cv2.cvtColor(self.img_route, cv2.COLOR_BGR2HSV)
        # route mask
        self.mask = cv2.inRange(img_route_hsv, cfg.lower_color, cfg.upper_color)
        # 腐蚀
        # kernel = np.ones((5,5),np.uint8)
        # self.mask = cv2.erode(mask, kernel, iterations = 1)
        # 从json文件中读取开始点和结束点
        self.read_route_json(img_route_json)

        self.cur_point = self.start_point
        self.last_k = -1
        self.direction = 1
        self.is_finish_ = False
        # cv2.imshow("origin", self.img_origin)
    
    def read_route_json(self, img_route_json):
        """
        从json文件中读取开始点和结束点
        """
        with open(img_route_json, 'r') as fp:
            data = json.load(fp)
            self.start_point = (data["start_x"], data["start_y"])
            self.end_point = (data["end_x"], data["end_y"])

    def is_finish(self):
        return self.is_finish_

    def show(self):
        cv2.imshow("route", self.img_origin)
        # cv2.waitKey()
    
    def get_route_img(self):
        return self.img_origin

    def vertical_line(self, point):
        """
        以该点作垂直线，返回垂直线与路线mask的交点
        """
        [x, y] = point
        # 计算上交点
        for i in range(y, -1, -1):
            if self.mask[i, x] == 0:
                up_point = (x, i)
                break
        # 计算下交点
        for i in range(y, cfg.image_height):
            if self.mask[i, x] == 0:
                down_point = (x, i)
                break
        return up_point, down_point
    
    def horizontal_line(self, point):
        """
        以该点作水平线，返回水平线与路线mask的交点
        """
        [x, y] = point
        # 计算左交点
        for i in range(x, -1, -1):
            if self.mask[y, i] == 0:
                left_point = (i, y)
                break
        # 计算右交点
        for i in range(x, cfg.image_width):
            if self.mask[y, i] == 0:
                right_point = (i, y)
                break
        return left_point, right_point

    def is_border(self, point):
        """
        检查它的九宫格，判断一个点在mask上是否是边界点
        """
        neibor = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for i in range(len(neibor)):
            if self.mask[point[1], point[0]] ^ self.mask[point[1]+neibor[i][1], point[0]+neibor[i][0]] != 0:
                return True
        return False

    def tangent_line(self, point):
        """
        在mask上计算point的切线
        当切线斜率为无穷大或0时，计算出的结果都是0
        """
        [x, y] = point
        border_x = []
        border_y = []
        half_size = int(cfg.tangent_size / 2)
        for j in range(y-half_size, y+half_size+1):
            for i in range(x-half_size, x+half_size+1):
                if(self.is_border((i, j))):
                    border_x.append(i)
                    border_y.append(j)
        
        p = np.polyfit(np.array(border_x), np.array(border_y), 1)
        return p[0]
          
    def draw_tangant(self, img, point, k):
        """
        在图像上绘制point的切线
        """
        first_point = [0, 0]
        first_point[0] = int(point[0] + cfg.tangent_length * 0.5) 
        first_point[1] = int(point[1] + cfg.tangent_length * 0.5 * k)
        second_point = [0, 0]
        second_point[0] = int(point[0] - cfg.tangent_length * 0.5)
        second_point[1] = int(point[1] - cfg.tangent_length * 0.5 * k)
        cv2.line(img, tuple(first_point), tuple(second_point), (255, 0, 0), 2)
        
    def compute_xy(self, k):
        """
        计算出k后，依据上一个计算的last_k以及direction等，计算出下一个点的位置
        计算结果保存在self.last_k和self.cur_point中
        """
        if abs(self.last_k) < 1e-6 and abs(k) > 0.5:
            # 改变方向
            self.direction *= -1             
        next_x = int(round((self.cur_point[0] + cfg.sampling_distance * self.direction)))
        if abs(k) < 1e-6:
            next_y = self.cur_point[1] - cfg.sampling_distance
        else:
            next_y = int(round((self.cur_point[1] + cfg.sampling_distance * self.direction * k)))
        self.last_k = k
        self.cur_point = [next_x, next_y]      

    def next_loc(self, debug=False):
        """
        获取下一个规划点
        """

        # 作水平线和垂直线
        [up_point, down_point] = self.vertical_line(self.cur_point)
        [left_point, right_point] = self.horizontal_line(self.cur_point)
        # debug 将水平线和垂直线画出来
        if debug:
            img = self.img_origin.copy()
            cv2.line(img, up_point, down_point, (0, 0, 255), 2)
            cv2.line(img, left_point, right_point, (0, 0, 255), 2)
            cv2.imshow("debug", img)

        # 获取每个交点的斜率
        points = [up_point, down_point, left_point, right_point]
        ps = []
        for i in range(len(points)):
            p = self.tangent_line(points[i])
            ps.append(p)
        
        # 确定前进的斜率
        vertical_k_delta = ps[0]- ps[1]
        honrizital_k_delta = ps[2] - ps[3]
        if abs(vertical_k_delta) < abs(honrizital_k_delta):
            k = (ps[0] + ps[1]) / 2
        else:
            k = (ps[2] + ps[3]) / 2

        
        # 确定下一个点
        self.compute_xy(k)

        # 对(x, y)进行修正
        [up_point, down_point] = self.vertical_line(self.cur_point)
        [left_point, right_point] = self.horizontal_line(self.cur_point)
        vertical_length = abs(up_point[1] - down_point[1])
        honrizital_length = abs(left_point[0] - right_point[0])
        if vertical_length < honrizital_length:
            self.cur_point[1] = up_point[1] + int(round(vertical_length / 2))
        else:
            self.cur_point[0] = left_point[0] + int(round(honrizital_length / 2))
        
        # 绘制到图像上
        cv2.circle(self.img_origin, tuple(self.cur_point), 2, (0, 255, 0), -1)
        # 是否到终点
        if abs(self.cur_point[0]-self.end_point[0])+abs(self.cur_point[1]-self.end_point[1]) <= 3:
            self.is_finish_ = True
        
        # debug 将确定的切线画出来
        if debug:
                self.draw_tangant(img, self.cur_point, k)
                cv2.imshow("debug", img)
                cv2.waitKey(100)
                #print("p", ps, "k", k, "direction", self.direction)
        
        return self.cur_point
            
        
        





