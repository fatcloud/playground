

#!/usr/bin/env python

import thread
import Queue
import time

import thread
import worker
import kivy_worker
from kivy.graphics import Color, Rectangle
from random import random as r
from kivy.base import runTouchApp


class SimpleModel(worker.Worker):

    def __init__(self):
        super(SimpleModel, self).__init__()
        self._add_sqrt = 0

    def _routine(self):
        missions = self.mission_queue
        while not missions.empty():
            mission = missions.get_nowait()
            self._add_sqrt += mission['show square']

    def _export_missions(self, caller):
        if self._add_sqrt > 0:
            mission = {'add_rect':self._add_sqrt}
            self._add_sqrt -= 1
            return [mission]
        return []

        
class SimpleWindow(kivy_worker.KivyWorker):

    def __init__(self, model=None):
        super(SimpleWindow, self).__init__(model)
        self._signal_to_model = []

    def _execute_a_keyboard_mission(self, mission):
        key_code = mission['key_code']
        if key_code[1] == 'up':
            sig = {'show square':1}
        else:
            exit()
        self._signal_to_model.append(sig)
    
    def _execute_a_render_mission(self, mission):
        """handle Model mission and do the render"""
        if mission['add_rect']:
            with self.canvas:
                Color(r(), 1, 1, mode='hsv')
                Rectangle(pos=(r() * self.width,
                    r() * self.height), size=(20, 20))
        
    # translate keyboard command to model signal    
    def _export_missions(self, receiver):
        sigs = self._signal_to_model[:]
        self._signal_to_model = []
        return sigs



if __name__ == '__main__':
    # print __doc__
    sm = SimpleModel()
    sm.start_loop()
    sw = SimpleWindow()
    sw.model = sm
    # runTouchApp(SimpleWindow(sm))
    runTouchApp(sw)


