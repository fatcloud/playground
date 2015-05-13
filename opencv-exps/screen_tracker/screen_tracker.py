from cv2 import *
import numpy as np
from motion_detect import MotionDetector
from cam import MyCam
from find_polygons import find_polygons

win_size = (300, 300)
if __name__ == '__main__':
    img = np.full((win_size[0], win_size[1], 3), 0, np.uint8)

    m_255 = np.full(win_size, 255, np.uint8)
    m_0 = np.full(win_size, 0, np.uint8)

    img[:,:,0] = m_255[:,:]
    index = 0
    
    cam = MyCam()
    
    md = MotionDetector(N=2, shape=cam.read().shape)
    
    while True:
        
        # turn off the previous bias
        img[:, :, index] = m_0
        
        # now turn on the next
        index = (index + 1) % 3
        img[:, :, index] = m_255
        
        cam_img = cam.read()
        # imshow('cam_img', cam_img)
        md.feed_image(cam_img)
        # imshow('md.diff',md.diff)
        gray_diff = cvtColor(md.diff, COLOR_BGR2GRAY)
        # imshow('',gray_diff)
        # blured = GaussianBlur(gray_diff, (5,5), 0)
        
        # # edges = Canny(gray_diff, 100, 200)
        # _, th = threshold(gray_diff, 80, 255, THRESH_BINARY)
        
        # contours, hry = findContours(th, RETR_TREE, CHAIN_APPROX_SIMPLE)
        
        # screens = []
        # for ctr in contours:
            # epsilon = 0.2*arcLength(ctr,True)
            # tmp = approxPolyDP(ctr,epsilon,True)
            # print len(tmp), contourArea(tmp)
            # if len(tmp) == 4 and contourArea(tmp) > 1000:
                # screens.append(tmp)
        
        quadrangles = find_polygons(gray_diff, 4, 0.01, 1000)
        # th = cvtColor(gray_diff, COLOR_GRAY2BGR)
        # print quadrangles
        c = [0,0,0]
        c[index] = 255
        for ctr in quadrangles:
            drawContours(cam_img, [ctr], 0, (c[0], c[1], c[2]), 3)
        
        imshow('motion', cam_img)
        imshow('BGR', img)
        k = waitKey(5)
        if k == 27:
            break