"""
route class
计算路线
"""
from cv2 import cv2
import config as cfg
import numpy as np


class Route:
    def __init__(self, img_origin_path, img_route_path):
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
        # 存储路线取样点(x, y)
        self.route_points = []
        self.route_points.append(cfg.head_point)

    def show(self):
        #route_pure = cv2.bitwise_or(self.img_route, self.img_route, mask=self.mask)
        self.compute_route()
        for i in range(len(self.route_points)):
            cv2.circle(self.img_route, self.route_points[i], 2, (255, 0, 0), -1)
        cv2.imshow("route", self.img_route)
        cv2.waitKey()

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
    
    def honrizital_line(self, point):
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
        当切线斜率为无穷大时，用此方法计算出的切线方程存在问题。
        但无穷大的斜率在少数情况下才会发生
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
        return p
          
    def draw_tangant(self, img, point, k):
        """
        在图像上绘制point的切线
        """
        first_point = [0, 0]
        first_point[0] = int(point[0] + cfg.tangent_length * 0.5) 
        #first_point[1] = int(first_point[0] * p[0] + p[1])
        first_point[1] = int(point[1] + cfg.tangent_length * 0.5 * k)
        second_point = [0, 0]
        second_point[0] = int(point[0] - cfg.tangent_length * 0.5)
        #second_point[1] = int(second_point[0] * p[0] + p[1])
        second_point[1] = int(point[1] - cfg.tangent_length * 0.5 * k)
        cv2.line(img, tuple(first_point), tuple(second_point), (255, 0, 0), 2)
        
    def compute_route(self):
        """
        以一定的方法，在mask标明的路线上取样点
        """
        cur_point = cfg.head_point
        last_k = -1
        direction = 1
        count = 60

        while True:
            [up_point, down_point] = self.vertical_line(cur_point)
            [left_point, right_point] = self.honrizital_line(cur_point)
            #cv2.line(self.img_route, up_point, down_point, (0, 0, 255), 1)
            #cv2.line(self.img_route, left_point, right_point, (0, 0, 255), 1)
            #cv2.imshow("line", self.img_route)

            points = [up_point, down_point, left_point, right_point]
            # 每个点的切线方程系数
            ps = []
            for i in range(len(points)):
                p = self.tangent_line(points[i])
                ps.append(p)
        
            # 找出最接近的两个切线斜率
            #min = abs(ps[0][0] - ps[1][0])
            #m = 0
            #n = 1
            #for i in range(len(ps)):
            #    for j in range(len(ps)):
            #        cur = abs(ps[i][0] - ps[j][0])
            #    if i!=j and cur < min:
            #        min = cur
            #        m = i
            #        n = j
            #k = (ps[m][0] + ps[n][0]) / 2
            #b = (ps[m][1] + ps[n][1]) / 2
            vertical_k_delta = ps[0][0] - ps[1][0]
            honrizital_k_delta = ps[2][0] - ps[3][0]
            if abs(vertical_k_delta) < abs(honrizital_k_delta):
                k = (ps[0][0] + ps[1][0]) / 2
            else:
                k = (ps[2][0] + ps[3][0]) / 2
            if count <= 5:
                img = self.img_route.copy()
                self.draw_tangant(img, cur_point, k)
                cv2.line(img, up_point, down_point, (0, 0, 255), 1)
                cv2.line(img, left_point, right_point, (0, 0, 255), 1)
                cv2.imshow("qiexian" + str(count), img)
                print(count, "p", ps, "k", k)

            # 确定下一个点
            if last_k * k < 0 and abs(last_k * k) > 1:
                # 改变方向
                direction *= -1             
            next_x = int(round((cur_point[0] + cfg.sampling_distance * direction)))
            #next_y = int(round(next_x * k + b))
            next_y = int(round((cur_point[1] + cfg.sampling_distance * direction * k)))
            last_k = k
            cur_point = (next_x, next_y)
            # 结束
            count = count - 1
            if count < 1:
                break
            self.route_points.append(cur_point)
        
        





