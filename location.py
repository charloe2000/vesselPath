import random

class Location:

    def __init__(self):
        pass

    def get_cur_loc(self):
        random_x = int(random.random() * 400)
        random_y = int(random.random() * 400)
        loc = (random_x, random_y)
        return loc