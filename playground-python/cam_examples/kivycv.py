#! /usr/bin/env python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


import cv2
import numpy as np

class CamApp(App):

    def build(self):
        self.img1 = Image(source='images/1.jpg')
        layout = BoxLayout()
        layout.add_widget(self.img1)
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        
        ret, frame = self.capture.read()
        Clock.schedule_interval(self.update, 1.0/60.0)
        return layout

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        # convert it to texture
        buf1 = cv2.flip(frame, -1)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    CamApp().run()

