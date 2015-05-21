import cv2
import numpy as np
from cam import MyCam
from fmatch import draw_match

from find_polygons import find_polygons, draw_oriented_polylines

class ScreenFinder(object):
    """This class find the location of the screen by checking
    if there is a quadrangle area that varies with respect to time"""

    def __init__(self):
        self.screen_shape = None
        self.screen_corners = None
        self.recovery_matrix = None
        
        self._detector = cv2.SIFT()
        self._screen_img = None
        
        self._screen_features = None
    
    def set_screen_img(self, screen_img):
        self._screen_features = self._detector.detectAndCompute(screen_img,None)
        self._screen_img = screen_img
    
    def find_screen_img(self, cam_img, screen_img=None, debug=True):
        
        MIN_MATCH_COUNT = 10
        FLANN_INDEX_KDTREE = 0
        
        
        if screen_img == None:
            kp1, des1 = self._screen_features
            screen_img = self._screen_img
        else:
            kp1, des1 = self._detector.detectAndCompute(screen_img,None)
            
        kp2, des2 = self._detector.detectAndCompute(cam_img,None)

        
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,des2,k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)

        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            h,w = self._screen_img.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            cv2.draw_oriented_polylines(cam_img,[np.int32(dst)],True,255,3)

        else:
            print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
            matchesMask = None
            
        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

        if debug==True:
            img3 = draw_match(self._screen_img, kp1, cam_img, kp2,good,None,**draw_params)
            cv2.imshow('matches', img3)

    def find_top_view(self, cam_img):
        shape = (self._screen_img.shape[1], self._screen_img.shape[0])
        img = warpPerspective(cam_img, self.recovery_matrix, shape)
        return img
        
if __name__ == '__main__':
    sf = ScreenFinder()
    cam = MyCam()
    cam.size = (640, 480)
    
    img = cv2.imread('seabunny1600.png', 0)
    cv2.imshow('source', img)

    if img.shape[0] * img.shape[1] > cam.size[0] * cam.size[1]:
        img = cv2.resize(img, cam.size)

    sf.set_screen_img(img)
    while True:
        cam_img = cv2.flip(cam.read(), 1)
        sf.find_screen_img(cam_img)
        cv2.imshow('cam', cam_img)
        
        k = cv2.waitKey(5)
        if k == 27:
            break