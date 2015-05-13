import cv2
import numpy as np
from cam import MyCam


def find_polygons(image_in, edge_num, tolerance=0.02, area_threshold=100, convex_only=True):
    """find contours that appears to be a """
    img = image_in.copy()
    lo, hi = 100, 150
    
    edge = cv2.Canny(img, lo, hi)
    
    thresh1, dst = cv2.threshold(edge,127,255,cv2.THRESH_BINARY)
    
    ctr, hry = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if hry is None: return img
    hry = hry[0]
    
    squares = []
    for cnt in ctr:
        
        # kill the contour if it doesn't look like a square
        epsilon = tolerance*cv2.arcLength(cnt,True)
        tmp = cv2.approxPolyDP(cnt,epsilon,True)
        
        if len(tmp) != edge_num: continue
        if convex_only and not cv2.isContourConvex(tmp): continue 
        if cv2.contourArea(tmp) < area_threshold: continue
        squares.append(cnt)
        
        
    return squares
    
if __name__ == "__main__":
    cam = MyCam()
    while True:
        img = cam.read()
        polygons = find_polygons(img, 4)
        for ctr in polygons:
            cv2.drawContours(img, [ctr], 0, (0,0,255), 2)
        cv2.imshow('find quadrangles',img)
        k = cv2.waitKey(5)
        if k == 27:
            break