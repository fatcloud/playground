from cv2 import *
import numpy as np
from cam import MyCam
from time import time

def find_polygons(gray_image_in, edge_num, tolerance=0.1, area_threshold=100, convex_only=True):
    """find contours that appears to be a """
    img = gray_image_in.copy()
    lo, hi = 100, 150
    
    # imshow('img', img)
    edge = Canny(img, lo, hi)
    # imshow('edge', edge)
    thresh1, dst = threshold(edge,60,255,THRESH_BINARY)
    # imshow('thresh', dst)
    ctr, hry = findContours(dst, RETR_TREE, CHAIN_APPROX_SIMPLE)
    # imshow('fndctr', dst)
    
    if hry is None: return []
    hry = hry[0]
    
    polygons = []
    for cnt in ctr:

        # kill the contour if it doesn't look like a square
        cnt = cnt.reshape(-1,2)
        epsilon = tolerance * 2 * ((3.14 * contourArea(cnt)) ** 0.5)
        tmp = approxPolyDP(cnt,epsilon,True)

        if len(tmp) != edge_num: continue
        if convex_only and not isContourConvex(tmp): continue 
        if contourArea(tmp) < area_threshold: continue
        polygons.append(tmp)
    
    return polygons
    
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