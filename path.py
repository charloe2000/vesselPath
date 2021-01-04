"""
先把图像中的绿色路径提出出来，然后腐蚀，得到腐蚀后的路径
"""
from cv2 import cv2
import config as cfg
import numpy as np

img_path = cv2.imread("images/path/path1.png")
img_origin = cv2.imread("images/origin.png")
img_origin = cv2.resize(img_origin ,(cfg.image_width, cfg.image_height), interpolation = cv2.INTER_AREA)
img_path = cv2.resize(img_path ,(cfg.image_width, cfg.image_height), interpolation = cv2.INTER_AREA)
img_hsv = cv2.cvtColor(img_path, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(img_hsv, cfg.lower_color, cfg.upper_color)
# 把绿色区域画出来
res = cv2.bitwise_or(img_path , img_path, mask=mask)
cv2.imshow("res_before", res)
kernel = np.ones((5,5),np.uint8)
# 腐蚀白色掩模
mask = cv2.erode(mask, kernel, iterations = 1)

# 腐蚀后的路径
res = cv2.bitwise_or(img_path , img_path, mask=mask)
result = res + img_origin
cv2.imshow("origin", img_origin)
cv2.imshow("path", img_path)
cv2.imshow("res_after", res)
cv2.imshow("result_after", result)
cv2.waitKey()
cv2.destroyAllWindows() 
