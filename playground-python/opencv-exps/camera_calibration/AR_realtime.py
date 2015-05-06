"""
usage: >>>python AR_realtime.py

This program tries to detect chessboard from camera image
and draw axis in real-time
"""

import cv2
import numpy as np
import glob
from time import sleep
# Load previously saved data
with np.load('camera_parameters.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

    
print 'data loaded...'


myimg = cv2.imread('phppg.png',-1)
# img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
mask = myimg[:,:,3]
ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
#mask = cv2.blur(mask, (5,5))
mask_inv = cv2.bitwise_not(mask)

cv2.imshow('mask_inv', mask_inv)
def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    
    raws, cols, depth = myimg.shape
    y, x = corner
    w, h, d = myimg.shape
    ww, hh, dd = img.shape
    if x + w > ww: w = ww - x
    if y + h > hh: h = hh - y
    
    roi = img[x: x + w, y: y + h]
    mymy = myimg[:,:,0:3]
    mymy = mymy[0:w, 0:h]
    
    bg = cv2.bitwise_and(roi, roi, mask = mask_inv[0:w, 0:h])
    fg = cv2.bitwise_and(mymy, mymy, mask = mask[0:w, 0:h])
    
    result = cv2.add(bg, fg)
    img[x: x + w, y: y + h] = result[0:w, 0:h]
    #cv2.cvtColor(myimg,cv2.COLOR_BGRA2GRAY)
    return img
    


shp = (8, 6)
    
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((shp[1]*shp[0],3), np.float32)
objp[:,:2] = np.mgrid[0:shp[0],0:shp[1]].T.reshape(-1,2)

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)


camera = cv2.VideoCapture(1)
if not camera.isOpened():
    camera = cv2.VideoCapture(0)


while True:
    
    img = camera.read()[1]
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, shp, None)

    if ret == True:
        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        # Find the rotation and translation vectors.
        rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)

        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

        img = draw(img,corners,imgpts)  
    
    cv2.imshow('img',img)
    
    k = cv2.waitKey(5) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('result.png', img)

cv2.destroyAllWindows()