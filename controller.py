import route
import location
from cv2 import cv2
import numpy as np

class Controller:

    def __init__(self, origin, path, json):
        """
        初始化Route和Location
        """
        self.route = route.Route(origin, path, 
            json)
        self.name = path.split('/')[-1]
        self.destination_loc = self.route.next_loc()
        self.next_destination_loc = self.route.next_loc()
        self.location = location.Location()
        self.current_loc = self.location.get_cur_loc()
    
    def get_next_destionation(self):
        cur_delta = np.square(np.abs(self.destination_loc[0] - self.current_loc[0])) + \
            np.square(np.abs(self.destination_loc[1] - self.current_loc[1]))
        next_delta = np.square(np.abs(self.next_destination_loc[0] - self.current_loc[0])) + \
            np.square(np.abs(self.next_destination_loc[1] - self.current_loc[1]))
        
        if (cur_delta >= next_delta):
            self.destination_loc = self.next_destination_loc
            self.next_destination_loc = self.route.next_loc()
           
    def compute_delta(self):
        """
        计算目标点和当前位置的差值
        """
        delta_x = self.destination_loc[0] - self.current_loc[0]
        delta_y = self.destination_loc[1] - self.current_loc[1]
        delta = (delta_x, delta_y)
        return delta
    
    def paint_delta(self):
        img_route = self.route.get_route_img().copy()
        cv2.line(img_route, tuple(self.current_loc), tuple(self.destination_loc), (0, 255, 255), 2)
        cv2.circle(img_route, tuple(self.current_loc), 3, (0, 0, 255), -1)
        cv2.imshow(self.name, img_route)
    
    def start(self):
        """
        对一个当前位置来说，这个位置应该与哪个目标点进行比较？
        """

        print(self.compute_delta())
        # count = 300
        # while not self.route.is_finish() and count > 0:
        while not self.route.is_finish():
            # count -= 1
            self.get_next_destionation()
            self.current_loc = self.location.get_cur_loc()
            self.paint_delta()
            print(self.compute_delta())
            if cv2.waitKey(100) & 0xFF == 27:
                print('Interrupt!')
                cv2.destroyWindow(self.name)
                return
        print('Done!')
        cv2.waitKey()
        cv2.destroyWindow(self.name)
        return


controller = Controller('images/origin.png', 'images/path/path1-1.png', 'jsons/path1-1.json')
controller.start()