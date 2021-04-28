import numpy as np
from cv2 import cv2

def generate_home(paths):
    back_img = np.zeros((300, 800, 3), np.uint8)
    count = 0
    for path in paths:
        img = cv2.imread(path)
        img = cv2.resize(img ,(200, 200), interpolation=cv2.INTER_AREA)
        back_img[50: 250, 50 + 250 * count: 250 + 250 * count] = img
        name = path.split('/')[-1]
        cv2.putText(back_img, name, (120 + 250 * count, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        count += 1
        if count >= 3:
            break
    return back_img
    


paths = ['images/path/path1-1.png', 'images/path/path1.png', 'images/path/path2.png', 'images/path/path3.png']
back_img = generate_home(paths)
cv2.imshow("back", back_img)
cv2.waitKey()
cv2.destroyAllWindows()