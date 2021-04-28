import route
from cv2 import cv2
from controller import Controller
import numpy as np



def generate_home(paths):
    back_img = np.zeros((300, 800, 3), np.uint8)
    count = 0
    for path in paths:
        img = cv2.imread(path)
        img = cv2.resize(img ,(200, 200), interpolation=cv2.INTER_AREA)
        back_img[50: 250, 50 + 250 * count: 250 + 250 * count] = img
        name = path.split('/')[-1].split('.')[0]
        cv2.putText(back_img, name, (120 + 250 * count, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        count += 1
        if count >= 3:
            break
    return back_img

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


origin = 'images/origin.png'
paths = ['images/path/path1-1.png', 'images/path/path1.png', 'images/path/path2.png', 'images/path/path3.png']
jsons = ['jsons/path1-1.json', 'jsons/path1.json', 'jsons/path2.json', 'jsons/path3.json']
# choice = None
# (45, 45), (225, 200)
# (300, 45), (500, 200)
# (560, 45), (750, 200)
img_home = generate_home(paths)
cv2.namedWindow('home')
cv2.setMouseCallback('home', choose_path)
while (10):
    cv2.imshow('home', img_home)        
    if cv2.waitKey() & 0xFF == 27:
        break

cv2.destroyWindow('home')