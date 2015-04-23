import cv2
CV_CAP_PROP_POS_MSEC = 0      # 'Current position of the video file in milliseconds.'
CV_CAP_PROP_POS_FRAMES = 1    # '0-based index of the frame to be decoded/captured next.'
CV_CAP_PROP_POS_AVI_RATIO = 2 # 'Relative position of the video file'
CV_CAP_PROP_FRAME_WIDTH = 3   # 'Width of the frames in the video stream.'
CV_CAP_PROP_FRAME_HEIGHT =4   # 'Height of the frames in the video stream.'
CV_CAP_PROP_FPS = 5           # 'Frame rate.'
CV_CAP_PROP_FOURCC = 6        # '4-character code of codec.'
CV_CAP_PROP_FRAME_COUNT =7    # 'Number of frames in the video file.'
CV_CAP_PROP_FORMAT = 8        # 'Format of the Mat objects returned by retrieve() .'
CV_CAP_PROP_MODE = 9          # 'Backend-specific value indicating the current capture mode.'
CV_CAP_PROP_BRIGHTNESS = 10   # 'Brightness of the image (only for cameras).'
CV_CAP_PROP_CONTRAST = 11     # 'Contrast of the image (only for cameras).'
CV_CAP_PROP_SATURATION = 12   # 'Saturation of the image (only for cameras).'
CV_CAP_PROP_HUE =13           # 'Hue of the image (only for cameras).'
CV_CAP_PROP_GAIN = 14         # 'Gain of the image (only for cameras).'
CV_CAP_PROP_EXPOSURE = 15     # 'Exposure (only for cameras).'

def cv_cap_info(capture):
    h    = "height: " + str(capture.get(CV_CAP_PROP_FRAME_HEIGHT))
    w    = "width:  " + str(capture.get(CV_CAP_PROP_FRAME_WIDTH))
    fps  = "fps:    " + str(capture.get(CV_CAP_PROP_FPS))
    gain = "gain:   " + str(capture.get(CV_CAP_PROP_GAIN))
    expo = "expo:   " + str(capture.get(CV_CAP_PROP_EXPOSURE))
    mode = "mode:   " + str(capture.get(CV_CAP_PROP_MODE))
    info = "\n".join([h, w, fps, gain, expo, mode])
    
    return info + "\n"
    
if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        cv2.imshow('info',frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
        elif ch != None:
            print cv_cap_info(cam)