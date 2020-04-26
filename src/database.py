#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3, os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

reload(sys).setdefaultencoding("utf-8")

def rplace(text):
    text = text.replace("ç","c")
    text = text.replace("Ç","C")
    text = text.replace("Ö","O")
    text = text.replace("ö","o")
    text = text.replace("ş","s")
    text = text.replace("Ş","S")
    text = text.replace("İ","I")
    text = text.replace("Ü","U")
    text = text.replace("ü","u")
    return text

def dbCreator():
    a = raw_input("Enter a .csv file to create a 'score.db': ")
    b = libdatabase()
    b.datapath = "score.db"
    b.fillToArchive(a)
class libdatabase:
    def __init__(self):
        self.a = None #SQLite connection
        self.c = None #cursor
        self.datapath = None
    def connect(self):
        self.a = sqlite3.connect(self.datapath)
        self.c = self.a.cursor()
    def commitclose(self):
        self.a.commit()
        self.c.close()
    def get_list(self, cursor):
        row = []
        for i in cursor:
            row.append(i)
        cursor.close()
        return row
    def searchBy(self, text, category):
        self.connect()
        self.c.execute('''SELECT * FROM archive WHERE LTRIM({0}) LIKE \'{1}%\' '''.format(category, text))
        row = self.get_list(self.c)
        return row
    def getAll(self):
        self.connect()
        self.c.execute('''SELECT * FROM archive ORDER BY orderer''')
        #self.c.execute('''SELECT * FROM archive ''')

        row = self.get_list(self.c)
        return row
    def start(self):
        self.connect()
        #Eserin İlk Dizesi;Makam;Form;Usul;Besteci;Söz Yazarı
        self.c.execute('''CREATE TABLE archive (id INTEGER PRIMARY KEY, firstline TEXT,
                          makam TEXT, form TEXT, time TEXT, composer TEXT, poet TEXT, orderer TEXT)''')

        #self.c.execute('''CREATE TABLE pictures (id INTEGER PRIMARY KEY, archiveid INTEGER, path TEXT)''')
        self.commitclose()
    def addToArchive(self, firstline, makam, form, time, composer, poet,orderer):
        self.connect()
        command = '''INSERT INTO archive (firstline, makam, form, time, composer, poet, orderer) VALUES
                          ("%s","%s","%s","%s","%s","%s","%s")''' % (firstline, makam, form, time, composer, poet, orderer)
        #print command
        self.c.execute(command)
        self.commitclose()

    def fillToArchive(self, csvfile):
        try:
            os.remove("score.db")
        except:
            pass
        self.start()
        myfile = open(csvfile, 'r')
        readlist = myfile.readlines()
        x = 0
        for i in readlist:
            x = x + 1
            second = i.split(";")
            print "- "+str(x)+" added " + " - "
            a = rplace(second[0].strip())
            print a
            self.addToArchive(second[0].strip(),second[1].strip(),second[2].strip(),
                              second[3].strip(),second[4].strip(),second[5].strip(),a)



if __name__ == '__main__':
    dbCreator()
