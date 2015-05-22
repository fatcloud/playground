import cv2
import numpy as np
from cam import MyCam
from screen_finder import ScreenFinder


def find_red_point(image, threshold):
    """ignore white stuff, find one single red point"""
    ret, mask = cv2.threshold(image[:,:,2], 127, 255, cv2.THRESH_BINARY)

    
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(image[:,:,2])
    if maxVal > threshold: return maxLoc
    
    return None

if __name__ == '__main__':
    sf = ScreenFinder()
    cam = MyCam()
    cam.size = (640, 480)
    
    screen_img = cv2.imread('seabunny800.png', 0)
    screen_shape = screen_img.shape
    sf.set_screen_img(screen_img)
    
    black = np.full(screen_shape, 0, dtype=np.uint8)
    while True:
        cam_img = cam.read()
        
        while not sf.screen_is_found:
            cv2.imshow('main', screen_img)
            cam_img = cam.read()
            sf.find_screen_img(cam_img)
            cv2.imshow('Type \'r\' to search for the screen', sf.draw_screen_boundary(cam_img))
            k = cv2.waitKey(5)
            if k == 27:
                break
        
        cv2.destroyWindow('Type \'r\' to search for the screen')
        
        top_view = sf.find_top_view(cam_img)
        cv2.imshow('top view', top_view)
        
        cv2.imshow('main', black)
        
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(top_view[:,:,2])
        dst = cv2.adaptiveThreshold(top_view[:,:,2], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 15)
        
        cv2.imshow('dst', dst)
        
        center = None
        if center is not None:
            cv2.circle(black, center, 30, (200,200,200))
        
        
        k = cv2.waitKey(5)
        if k == 27:
            break
        elif k == ord('r'):
            sf.clear_found()