import cv2
import numpy as np



cam = cv2.VideoCapture(0)
# fgbg = cv2.BackgroundSubtractorMOG()
while (cam.isOpened):
    f, img = cam.read()
    lo, hi = 100, 150
    if f == True:
        
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # img=cv2.flip(img,1)
        # img=cv2.medianBlur(img,3)
        # fgmask = fgbg.apply(img)
        # blur = cv2.blur(fgmask,(10,10))
        '''
        edgeH = cv2.Canny(img[:,:,0],100,200)
        edgeV = cv2.Canny(img[:,:,2],100,200)
        edge = cv2.bitwise_or(edgeH, edgeV)
        '''
        # edge = cv2.Canny(img, lo, hi)
        
        gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh1, dst = cv2.threshold(gry,127,255,cv2.THRESH_BINARY)
        dst = cv2.bitwise_not(dst)
        
        ctr, hry = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # while True: exec raw_input(">>>")
        
        
        hry = hry[0]
        
        for idx, cnt in enumerate(ctr):
            
            if(hry[idx][2] == -1):
                continue
            
            epsilon = 0.05*cv2.arcLength(cnt,True)
            tmp = cv2.approxPolyDP(cnt,epsilon,True)
            
            child = ctr[hry[idx][2]]
            epsilon = 0.05*cv2.arcLength(child,True)
            ttmp = cv2.approxPolyDP(child,epsilon,True)
            if (len(tmp), len(ttmp)) = (4, 4) and cv2.contourArea(tmp)/cv2.contourArea(ttmp) > /:
                cv2.drawContours(img, [tmp], 0, (0, 0, 255))
                cv2.drawContours(img, [ttmp], 0, (0, 255, 0))
        
        cv2.imshow('edge', img)
        #cv2.drawContours(edge, ctr, -1, (1, 0, 0))
        #cv2.imshow('edgeH', edgeH)
        #cv2.imshow('edgeV', edgeV)
        
        #cv2.imshow('edge', edge)
    if (cv2.waitKey(27) != -1):
        cam.release()
        cv2.destroyAllWindows()
        break