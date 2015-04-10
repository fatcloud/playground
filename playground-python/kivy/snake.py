from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, Rectangle
from random import random as r
    
from kivy.core.window import Window


class BoxesCanvus(Widget):

    def __init__(self, **kwargs):
        super(BoxesCanvus, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
        
    def _init_key_func_map():
        self._key_func_map
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print 'the key', keycode, 'with modifier', modifiers, 'is pressed'
        return True


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
    
