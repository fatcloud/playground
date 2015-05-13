from cv2 import *
import numpy as np
from cam import MyCam


def find_polygons(image_in, edge_num, tolerance=0.1, area_threshold=100, convex_only=True):
    """find contours that appears to be a """
    img = image_in.copy()
    lo, hi = 100, 150
    
    edge = Canny(img, lo, hi)
    # imshow('edge', edge)
    thresh1, dst = threshold(edge,127,255,THRESH_BINARY)
    # imshow('thresh', dst)
    ctr, hry = findContours(dst, RETR_TREE, CHAIN_APPROX_SIMPLE)
    imshow('fndctr', dst)
    
    if hry is None: return img
    hry = hry[0]
    
    squares = []
    for cnt in ctr:
        
        # kill the contour if it doesn't look like a square
        epsilon = tolerance*arcLength(cnt,True)
        tmp = approxPolyDP(cnt,epsilon,True)
        
        if len(tmp) != edge_num: continue
        if convex_only and not isContourConvex(tmp): continue 
        if contourArea(tmp) < area_threshold: continue
        squares.append(cnt)
        
        
    return squares
    
if __name__ == "__main__":
    cam = MyCam()
    while True:
        img = cam.read()
        polygons = find_polygons(img, 4)
        for ctr in polygons:
            drawContours(img, [ctr], 0, (0,0,255), 2)
        imshow('find quadrangles',img)
        k = waitKey(5)
        if k == 27:
            break