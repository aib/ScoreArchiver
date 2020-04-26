#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from score_ui import Ui_Dialog

import platform

PLA = platform.system()
	
class ScoreDialog(QDialog, Ui_Dialog):
    def __init__(self, archiveid,dpath):
        QDialog.__init__(self)
        self.setupUi(self)

        self.connect(self.comboBox, SIGNAL("activated(int)"), self.addtoList) 

        self.connect(self.listWidget, SIGNAL("currentRowChanged(int)"), self.showPicture)

        self.connect(self.pushButton, SIGNAL("clicked()"), self.filePrint)

        self.archiveid = archiveid
        self.printer = None
        self.dpath = dpath
        # print "%s%sdata%s%s" % (self.dpath,os.sep,os.sep, str(archiveid))
        # print "%s%sdata%s%s" % (self.dpath,"/","/", str(archiveid))
        # print "dirs:", self.dircleaner(os.listdir("%s%sdata%s%s" % (self.dpath,"\\\\","\\\\", str(archiveid))))
        dirs = self.dircleaner(os.listdir("%s%sdata%s%s%s" % (self.dpath,os.sep,os.sep, str(archiveid),os.sep)))
        dirs.sort()
        #print dirs
        self.comboBox.addItems(self.makelistString(dirs))
        self.label_3.setText(str(len(self.makelistString(dirs))))
        self.addtoList(0)
        self.currentPixmap = None
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0,0,612,792)
        self.graphicsView.setScene(self.scene)
    

        if PLA == "Windows":
            settings = QSettings("settings.ini", QSettings.IniFormat)
        else:
            settings = QSettings()

        size = settings.value("Score/Size",
                              QVariant(QSize(600, 500))).toSize()
        self.resize(size)
        position = settings.value("Score/Position",
                                  QVariant(QPoint(0, 0))).toPoint()
        self.move(position)

    def filePrint(self):
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setPageSize(QPrinter.Letter)
        form = QPrintDialog(self.printer, self)
        if form.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.currentPixmap.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.currentPixmap.rect())
            painter.drawPixmap(0, 0, self.currentPixmap)

    def showPicture(self):
        self.scene.clear()
        if self.listWidget.currentItem():
            filename = self.listWidget.currentItem().text()
            picture = QPixmap("%s%sdata%s%s%s%s%s%s" % (self.dpath, os.sep, os.sep, str(self.archiveid), os.sep, str(self.comboBox.currentIndex()+1), os.sep,filename))
            self.currentPixmap = QPixmap("%s%sdata%s%s%s%s%s%s" % (self.dpath, os.sep, os.sep, str(self.archiveid), os.sep, str(self.comboBox.currentIndex()+1), os.sep, filename))
            
            item = QGraphicsPixmapItem(self.currentPixmap)
            item.setPos(0,0)
            item.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
            item.setMatrix(QMatrix())
            self.scene.clearSelection()
            self.scene.addItem(item)

    def addtoList(self, number):
       
        files = []
        self.listWidget.clear()
        dirs = self.dircleaner(os.listdir("%s%sdata%s%s%s%s" % (self.dpath,os.sep, os.sep,str(self.archiveid),os.sep, str(number+1))))
        dirs.sort()
        for i in dirs:
            self.listWidget.addItem(i)
        
    def makelistString(self, alist):
        a = []
        for i in alist:
            a.append(str(i))
        return a
    def dircleaner(self, alist):
        a = []
        for i in alist:
            if i[0] != ".":
                a.append(i)
        return a
      
    def closeEvent(self, event):
        if PLA == "Windows":
            settings = QSettings("settings.ini", QSettings.IniFormat)
        else:
            settings = QSettings()
        settings.setValue("Score/Size", QVariant(self.size()))
        settings.setValue("Score/Position",
               QVariant(self.pos()))


