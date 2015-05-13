from cv2 import *
import numpy as np
from motion_detect import MotionDetector
from cam import MyCam
from find_polygons import find_polygons


class ScreenFinder(object):
    """This class find the location of the screen by checking
    if there is a quadrangle area that varies with respect to time"""

    def __init__(self, depth=2):
        self.screens = None
        self._md = None
        
    def put_cam_img(self, cam_img):
    
        if self._md == None:
            self._md = MotionDetector(N=2, shape=cam_img.shape)
    
        self._md.feed_image(cam_img.copy())
        gray_diff = cvtColor(self._md.diff, COLOR_BGR2GRAY)
        
        quadrangles = find_polygons(gray_diff, 4, 0.03, 1000, True, 10)
        
        if quadrangles != []:
            # The camera is probably not synchronized with display
            self.screens = quadrangles

    def find(self):
        pass


if __name__ == '__main__':
    
    from random import randint
    win_size = (300, 300)

    cam = MyCam()
    sf = ScreenFinder()
    
    def r():
        return randint(0, 255)
    
    cam_img = None
    while sf.screens is None:
        
        img = np.full((win_size[0], win_size[1], 3), (r(), r(), r()), np.uint8)
        imshow('BGR', img)
        
        cam_img = cam.read()
        sf.put_cam_img(cam_img)
        imshow('motion', cam_img)
        k = waitKey(5)
        if k == 27:
            break
    
    for rect in sf.screens:
        drawContours(cam_img, [rect], 0, (128, 0, 128), 3)
    
    imshow('motion', cam_img)
    
    waitKey(0)