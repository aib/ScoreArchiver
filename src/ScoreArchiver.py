#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from os import getcwd, sep, listdir
import time, traceback, io




from main_ui import Ui_MainWindow
from database import libdatabase
from score import ScoreDialog
import platform

PLA = platform.system()

if platform.system() == "Darwin" and platform.system() == "Linux":

    import locale
    locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")

elif platform.system() == "Windows":
    import locale
    locale.setlocale(locale.LC_ALL,'Turkish_Turkey.1254')

#Thanks to the Eric IDE :)
#http://www.mail-archive.com/pyqt@riverbankcomputing.com/msg17424.html
def excepthook(excType, excValue, tracebackobj):
    separator = '-' * 80
    notice = "An unhandled exception occurred.\nPlease report the problem via email to <scorearchiver@gmail.com>\nVersion: \"1.0\".\n\nError information:\n"
    timeString = time.strftime("%d-%m-%Y  %H:%M:%S")
    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)


    errorbox=  QMessageBox()
    errorbox.setText(str(notice)+str(msg))
    errorbox.exec_()



class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        if PLA == "Windows":
            settings = QSettings("settings.ini", QSettings.IniFormat)
        else:
            settings = QSettings()
        self.savePath = None
        widths = settings.value("widths").toStringList()
        if widths:
            for i in range(0,7):
                self.tableWidget.setColumnWidth(i,int(widths[i]))

        self.database = libdatabase()
        if PLA == "Windows":
            if QFile.exists("."+sep+"score.db") and  QFile.exists("."+sep+"data"):
                self.savePath = "."
            else:
                QMessageBox.warning(self, self.tr("Score Archiver - Database Not Found"), self.tr("Please put \'score.db\' file and \'data\' directory near to the exe file."))
                sys.exit(1)
        else:
            self.savePath = self.returnDBPath()
        print(self.savePath)
        if self.savePath:
            path = str(self.savePath+sep+"score.db")

        self.setWindowTitle(self.tr("ScoreArchiver") + " - ("+path+")")
        self.database.datapath = path
        self.database.connect()

        self.connect(self.actionAbout, SIGNAL("triggered()"), self.about_me)
        self.connect(self.toolButton, SIGNAL("clicked()"), self.go_to_donate)
        self.connect(self.scoretool, SIGNAL("clicked()"), self.go_to_score)
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.search_data)

        if PLA == "Darwin":
            QTimer.singleShot(0, self.fill_data)
        else:
            self.fill_data()

        size = settings.value("MainWindow/Size",
                              QVariant(QSize(600, 500))).toSize()
        self.resize(size)
        position = settings.value("MainWindow/Position",
                                  QVariant(QPoint(0, 0))).toPoint()
        self.move(position)
        self.restoreState(settings.value("MainWindow/State").toByteArray())
    def about_me(self):
        QMessageBox.about(self, self.tr("About ScoreArchiver"), self.tr("ScoreArchiver - 1.0\n\nTurkish Music Archive Viewer\n\n\nEmre Pinarbasi   <emrepinarbasi@gmail.com>\nTaha Dogan Gunes <tdgunes@gmail.com>\n\nLicense: GPLv3\n\nWeb Site: code.google.com/p/scorearchiver"))

    def go_to_donate(self):

        QDesktopServices.openUrl(QUrl("https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=2YSBG5295B3XE&lc=TR&item_name=Scorearchiver&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted"))
    def returnDBPath(self):
        settings = QSettings()
        pname = (settings.value("databasePath").toString())

        if pname and QFile.exists(pname+sep+"score.db") and  QFile.exists(pname+sep+"data"):

            return pname
        else:

            pname = str(QFileDialog.getExistingDirectory(self, self.tr("ScoreArchiver")+self.tr("Add the database directory")))

            if pname and QFile.exists(pname+sep+"score.db") and  QFile.exists(pname+sep+"data"):
                print(pname)
                return pname
            else:
                print(pname)
                sys.exit(1)

    def closeEvent(self, event):
        if self.savePath:
            if PLA == "Windows":
                settings = QSettings("settings.ini", QSettings.IniFormat)
            else:
                settings = QSettings()
            widths = []
            for i in range(0,7):
                widths.append(str(self.tableWidget.columnWidth(i)))
            allwidth = QVariant(widths)
            settings.setValue("widths", widths)
            settings.setValue("databasePath", self.savePath)
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position",
                   QVariant(self.pos()))
            settings.setValue("MainWindow/State", QVariant(self.saveState()))



    def search_data(self):
        keyword = self.lineEdit.text()
        if keyword:
             mydict = {0:"firstline",1:"makam",2:"form",3:"time",4:"composer",5:"poet"}
             cat = mydict.get(self.comboBox.currentIndex())
             self.addToTable(self.database.searchBy(keyword, cat))
        else:
             self.fill_data()

    def go_to_score(self):
        ifpass = True
        try:
            number = int( self.tableWidget.item( self.tableWidget.currentRow(), 0).text())
        except AttributeError:
            ifpass = False
        if ifpass:
            try:
                 if QFile.exists(self.savePath+sep+"data"+sep+str(number)):
                     scoredialog = ScoreDialog(number, str(self.savePath))
                     scoredialog.exec_()

                 else:
                     QMessageBox.warning(self, self.tr("Score Archiver - Record Not Found"), str(number)+ self.tr("\'s score data is missing,\nIf you want to add,\nplease contact scorearchiver@gmail.com"))
            except OSError as ose:
                 (error_no, error) = ose.args
                 if error_no is 2:
                     QMessageBox.warning(self, self.tr("Score Archiver - Record Not Found"), str(number)+ self.tr("\'s score data is missing,\nIf you want to add,\nplease contact scorearchiver@gmail.com"))



    def addToTable(self, b):
        self.tableWidget.clearContents()
        x = 0
        while x<len(b):

            self.tableWidget.setRowCount(len(b))
            self.label_2.setText(str(len(b)))
            aa = QTableWidgetItem(str(b[x][0]))
            ab = QTableWidgetItem(b[x][1])
            ac = QTableWidgetItem(b[x][2])
            ad = QTableWidgetItem(b[x][3])
            ae = QTableWidgetItem(b[x][4])
            af = QTableWidgetItem(b[x][5])
            ag = QTableWidgetItem(b[x][6])
            self.tableWidget.setItem(x, 0, aa)
            self.tableWidget.setItem(x, 1, ab)
            self.tableWidget.setItem(x, 2, ac)
            self.tableWidget.setItem(x, 3, ad)
            self.tableWidget.setItem(x, 4, ae)
            self.tableWidget.setItem(x, 5, af)
            self.tableWidget.setItem(x, 6, ag)
            x+=1

    def fill_data(self):
        self.addToTable(self.database.getAll())

sys.excepthook = excepthook


def main():

    app = QApplication(sys.argv)
    locale = QLocale.system().name()
    translator = QTranslator()
    if PLA == "Darwin":
        translator.load(getcwd()+"/ScoreArchiver.app/Contents/MacOS/scorearchiver_%s.qm" % locale)
   # translator.load('scorearchiver_%s.qm' % "tr_TR")
    elif PLA=="Linux":
        if QFile.exists("/usr/local/share/scorearchiver/qm"):
            translator.load("/usr/local/share/scorearchiver/qm/scorearchiver_%s.qm" % locale)
        elif QFile.exists("/usr/share/scorearchiver/qm"):
            translator.load("/usr/share/scorearchiver/qm/scorearchiver_%s.qm" % locale)
        else:
            translator.load('scorearchiver_%s.qm' % locale)
    else:
        translator.load('scorearchiver_%s.qm' % locale)
    app.installTranslator(translator)

    main_window = MainWindow()
    main_window.show()
    app.exec_()

if __name__ == '__main__':
    main()
