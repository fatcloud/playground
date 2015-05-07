import cv2
import numpy as np
from cam import MyCam



def detect_square(input):
    img = input.copy()
    lo, hi = 100, 150
    
    edge = cv2.Canny(img, lo, hi)
    thresh1, dst = cv2.threshold(edge,127,255,cv2.THRESH_BINARY)
    
    ctr, hry = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hry = hry[0]
    
    for idx, cnt in enumerate(ctr):
        
        # kill the contour if it doesn't look like a square
        epsilon = 0.02*cv2.arcLength(cnt,True)
        tmp = cv2.approxPolyDP(cnt,epsilon,True)
        
        if len(tmp) != 4: continue
        if not cv2.isContourConvex(tmp): continue 
        if cv2.contourArea(tmp) < 100: continue
        #print tmp
        cv2.drawContours(img, [tmp], 0, (0, 0, 255))
        
    return img
    
if __name__ == "__main__":
    cam = MyCam()
    cam.cam_loop(detect_square)