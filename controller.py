import route
import location
from cv2 import cv2

class Controller:

    def __init__(self):
        """
        初始化Route和Location
        """
        self.route = route.Route("images/origin.png", "images/path/path3.png", 
            "jsons/path3.json")
        self.destination_loc = self.route.next_loc()
        self.location = location.Location()
        self.current_loc = self.location.get_cur_loc()
    
    def compute_delta(self):
        """
        计算目标点和当前位置的差值
        """
        delta_x = self.destination_loc[0] - self.current_loc[0]
        delta_y = self.destination_loc[1] - self.current_loc[1]
        delta = (delta_x, delta_y)
        return delta
    
    def start(self):
        """
        对一个当前位置来说，这个位置应该与哪个目标点进行比较？
        """

        print(self.compute_delta())
        count = 300
        while(not self.route.is_finish() and count > 0):
            count -= 1
            self.destination_loc = self.route.next_loc()
            self.current_loc = self.location.get_cur_loc()
            print(self.compute_delta())
            cv2.waitKey(100)
        print('Done!')
        return


controller = Controller()
controller.start()