import cv2
from cam import MyCam

cam = MyCam()
while True:
    img = cam.read()
    imgR = img[:,:,2]
    imgG = img[:,:,1]
    
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(imgR)