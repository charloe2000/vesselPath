import numpy as np
from cv2 import cv2
from location import Location
import config as cfg

cap = cv2.VideoCapture(2)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    location = Location()
    frame = cv2.resize(frame ,(cfg.image_width, cfg.image_height), interpolation = cv2.INTER_AREA)
    cv2.circle(frame, location.get_cur_loc(frame), 3, (0, 0, 255), -1)
    cv2.imshow('frame', frame)
    if cv2.waitKey(100) & 0xFF == 27:
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()