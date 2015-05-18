from cv2 import *
import numpy as np
from cam import MyCam


class ScreenTracker(object):
    """This class find the location of the screen by checking
    if there is a quadrangle area that varies with respect to time"""

    def __init__(self, depth=2):
        self.screens = None
        self._md = None
        
    def update(screen_image):
        # 1. decide what method is best to find this screen_image
        # 2. do all that shit and find the corners

    def find(self):
        pass


if __name__ == '__main__':
    sc = ScreenTracker(MyCam())
    while True:
        sc.