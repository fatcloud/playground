#!/usr/bin/env python

'''
Camshift tracker
================

This is a demo that shows mean-shift based tracking
You select a color objects such as your face and it tracks it.
This reads from video camera (0 by default, or the camera number the user enters)

http://www.robinhewitt.com/research/track/camshift.html

Usage:
------
    camshift.py [<video source>]

    To initialize tracking, select the object with mouse

Keys:
-----
    ESC   - exit
    b     - toggle back-projected probability visualization
'''

import numpy as np
import cv2
import video






from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, Rectangle
from random import random as r
    
from kivy.core.window import Window


class MainCanvus(Widget):

    def __init__(self, **kwargs):
        super(MainCanvus, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self.cam = video.create_capture()
        ret, self.frame = self.cam.read()
        

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
        cv2.VideoCapture.release()
        print 'yooo'
                
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print 'the key', keycode, 'with modifier', modifiers, 'is pressed'
        ret, self.frame = self.cam.read()
        vis = self.frame.copy()
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        cv2.imshow('camshift', vis)
        return True

    def add_rects(self, count, *largs):
        with self.canvas:
            for x in range(count):
                Color(r(), 1, 1, mode='hsv')
                Rectangle(pos=(r() * self.width,
                               r() * self.height), size=(20, 20))

class MyApp(App):

    def build(self):
        self.bc = MainCanvus()
        return self.bc

    def on_start(self):
        self.root.add_rects(100)

    def on_stop(self):
        self.bc.cam.release()
        
if __name__ == '__main__':
    print __doc__
    MyApp().run()
    print 'haha'





