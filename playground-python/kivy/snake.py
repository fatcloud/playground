'''
Canvas stress
=============

This is just a test for testing the performance of our Graphics engine.
'''

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, Rectangle
from random import random as r
from functools import partial
    
from kivy.core.window import Window


class BoxesCanvus(Widget):

    def __init__(self, **kwargs):
        super(BoxesCanvus, self).__init__(**kwargs)
        self.cols = 1
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.add_rects(100)
        
    def add_rects(self, count, *largs):
        with self.canvas:
            for x in range(count):
                Color(r(), 1, 1, mode='hsv')
                Rectangle(pos=(r() * self.width,
                               r() * self.height), size=(20, 20))

class MyApp(App):

    def build(self):
        bc = BoxesCanvus()
        return bc

    def on_start(self):
        self.root.add_rects(100)


if __name__ == '__main__':
    MyApp().run()
    
