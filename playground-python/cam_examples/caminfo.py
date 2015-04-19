


def cv_cap_info(capture):
    CV_CAP_PROP_FRAME_WIDTH = 3
    CV_CAP_PROP_FRAME_HEIGHT = 4
    CV_CAP_PROP_FPS = 5
    CV_CAP_PROP_GAIN = 14
    CV_CAP_PROP_EXPOSURE = 15
    h    = "height: " + str(capture.get(CV_CAP_PROP_FRAME_HEIGHT))
    w    = "width:  " + str(capture.get(CV_CAP_PROP_FRAME_WIDTH))
    fps  = "fps:    " + str(capture.get(CV_CAP_PROP_FPS))
    gain = "gain:   " + str(capture.get(CV_CAP_PROP_GAIN))
    expo = "expo:   " + str(capture.get(CV_CAP_PROP_EXPOSURE))
    info = "\n".join([h, w, fps, gain, expo])
    return info + "\n"