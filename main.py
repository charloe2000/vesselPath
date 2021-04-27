import route
from cv2 import cv2
from controller import Controller

img_home = cv2.imread('images/home.png')
origin = 'images/origin.png'
paths = ['images/path/path1.png', 'images/path/path2.png', 'images/path/path3.png']
jsons = ['jsons/path1.json', 'jsons/path2.json', 'jsons/path3.json']
# choice = None
# (45, 45), (225, 200)
# (300, 45), (500, 200)
# (560, 45), (750, 200)

def choose_path(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and 45 < y < 200:
        # path1
        if 45 < x < 225:
            Controller(origin, paths[0], jsons[0]).start()         
        # path2
        elif 300 < x < 500:
            Controller(origin, paths[1], jsons[1]).start()
        # path3
        elif 560 < x < 750:
            Controller(origin, paths[2], jsons[2]).start()

cv2.namedWindow('home')
cv2.setMouseCallback('home', choose_path)
while (10):
    cv2.imshow('home', img_home)        
    if cv2.waitKey() & 0xFF == 27:
        break

cv2.destroyWindow('home')