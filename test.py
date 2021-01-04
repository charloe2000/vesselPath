from cv2 import cv2
import config as cfg

img = cv2.imread("images/path/path2.png")
img = cv2.resize(img ,(cfg.image_width, cfg.image_height), interpolation = cv2.INTER_AREA)
cv2.imshow("img", img)
cv2.waitKey()