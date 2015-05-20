from cv2 import *
import numpy as np
from motion_detect import MotionDetector
from cam import MyCam
from find_polygons import find_polygons, draw_oriented_polylines


class ScreenFinder(object):
    """This class find the location of the screen by checking
    if there is a quadrangle area that varies with respect to time"""

    def __init__(self, depth=2):
        self.screens = None
        self.screen_size = None
        self._md = None
        self._mapping_matrix = None
        self.screen_shape
        
    def put_cam_img(self, cam_img):
    
        if self._md is None:
            self._md = MotionDetector(N=2, shape=cam_img.shape)
    
        self._md.feed_image(cam_img.copy())
        
        gray_diff = cvtColor(self._md.diff, COLOR_BGR2GRAY)
        quadrangles = find_polygons(gray_diff, 4, 0.1, 1000, True, 10)
        
        if quadrangles != []:
            # The camera is probably not synchronized with display
            self.screens = quadrangles
    
    
    def calibrate(self):
        
        if self.screens is None:
            return
        
        w, h = screen_shape
            
        src_pts = self.screens[0].astype(np.float)
        h, w = screen_img.shape[0], screen_img.shape[1]
        dst_pts = np.array([[0, 0], [0, h], [w, h], [w, 0]], dtype=np.float)
        self._mapping_matrix, mask = findHomography(src_pts, dst_pts, RANSAC, 5.0)
    
    def findTopView(self, cam_img):
        
        
        # transform the point and 
        #dst = perspectiveTransform(laser_pts,M)
        img = warpPerspective(cam_img, M, (w, h))
        return 
    
    def find_laser_spots(self, screen_img, cam_img):
        # find location of green/red spots on camera image
        
        
        # find the transform matrix from camera image to screen
        src_pts = self.screens[0].astype(np.float)
        h, w = screen_img.shape[0], screen_img.shape[1]
        dst_pts = np.array([[0, 0], [0, h], [w, h], [w, 0]], dtype=np.float)
        M, mask = findHomography(src_pts, dst_pts, RANSAC, 5.0)
        
        # transform the point and 
        #dst = perspectiveTransform(laser_pts,M)
        img = warpPerspective(cam_img, M, (w, h))
        img = Canny(img[:,:,2], 50, 100)
        imshow('img', img)
        
        
        
    def reset(self):
        self.screens = None
            
    def find(self):
        pass


if __name__ == '__main__':
    
    from random import randint
    win_size = (600, 800, 3)

    cam = MyCam()
    sf = ScreenFinder()
    
    black = np.full(win_size, (0, 0, 0), np.uint8)
    
    while True:
        k = waitKey(5)
        if k == 27:
            break
        if k == ord('r'):
            sf.reset()
        
        cam_img = cam.read()
        on = True
        while sf.screens is None:
            
            on = not on
            x = on * 255
            img = np.full(win_size, (x, x, x), np.uint8)
            imshow('main', img)
            
            cam_img = cam.read()
            sf.put_cam_img(cam_img)
            k = waitKey(5)
            
        spots = sf.find_laser_spots(black, cam_img)
        
        for rect in sf.screens:
            draw_oriented_polylines(cam_img, rect, 0, (0, 0, 255), 3)
        
        
        imshow('main', black)
        imshow('screen finder', cam_img)
            
        
        