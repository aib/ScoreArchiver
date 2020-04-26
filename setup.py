#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os, glob, shutil, platform

PLATFORM = platform.system()


if PLATFORM == "Linux":
    myfiles = ["score.py","graphic.py","ScoreArchiver.py","ScoreArchiver","database.py"]
    if not os.path.exists("ScoreArchiver/"):
        os.mkdir("ScoreArchiver")
        for i in myfiles:
            shutil.copy("./src/"+i,"ScoreArchiver/")
        for i in glob.glob("./data/*.ts"):
            os.system("lrelease -verbose " + i)
            os.system("lrelease-qt4 -verbose " + i)
        for i in glob.glob("./data/*.qm"):
            shutil.copy(i,"ScoreArchiver/")
        for i in glob.glob("./ui/*.ui"):
            command = "pyuic4 "+i+" -o "+ "ScoreArchiver/"+ i.split("/")[-1].replace(".","_")+".py"
            print(command)
            os.system(command)
    os.system("pyrcc4 ./data/scorearchiver.qrc -o ./ScoreArchiver/scorearchiver_rc.py")
    os.chmod("./ScoreArchiver/ScoreArchiver", 0o755)
    os.system("touch ./ScoreArchiver/__init__.py")

    data = [("share/applications", ["./data/ScoreArchiver.desktop"]),
            ("share/pixmaps", ["./data/scorearchiver.png"]),
            ("share/scorearchiver/qm", glob.glob("./ScoreArchiver/*.qm"))
           ]

    setup(
        name = "ScoreArchiver",
        version = "1.0",
        description = "Shows Turkish Music Archive",
        author = "Taha Doğan Güneş",
        author_email = "tdgunes@gmail.com",
        url = "http://code.google.com/p/scorearchiver",
        packages = ["ScoreArchiver"],
        scripts = ["./ScoreArchiver/ScoreArchiver"],
        data_files = data
        )

elif PLATFORM == "Darwin":
    import py2app
    print("Building on Mac")
    #icon building
    go = input("Warning! - You need cx_freeze to build!(ok to continue)")
    try:
        try:
            os.system("rm -R -f ./build")
        except:
            pass
        try:
            os.system("rm -R -f ./ScoreArchiver.app")
        except:
             pass
        try:
            os.system("rm -R -f ./ScoreArchiver.dmg")
        except:
             pass

    except:
        pass
    os.mkdir("build")
    tsfiles = glob.glob("./data/*.ts")
    for i in tsfiles:
        os.system("lrelease -verbose ./data/%s" % i.split("/")[-1]),
    qmfiles = glob.glob("./data/*.qm")
    print(qmfiles)
    for i in qmfiles:
        shutil.copy(i, "build/")
        os.remove(i)
   # a = raw_input("go?:")

    os.system("pyrcc4 ./data/scorearchiver.qrc -o ./build/scorearchiver_rc.py")
    os.system("pyuic4 ./ui/main.ui -o ./build/main_ui.py")
    os.system("pyuic4 ./ui/score.ui -o ./build/score_ui.py")

    shutil.copy("data/scorearchiver.icns", "build/")
    shutil.copy("src/ScoreArchiver.py","build/")
    shutil.copy("src/graphic.py","build/")
    shutil.copy("src/database.py","build/")
    shutil.copy("src/score.py","build/")

    os.chdir("build")
    os.sys.path.append("./")
    APP = ['./ScoreArchiver.py']
    OPTIONS = { 'argv_emulation': True, 'iconfile': 'scorearchiver.icns','includes': ["time"]}
    setup(
        app=APP,
        options={'py2app': OPTIONS},
        setup_requires=['py2app']
)
    try:
        os.system("rm -R -f ./build")
        os.system("cp  -f -R /Library/Frameworks/QtGui.framework ./")
        os.system("cp  -f -R /Library/Frameworks/QtCore.framework ./")
    except:
        pass
    exec("""os.system("sudo cxfreeze ScoreArchiver.py --target-dir ScoreArchiver")""")
    qmfiles = glob.glob("./*.qm")
    for i in qmfiles:
        shutil.copy(i, "ScoreArchiver/")
    myfiles = os.listdir("./ScoreArchiver/")
    print(myfiles)
    for i in myfiles:
        shutil.copy(("ScoreArchiver/%s" % i),"./dist/ScoreArchiver.app/Contents/MacOS/")
    try:
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/MacOS/python")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Frameworks/QtCore.framework")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Frameworks/QtGui.framework")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Resources/__boot__.py")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Resources/__error__.sh")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Resources/include")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Resources/lib")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Resources/ScoreArchiver.py")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Resources/site.py")
        os.system("sudo rm -R -f ./dist/ScoreArchiver.app/Contents/Resources/site.pyc")
        os.system("sudo rm -R -f ./ScoreArchiver")
        os.system("sudo mv  ./dist/ ./ScoreArchiver")
        askme = input("Do you want me to make you a .dmg package?(y/n)\n:-> ")
        if askme == "y":
            os.system("hdiutil create -imagekey zlib-level=9 -srcfolder ScoreArchiver/ ./ScoreArchiver.dmg")

    except:
        pass
    os.chdir(os.getcwd()[:-5])
    os.sys.path.append("./")
    try:
        if askme == "y":
             os.system("sudo cp -f -R ./build/ScoreArchiver.dmg ./")
        else:
             os.system("sudo cp -f -R ./build/ScoreArchiver/ScoreArchiver.app ./")
        os.system("sudo rm -f -R ./build")
    except:
        pass
    finally:
        print("Building is finished!, If you want to put version number\nYou need to edit info.plist inside Contents!")

elif PLATFORM == "Windows":
    import py2exe
    NAME="ScoreArchiver"

    try:


        os.mkdir("build")
    except:
        pass

    os.system("pyrcc4 .\\data\\scorearchiver.qrc -o .\\build\\scorearchiver_rc.py")
    os.system("pyuic4 .\\ui/main.ui -o .\\build\\main_ui.py")
    os.system("pyuic4 .\\ui/score.ui -o .\\build\\score_ui.py")
    #preparing package

    tsfiles = glob.glob(".\\data\\*.ts")
    pyfiles = glob.glob(os.getcwd()+".\\src\\*.py")
    for i in pyfiles:
        shutil.copy(i, "build\\")

    for i in tsfiles:
        os.system("lrelease -verbose %s" % i.split("/")[-1]),
    qmfiles = glob.glob(os.getcwd()+"\\data\\*.qm")
    print(qmfiles)
    shutil.copy(".\\data\\scorearchiver.ico","build\\")
    #creating icons



    data=[("",qmfiles)]




    os.chdir("build")
    os.sys.path.append(".\\")

    # To build $python.exe setup.py py2exe
    setup(windows=[{"script" : "ScoreArchiver.py","icon_resources":[(1,"scorearchiver.ico")] }],
          options={"py2exe" :
                  {"includes" : ["sip",
                                 "PyQt4.QtGui",
                                 "PyQt4.QtCore",
                                 "score_ui",
                                 "scorearchiver_rc",
                                 "main_ui",
                                 "database",
                                 "graphic",
                                 "score",
                                 "platform",
                                 "traceback",
                                 "cStringIO",
                                 "locale",
                                 "time",
                                 "os",
                                 "sys",],
                   "dll_excludes":["MSVCP90.dll"]}},
          data_files=data)

    shutil.copytree("dist", "..\\ScoreArchiver\\")
    os.chdir("..")


