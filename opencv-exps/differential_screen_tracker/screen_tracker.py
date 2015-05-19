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

    def find_laser_spots(self, screen_img, cam_img):
        # map cam_img to the same size of screen_img
        # diff the image
        # find green/red spots
        src_pts = self.screens[0]
        
        """
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        
        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        """   
        
    def reset(self):
        self.screens = None
            
    def find(self):
        pass


if __name__ == '__main__':
    
    from random import randint
    win_size = (600, 800, 3)

    cam = MyCam()
    sf = ScreenFinder()
    
    def r(): return randint(0, 255)
    black = np.full(win_size, (0, 0, 0), np.uint8)
    
    while True:
        k = waitKey(5)
        if k == 27:
            break
        if k == ord('r'):
            sf.reset()
        
        cam_img = cam.read()
        while sf.screens is None:
            
            img = np.full(win_size, (r(), r(), r()), np.uint8)
            imshow('main', img)
            
            cam_img = cam.read()
            sf.put_cam_img(cam_img)
            k = waitKey(5)
            
        for rect in sf.screens:
            drawContours(cam_img, [rect], 0, (0, 0, 255), 3)
        
        imshow('main', black)
        imshow('screen finder', cam_img)
            
        
        