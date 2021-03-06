# -*- coding: utf-8 -*-
# all screens represent a class in a python
# the variables are the labels, widgets, etc. PyQt does it for us with loadUi
# source of tutorials: https://www.youtube.com/watch?v=RxGlB9U64fg&list=PLs3IFJPw3G9LTcNjRVR6BSJwUaoj44rCV

# NOTE
# firebase replacing data and refreshing information
# extract information ---> instead input it
# have button to go to login page if already signed up on sign in page?
# All information needs to be saved in that account


# push data: https://github.com/codefirstio/Python-Firebase-Realtime-Database-CRUD-Series/blob/master/createdata.py

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
#from firebase_admin import auth

from datetime import datetime
import time
from time import sleep

import smtplib
from email.message import EmailMessage

from PyQt5.QtCore import QObject, QThread, pyqtSignal

# importing raspberrypi
# import RPi.GPIO as GPIO
# import time import sleep
import pyrebase

# need to import pyrebase
firebaseConfig = {
    'apiKey': "AIzaSyDFcKZxM45qSe9DmtSPoUwwVYilclTouKs",
    'authDomain': "capstone-project-6325f.firebaseapp.com",
    'databaseURL': "https://capstone-project-6325f-default-rtdb.firebaseio.com",
    'projectId': "capstone-project-6325f",
    'storageBucket': "capstone-project-6325f.appspot.com",
    'messagingSenderId': "463650994151",
    'appId': "1:463650994151:web:62f7742b008e5485726f42",
    'measurementId': "G-E88E98P34S"
};
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

now = datetime.now()


class Load(QDialog):
    def __init__(self):
        super(Load, self).__init__()
        loadUi("load.ui", self)
        self.s1.clicked.connect(self.start1)
        self.s2.clicked.connect(self.start2)
        self.s3.clicked.connect(self.start3)
        self.s4.clicked.connect(self.start4)
        self.f1.clicked.connect(self.finish1)
        self.f2.clicked.connect(self.finish2)
        self.f3.clicked.connect(self.finish3)
        self.f4.clicked.connect(self.finish4)
        self.back.clicked.connect(self.backto)

    def start1(self):
        ea_user = self.email.text()
        other = db.child("Medication").child("Med1").order_by_child("User email").equal_to(ea_user).get()
        print(other.val())
        # key=result.val()
        key = str(other.val())
        key2 = key[key.index('[('):key.index('Hour1')]
        key3 = key2[3:-5]
        test=db.child("Medication").child("Med1").child(key3).get()
        test1 = str(test.val())
        print(test1)
        move_to_level(1)
        slot = db.child("Medication").child("Med1").child(key3).child("SCount1").get()
        nm = int(str(slot.val()))
        num=20-nm
        print(num)
        if num <= 20 and num >= 1:
            slotnew = num - 1
            count1 = 20-num
            rotate(1, False)
            db.child("Medication").child("Med1").child(key3).update({"SCount1":count1})
            self.c1.setText(count1)
            time.sleep(8)
        else:
            print("Not enough slots, start at a new level")


    def finish1(self):
        ea_user = self.email.text()
        other = db.child("Medication").child("Med1").order_by_child("User email").equal_to(ea_user).get()
        print(other.val())
        # key=result.val()
        key = str(other.val())
        key2 = key[key.index('[('):key.index('Hour1')]
        key3 = key2[3:-5]
        a1=db.child("Medication").child("Med1").child(key3).child("Count1").get()
        b1=str(a1.val())
        self.c1.setText(b1)
        move_to_level(1)
        disable_motors(1)

    def backto(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class InfoShow(QDialog):
    def __init__(self):
        super(InfoShow, self).__init__()
        loadUi("InfoShow.ui", self)
        self.pushButton_2.clicked.connect(self.accessSU)

        self.pushButton.clicked.connect(self.gotoprofile)

    def accessSU(self):
        ea_user = self.email.text()
        result = db.child("users").order_by_child("User email").equal_to(ea_user).get()
        print(result.val())
        # key=result.val()
        key = str(result.val())
        here = key[key.index('Last name'):key.index('User')]
        true = here[13:-4]
        here1 = key[key.index('First name'):key.index('Last')]
        true1 = here1[14:-4]
        here2 = key[key.index('DOB'):key.index('First')]
        true2 = here2[7:-4]
        self.Lastname.setText(true)
        self.first.setText(true1)
        self.DOB.setText(true2)

        other = db.child("Medication").child("Med1").order_by_child("User email").equal_to(ea_user).get()
        print(other.val())
        # key=result.val()
        key = str(other.val())
        key2 = key[key.index('Name1'):key.index('PMor')]
        med1 = key2[9:-4]
        key3 = key[key.index('Hour1'):key.index('Min1')]
        h1 = key3[7:-4]
        key4 = key[key.index('Min1'):key.index('Name1')]
        m1 = key4[8:-4]
        key5 = key[key.index('AM1'):key.index('User')]
        a1 = key5[7:-4]

        self.Med1.setText(med1)

        self.min1.setText(m1)
        self.AP1.setText(a1)

        other2 = db.child("Medication").child("Med2").order_by_child("User email").equal_to(ea_user).get()
        print(other2.val())
        # key=result.val()
        key11 = str(other2.val())
        key21 = key11[key11.index('Name2'):key11.index('PMor')]
        med11 = key21[9:-4]
        key31 = key11[key11.index('Hour2'):key11.index('Min2')]
        h11 = key31[7:-4]
        key41 = key11[key11.index('Min2'):key11.index('Name2')]
        m11 = key41[8:-4]
        key51 = key11[key11.index('AM2'):key11.index('User')]
        a11 = key51[7:-4]

        self.Med2.setText(med11)

        self.min2.setText(m11)
        self.AP2.setText(a11)

        other3 = db.child("Medication").child("Med3").order_by_child("User email").equal_to(ea_user).get()
        print(other3.val())
        # key=result.val()
        key13 = str(other3.val())
        key23 = key13[key13.index('Name3'):key13.index('PMor')]
        med13 = key23[9:-4]
        key33 = key13[key13.index('Hour3'):key13.index('Min3')]
        h13 = key33[7:-4]
        key43 = key13[key13.index('Min3'):key13.index('Name3')]
        m13 = key43[8:-4]
        key53 = key13[key13.index('AM3'):key13.index('User')]
        a13 = key53[7:-4]

        self.Med3.setText(med13)

        self.min3.setText(m13)
        self.AP3.setText(a13)



        hou1 = ""
        for m in h1:
            if m.isdigit():
                hou1 = hou1 + m
        hou2 = ""
        for m in h11:
            if m.isdigit():
                hou2 = hou2 + m

        hou3 = ""
        for m in h13:
            if m.isdigit():
                hou3 = hou3 + m


        print(hou1)

        # hou1 = int(float((hou1)))
        # hou2 = int(float((hou2)))
        # hou3 = int(float((hou3)))
        # hou4 = int(float((hou4)))
        hou2 = int(hou2)
        hou3 = int(hou3)

        hou1 = int(hou1)
        if 12 < hou1:
            hou1 = hou1 - 12
        if 12 < hou2:
            hou2 = hou2 - 12
        if 12 < hou3:
            hou3 = hou3 - 12


        hou2 = str(hou2)
        hou3 = str(hou3)

        hou1 = str(hou1)


        self.Hour3.setText(hou3)
        self.Hour2.setText(hou2)
        self.Hour1.setText(hou1)

    def gotoprofile(self):
        yourpro = YourProfile()
        widget.addWidget(yourpro)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        # loads .ui file into code
        loadUi("signup.ui", self)
        # the loginbutton on QDialog (self) will execute accessLogin function when it is clicked
        self.subutton.clicked.connect(self.accessSU)
        self.ihaveacct_button.clicked.connect(self.HaveAnAcct)

        self.errormessage.setVisible(False)
        self.errormessage2.setVisible(False)

        # button for already have an account, different Login screen than verification screen

    def accessSU(self):
        ea_user = self.easu.text()
        password_user = self.passwordsu.text()
        firstname = self.firstname.text()
        lastname = self.lastname.text()
        dob = self.DOB.text()

        # https://github.com/codefirstio/PyQT5-with-Firebase-Auth-Login-and-Signup-form/blob/master/main.py
        try:
            # create account and push the data to database
            auth.create_user_with_email_and_password(ea_user, password_user)

            # key = {"Email":ea_user}
            # db.child("users").child(key)
            data = {"First name": firstname, "Last name": lastname, "DOB": dob, "User email": ea_user}
            db.child("users").push(data)

            mainmenu = MainMenu()
            widget.addWidget(mainmenu)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        except:
            if len(password_user) <= 6:
                self.errormessage2.setVisible(True)
                self.errormessage.setVisible(False)
            else:
                self.errormessage.setVisible(True)
                self.errormessage2.setVisible(False)
            # need to add condition for both, extract data from firebase?
            # it'll show both separaetely if the ocnditions don't fit

    def HaveAnAcct(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Verify(QDialog):
    def __init__(self):
        super(Verify, self).__init__()
        loadUi("verify.ui", self)
        self.Med1.clicked.connect(self.run1)
        #self.Med2.clicked.connect(self.run2)
        #self.Med3.clicked.connect(self.run3)
        self.backtoMain2.clicked.connect(self.gotomain)

    # def runMotor, all the stuff for the motor
    # if info is right, just one click and dispense, if not, try again
    def run1(self):
        ea_li = self.ea_li.text()
        password_li = self.password_li.text()
        auth.sign_in_with_email_and_password(ea_li, password_li)
        print("Successful verification Med1")
        me1 = db.child("Medication").child("Med1").order_by_child("User email").equal_to(ea_li).get()
        md1 = str(me1.val())
        ed1 = md1[md1.index('SCount1'):md1.index('}')]
        print(ed1)
        co = ed1[11:-1]
        ou = int(co)
        move_to_level(1)
        rotate(1, True)
        nt = ou-1
        key2 = md1[md1.index('[('):md1.index('Hour1')]
        key3 = key2[3:-5]
        db.child("Medication").child("Med1").child(key3).update({"SCount1":nt})



        # put motor code

    def gotomain(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Pharm(QDialog):
    def __init__(self):
        super(Pharm, self).__init__()
        loadUi("pharm.ui", self)
        self.cvs.clicked.connect(self.show_cvs)
        self.wal.clicked.connect(self.show_wal)
        self.rite.clicked.connect(self.show_rite)
        self.app.clicked.connect(self.gotoMedInfo)

    def show_cvs(QDialog):
        cvspage = CVSpage()
        widget.addWidget(cvspage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_wal(QDialog):
        walgreen = Walgreen()
        widget.addWidget(walgreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_rite(QDialog):
        riteaid = RiteAid()
        widget.addWidget(riteaid)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoMedInfo(self):
        medinfo = MedInfo()
        widget.addWidget(medinfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CVSpage(QDialog):
    def __init__(self):
        super(CVSpage, self).__init__()
        loadUi("cvs.ui", self)
        self.webEngineView.setUrl(QtCore.QUrl("https://www.cvs.com/account/login/"))
        self.webEngineView.setObjectName("webEngineView")

        self.app_2.clicked.connect(self.goPharm)
        self.back.clicked.connect(self.backward)
        self.goPage.clicked.connect(self.forward)
        self.re.clicked.connect(self.reload)
        self.homepage.clicked.connect(self.home)

    def backward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def reload(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Reload)

    def home(self):
        self.webEngineView.setUrl(QtCore.QUrl("https://www.cvs.com/account/login/"))

    def goPharm(QDialog):
        pharm = Pharm()
        widget.addWidget(pharm)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Walgreen(QDialog):
    def __init__(self):
        super(Walgreen, self).__init__()
        loadUi("walgreens.ui", self)
        self.webEngineView.setUrl(QtCore.QUrl("https://www.walgreens.com/login.jsp?ru=%2F"))
        self.webEngineView.setObjectName("webEngineView")

        self.app.clicked.connect(self.goPharm)
        self.back.clicked.connect(self.backward)
        self.goPage.clicked.connect(self.forward)
        self.re.clicked.connect(self.reload)
        self.homepage.clicked.connect(self.home)

    def backward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def reload(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Reload)

    def home(self):
        self.webEngineView.setUrl(QtCore.QUrl("https://www.walgreens.com/login.jsp?ru=%2F"))

    def goPharm(QDialog):
        pharm = Pharm()
        widget.addWidget(pharm)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class RiteAid(QDialog):
    def __init__(self):
        super(RiteAid, self).__init__()
        loadUi("riteaid.ui", self)
        self.webEngineView.setUrl(QtCore.QUrl("https://www.riteaid.com/signup-signin#login"))
        self.webEngineView.setObjectName("webEngineView")

        self.app.clicked.connect(self.goPharm)
        self.back.clicked.connect(self.backward)
        self.goPage.clicked.connect(self.forward)
        self.re.clicked.connect(self.reload)
        self.homepage.clicked.connect(self.home)

    def backward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def reload(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Reload)

    def home(self):
        self.webEngineView.setUrl(QtCore.QUrl("https://www.riteaid.com/signup-signin#login"))

    def goPharm(QDialog):
        pharm = Pharm()
        widget.addWidget(pharm)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Drug(QDialog):
    def __init__(self):
        super(Drug, self).__init__()
        loadUi("drug.ui", self)
        self.webEngineView.setUrl(QtCore.QUrl("https://www.drugs.com/"))
        self.webEngineView.setObjectName("webEngineView")

        self.app.clicked.connect(self.gotoMedInfo)
        self.back.clicked.connect(self.backward)
        self.goto_2.clicked.connect(self.forward)
        self.re.clicked.connect(self.reload)
        self.homepage.clicked.connect(self.home)

    def backward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def reload(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Reload)

    def home(self):
        self.webEngineView.setUrl(QtCore.QUrl("https://www.drugs.com/"))

    def gotoMedInfo(self):
        medinfo = MedInfo()
        widget.addWidget(medinfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# will inherit from QDialog which is the screen
# This class will take everything from QDialog
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        # loads .ui file into code
        loadUi("login.ui", self)
        # the loginbutton on QDialog (self) will execute accessLogin function when it is clicked
        self.loginbutton.clicked.connect(self.accessLI)
        # self.loginbutton.clicked.connect(self.goMain)
        self.backtoSU.clicked.connect(self.backtoSignUp)
        self.errormessage.setVisible(False)

    # This function will take the email and password
    # nothing happens, just basic logging in screen

    def accessLI(self):
        ea_li = self.ea_lo.text()
        password_li = self.pw_lo.text()
        try:
            self.worker = WorkerThread()
            self.worker.start()
            self.worker.finished.connect(self.imDone)
            self.loginbutton.setEnabled(False)

            auth.sign_in_with_email_and_password(ea_li, password_li)
            mainmenu = MainMenu()
            widget.addWidget(mainmenu)
            widget.setCurrentIndex(widget.currentIndex() + 1)  #####

        except:
            self.errormessage.setVisible(True)

    def imDone(self):
        print("I'm done!!!!!")
        self.loginbutton.setEnabled(True)

    def backtoSignUp(self):
        signup = SignUp()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MainMenu(QDialog):
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi("mainmenu.ui", self)
        self.profilebutton.clicked.connect(self.gotoprofile)
        self.medinfobutton.clicked.connect(self.gotoMedInfo)
        self.loutmain.clicked.connect(self.gotoLoginScreen)
        self.pushButton.clicked.connect(self.gotouserinfo)
        self.load.clicked.connect(self.gotoLoad)

    def gotouserinfo(self):
        userin = InfoShow()
        widget.addWidget(userin)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoprofile(self):
        yourpro = YourProfile()
        widget.addWidget(yourpro)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoMedInfo(self):
        medinfo = MedInfo()
        widget.addWidget(medinfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoLoginScreen(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoLoad(self):
        loadpill = Load()
        widget.addWidget(loadpill)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class YourProfile(QDialog):
    def __init__(self):
        super(YourProfile, self).__init__()
        loadUi("yourprofile.ui", self)
        self.bmain1.clicked.connect(self.gotomain2)
        self.bmain1_2.clicked.connect(self.infoupdate)
        # update prfile button push to firbease with updatePro

    def infoupdate(self):
        ea_user = self.email.text()
        result = db.child("users").order_by_child("User email").equal_to(ea_user).get()
        print(result.val())
        # key=result.val()
        key = str(result.val())
        key2 = key[key.index('[('):key.index('DOB')]
        key3 = key2[3:-5]
        firstname = self.firstname.text()
        lastname = self.lastname.text()
        DOB = self.DOB.text()

        # https://github.com/codefirstio/PyQT5-with-Firebase-Auth-Login-and-Signup-form/blob/master/main.py
        try:
            # create account and push the data to database
            # auth.create_user_with_email_and_password(ea_user,password_user)
            # key = {"Email":ea_user}
            # db.child("users").child(key)
            data = {"First name": firstname, "Last name": lastname, "DOB": DOB}
            db.child("users").child(key3).update(data)
        except:
            print("not right")

    def gotoprofile(self):
        yourpro = YourProfile()
        widget.addWidget(yourpro)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotomain2(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MedInfo(QDialog):
    def __init__(self):
        super(MedInfo, self).__init__()
        loadUi("MedInfo.ui", self)
        self.submit.clicked.connect(self.sendInfo)
        self.backtoMain3.clicked.connect(self.gotomain3)
        self.verifyItsYou.clicked.connect(self.gotoVerify)
        self.DrugInfo.clicked.connect(self.goDrugInfo)
        self.Pharm.clicked.connect(self.goPharm)

        # new button for updating info
        self.pushButton.clicked.connect(self.updateInfo)

    def sendInfo(self):
        # 2/21/22 updating from t1 and m1 to hour and minute and PM

        m1 = self.m1.text()
        h1 = self.h1.text()
        min1 = self.min1.text()
        AmPm = self.ap1.text()
        M2 = self.m2.text()
        M3 = self.m3.text()


        h2 = self.h2.text()
        h3 = self.h3.text()


        MIN2 = self.min2.text()
        MIN3 = self.min3.text()


        AP2 = self.ap2.text()
        AP3 = self.ap3.text()


        if AmPm == "PM":
            h1 = int(h1)
            h1 = h1 + 12
            ho1 = str(h1)

        if AP2 == "PM":
            h2 = int(h2)
            h2 = h2 + 12
            ho2 = str(h2)

        if AP3 == "PM":
            h3 = int(h3)
            h3 = h3 + 12
            ho3 = str(h3)



        if AmPm == "AM":
            h1 = int(h1)
            ho1 = str(h1)

        if AP2 == "AM":
            h2 = int(h2)
            ho2 = str(h2)

        if AP3 == "AM":
            h3 = int(h3)
            ho3 = str(h3)



        ea_user = self.email.text()
        result = db.child("users").order_by_child("User email").equal_to(ea_user).get()
        print(result.val())
        # key=result.val()

        data1 = {"Name1": m1, "Hour1": ho1, "Min1": min1, "PMorAM1": AmPm, "User email": ea_user,"SCount1":"0"}
        data2 = {"Name2": M2, "Hour2": ho2, "Min2": MIN2, "PMorAM2": AP2, "User email": ea_user,"SCount2":"0"}
        data3 = {"Name3": M3, "Hour3": ho3, "Min3": MIN3, "PMorAM3": AP3, "User email": ea_user,"SCount3":"0"}

        db.child("Medication").child("Med1").push(data1)
        db.child("Medication").child("Med2").push(data2)
        db.child("Medication").child("Med3").push(data3)



    def updateInfo(self):
        m1 = self.m1.text()
        h1 = int(self.h1.text())
        min1 = self.min1.text()
        AmPm = self.ap1.text()
        M2 = self.m2.text()
        M3 = self.m3.text()


        h2 = int(self.h2.text())
        h3 = int(self.h3.text())


        MIN2 = self.min2.text()
        MIN3 = self.min3.text()


        AP2 = self.ap2.text()
        AP3 = self.ap3.text()


        if AmPm == "PM":
            h1 = h1 + 12;
            ho1 = str(h1)

        if AP2 == "PM":
            h2 = h2 + 12;
            ho2 = str(h2)

        if AP3 == "PM":
            h3 = h3 + 12;
            ho3 = str(h3)


        if AmPm == "AM":
            ho1 = str(h1)

        if AP2 == "AM":
            ho2 = str(h2)

        if AP3 == "AM":
            ho3 = str(h3)



        ea_user = self.email.text()
        other = db.child("Medication").child("Med1").order_by_child("User email").equal_to(ea_user).get()

        print(other.val())
        # key=result.val()
        key = str(other.val())
        key2 = key[key.index('[('):key.index('Hour1')]
        key3 = key2[3:-5]
        other1 = db.child("Medication").child("Med2").order_by_child("User email").equal_to(ea_user).get()
        print(other1.val())
        # key=result.val()
        key11 = str(other1.val())
        key21 = key11[key11.index('[('):key11.index('Hour2')]
        key31 = key21[3:-5]

        other2 = db.child("Medication").child("Med3").order_by_child("User email").equal_to(ea_user).get()
        print(other2.val())
        # key=result.val()
        key12 = str(other2.val())
        key22 = key12[key12.index('[('):key12.index('Hour3')]
        key32 = key22[3:-5]



        data1 = {"Name1": m1, "Hour1": ho1, "Min1": min1, "PMorAM1": AmPm, "User email": ea_user}
        data2 = {"Name2": M2, "Hour2": ho2, "Min2": MIN2, "PMorAM2": AP2, "User email": ea_user}
        data3 = {"Name3": M3, "Hour3": ho3, "Min3": MIN3, "PMorAM3": AP3, "User email": ea_user}

        db.child("Medication").child("Med1").child(key3).update(data1)
        db.child("Medication").child("Med2").child(key31).update(data2)
        db.child("Medication").child("Med3").child(key32).update(data3)


    def gotoVerify(QDialog):
        verifyYou = Verify()
        widget.addWidget(verifyYou)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotomain3(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goDrugInfo(QDialog):
        drugscom = Drug()
        widget.addWidget(drugscom)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goPharm(QDialog):
        pharm = Pharm()
        widget.addWidget(pharm)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class WorkerThread(QtCore.QThread):
    def run(self):

        while True:

            now = datetime.now()
           
            result1 = db.child("Medication").child("Med1").get()
            result3 = db.child("Medication").child("Med2").get()
            result5 = db.child("Medication").child("Med3").get()
            
            #OrderedDict([('-MzNJwKs0W63OSll0xqv', {'Hour1': '23', 'Min1': '57', 'Name1': 'asd', 'PMorAM1': 'PM', 'User email': 'ywang1@gwmail.gwu.edu'})])
            r1 = str(result1.val())
            r3 = str(result3.val())
            r5 = str(result5.val())
          
            #print(r1)
            r2 = r1.split("'User email': ")
            r4 = r3.split("'User email': ")
            r6 = r5.split("'User email': ")
            l1=len(r2)
            l2=len(r4)
            l3=len(r6)
            current_hour = int(now.strftime("%H"))
            current_min = int(now.strftime("%M"))
            
          
            for x1 in range(1,l1):
                a1 =str(r2[x1])
                #print(a1)
                b1 = a1[a1.index(''):a1.index('}')]
                c1 = b1[1:-1]
                print(c1)
                d1 = db.child("Medication").child("Med1").order_by_child("User email").equal_to(c1).get()
                key = str(d1.val())
                key2 = key[key.index('Hour1'):key.index('Min1')]
                h1 = key2[7:-4]
                key3 = key[key.index('Min1'):key.index('Name1')]
                m1 = key3[8:-4]



                hou1 = ""
                for m in h1:
                    if m.isdigit():
                        hou1 = hou1 + m
                hou1 = int(hou1)
                uHour1 = hou1;
                uMin1 = int(str(m1));
                current_hour = int(now.strftime("%H"))
                current_min = int(now.strftime("%M"))
                num1 = key[key.index('SCount1'):key.index('}')]
                num2 = num1[11:-1]
                for num2 in range(0,8):



                    print("This is " +c1)

                    msg = EmailMessage()
                    # msg.set_content(body)
                    msg['subject'] = "Medication1 needs refill"
                    msg['to'] = c1
                    msg['Hello']

                    user = "encapsulate22@gmail.com"

                    msg['from'] = user

                    password = "ldlsyipkmdjnmxro"
                    # gxfsicsrhpfgrvfw

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(user, password)
                    server.send_message(msg)

                    server.quit()
                    time.sleep(420)

                if (uMin1 == current_min):
                    if (uHour1 == current_hour):
                    
                        t1 = db.child("Medication").child("Med1").order_by_child("Min1").equal_to(str(current_min)).get()
                        print(t1)
                        print(t1.val())
                        work1 = str(t1.val())
                        print("working?")

                        print (work1)
                        find = work1[work1.index("User email"):work1.index("}")]
                        uemail = find[14:-1]
                        print(uemail)
                        msg = EmailMessage()
                # msg.set_content(body)
                        msg['subject'] = "Time to Take Medication"
                        msg['to'] = uemail
                        msg['Hello']

                        user = "encapsulate22@gmail.com"

                        msg['from'] = user

                        password = "ldlsyipkmdjnmxro"
                # gxfsicsrhpfgrvfw

                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(user, password)
                        server.send_message(msg)

                        server.quit()
                        time.sleep(60)
                    
                    
            for x2 in range(1,l2):
                a2 =str(r4[x2])
                #print(a1)
                b2 = a2[a2.index(''):a2.index('}')]
                c2 = b2[1:-1]
                print(c2)
                d2 = db.child("Medication").child("Med2").order_by_child("User email").equal_to(c2).get()
                keyy = str(d2.val())
                keyy2 = keyy[keyy.index('Hour2'):keyy.index('Min2')]
                h2 = keyy2[7:-4]
                keyy3 = keyy[keyy.index('Min2'):keyy.index('Name2')]
                m2 = keyy3[8:-4]

                hou2 = ""
                for m in h2:
                    if m.isdigit():
                        hou2 = hou2 + m
                hou2 = int(hou2)
                print(hou2)
                
                uHour2 = hou2;
                uMin2 = int(str(m2));
                current_hour = int(now.strftime("%H"))
                current_min = int(now.strftime("%M"))
                num12 = keyy[keyy.index('SCount2'):keyy.index('}')]
                num22 = num12[11:-1]
                for num22 in range(0, 8):
                    print("This is " + c2)

                    msg = EmailMessage()
                    # msg.set_content(body)
                    msg['subject'] = "Medication2 needs refill"
                    msg['to'] = c2
                    msg['Hello']

                    user = "encapsulate22@gmail.com"

                    msg['from'] = user

                    password = "ldlsyipkmdjnmxro"
                    # gxfsicsrhpfgrvfw

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(user, password)
                    server.send_message(msg)

                    server.quit()
                    time.sleep(420)

                if (uMin2 == current_min):
                    if (uHour2 == current_hour):
                        t2 = db.child("Medication").child("Med2").order_by_child("Min2").equal_to(str(current_min)).get()
                        print("2")
                        w2 = str(t2.val())
                        find = w2[w2.index("User email"):w2.index("}")]
                        uemail = find[14:-1]
                        print(uemail)
                        msg = EmailMessage()
                # msg.set_content(body)
                        msg['subject'] = "Time to Take Medication"
                        msg['to'] = uemail
                        msg['Hello']

                        user = "encapsulate22@gmail.com"

                        msg['from'] = user

                        password = "ldlsyipkmdjnmxro"
                        # gxfsicsrhpfgrvfw

                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(user, password)
                        server.send_message(msg)

                        server.quit()
                        time.sleep(60)
                    
            for x3 in range(1,l3):
                a3 =str(r6[x3])
                #print(a1)
                b3 = a3[a3.index(''):a3.index('}')]
                c3 = b3[1:-1]
                print(c3)
                d3 = db.child("Medication").child("Med3").order_by_child("User email").equal_to(c3).get()
                ky = str(d3.val())
                ky2 = ky[ky.index('Hour3'):ky.index('Min3')]
                h3 = ky2[7:-4]
                ky3 = ky[ky.index('Min3'):ky.index('Name3')]
                m3 = ky3[8:-4]
                hou3 = ""
                for m in h3:
                    if m.isdigit():
                        hou3 = hou3 + m
                hou3 = int(hou3)
                uHour3 = hou3;
                uMin3 = int(str(m3));

                current_hour = int(now.strftime("%H"))
                current_min = int(now.strftime("%M"))
                num13 = ky[ky.index('SCount3'):ky.index('}')]
                num23 = num13[11:-1]
                for num23 in range(0, 8):
                    print("This is " + c3)

                    msg = EmailMessage()
                    # msg.set_content(body)
                    msg['subject'] = "Medication2 needs refill"
                    msg['to'] = c3
                    msg['Hello']

                    user = "encapsulate22@gmail.com"

                    msg['from'] = user

                    password = "ldlsyipkmdjnmxro"
                    # gxfsicsrhpfgrvfw

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(user, password)
                    server.send_message(msg)

                    server.quit()
                    time.sleep(420)
                
                if (uMin3 == current_min):
                    if (uHour3 == current_hour):
                        print("3")
                        t3 = db.child("Medication").child("Med3").order_by_child("Min3").equal_to(str(current_min)).get()
                        w3 = str(t3.val())
                        find = w3[w3.index("User email"):w3.index("}")]
                        uemail = find[14:-1]
                        print(uemail)
                        msg = EmailMessage()
                        # msg.set_content(body)
                        msg['subject'] = "Time to Take Medication"
                        msg['to'] = uemail
                        msg['Hello']

                        user = "encapsulate22@gmail.com"

                        msg['from'] = user

                        password = "ldlsyipkmdjnmxro"
                        # gxfsicsrhpfgrvfw

                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(user, password)
                        server.send_message(msg)

                        server.quit()
                        time.sleep(60)


                
 
           
            
            
     

            # pulling time from firebase then converting to an integer

            # userHour = db.child("Medication Information").child("-Mxjk5Za6vVJE3H7AD5I").child("Hour 1").get();
            # userMin = db.child("Medication Information").child("-Mxjk5Za6vVJE3H7AD5I").child("Minute 1").get();





##category of "User Account Info" for all users
##category of "UserInfo" for a specific user

# main
# this is for the actual widget
app = QApplication(sys.argv)  # always need this to launch the app, pass command line arguments to it
SIU = SignUp()

# stacking on top of this widget called widget
widget = QStackedWidget()
widget.addWidget(SIU)
widget.setFixedHeight(670)
widget.setFixedWidth(600)
widget.show()

try:
    sys.exit(app.exec_())

except:
    print("Done")
