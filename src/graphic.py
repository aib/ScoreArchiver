#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class graphic(QGraphicsView):
    def __init__(self, parent=None):
        super(graphic, self).__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
    def wheelEvent(self, event):
        factor = 1.41**(-event.delta()/240.0)
        self.scale(factor, factor)

