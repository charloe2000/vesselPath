import route
from cv2 import cv2

route = route.Route("images/origin.png", "images/path/path2.png")
count = 300
while count > 0 and not route.is_finish():
    #if count <=5:
    #    route.next_loc(debug=True)
    #else:
    #    route.next_loc()
    route.next_loc(debug=True)
    count -= 1
cv2.waitKey()
#route.show()