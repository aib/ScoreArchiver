#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class graphic(QGraphicsView):
    def __init__(self, parent=None):
        super(graphic, self).__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
    def wheelEvent(self, event):
        factor = 1.41**(-event.delta()/240.0)
        self.scale(factor, factor)

