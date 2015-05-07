import cv2
import numpy as np



cam = cv2.VideoCapture(0)
# fgbg = cv2.BackgroundSubtractorMOG()
while (cam.isOpened):
    f, img = cam.read()
    lo, hi = 100, 150
    if f == True:
        
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
            
            '''
            if(hry[idx][2] == -1): continue       # no child
            
            child   = ctr[hry[idx][2]]
            epsilon = 0.05*cv2.arcLength(child,True)
            ttmp    = cv2.approxPolyDP(child,epsilon,True)
            
            ratio   = 0
            try:
                ratio   = cv2.contourArea(tmp)/cv2.contourArea(ttmp)
            except ZeroDivisionError:
                pass
            if (, len(ttmp)) == (4, 4) and ratio > 0.1 and cv2.contourArea(tmp) > 100:
                cv2.drawContours(img, [tmp], 0, (0, 0, 255))
                cv2.drawContours(img, [ttmp], 0, (0, 255, 0))
            '''
            
        cv2.imshow('edge', img)
        
    if (cv2.waitKey(27) != -1):
        cam.release()
        cv2.destroyAllWindows()
        break