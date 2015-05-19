from cv2 import *
import numpy as np
from cam import MyCam
from time import time

def draw_oriented_polylines(img, pts, is_closed, color_start, thickness=1, color_end=(0,0,0)):
    img_out = img
    if len(img.shape) == 2:
        img_out = cvtColor(img_out, COLOR_GRAY2BGR)
    
    cs, ce = color_start, color_end
    n = len(pts)
    for idx, pt in enumerate(pts):
    
        if idx == n and not is_closed: break
    
        next_pt = pts[(idx + 1) % n]
        next_pt = (next_pt[0, 0], next_pt[0, 1])
        pt = (pt[0, 0], pt[0, 1])
        
        color = ((cs[0]*(n-idx) + ce[0]*idx) / n,\
                 (cs[1]*(n-idx) + ce[1]*idx) / n,\
                 (cs[2]*(n-idx) + ce[2]*idx) / n)
        line(img_out, pt, next_pt, color, thickness)
            

def find_polygons(gray_image_in, edge_num, tolerance=0.1, area_threshold=100, convex_only=True, edge_threshold=60):
    """find contours that appears to be a """
    img = gray_image_in.copy()
    lo, hi = 100, 150
    
    # imshow('img', img)
    edge = Canny(img, lo, hi)
    # imshow('edge', edge)
    thresh1, dst = threshold(edge,edge_threshold,255,THRESH_BINARY)
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
        
        # now sort the points in counter clock wise so we can eliminate similar solutions
        if np.cross(tmp[1] - tmp[0], tmp[2] - tmp[1])[0] > 0:
            tmp = np.flipud(tmp)
        
        # distance_from_origin = map(lambda pt: pt[0,0] ** 2 + pt[0,1] ** 2, tmp)
        # val, idx = min((val, idx) for (idx, val) in enumerate(distance_from_origin))
        
        # up, down = np.vsplit(tmp, idx)
        # tmp = np.vstack(down, up)
        # print tmp
        polygons.append(tmp)
    
    return polygons
    
if __name__ == "__main__":
    cam = MyCam()
    while True:
        img = cam.read()
        polygons = find_polygons(img, 4)
        for ctr in polygons:
            draw_oriented_polylines(img, ctr, 0, (0,0,255), 2, (255,0,0))
        imshow('find quadrangles',img)
        k = waitKey(5)
        if k == 27:
            break