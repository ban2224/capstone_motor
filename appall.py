# -*- coding: utf-8 -*-
#all screens represent a class in a python
#the variables are the labels, widgets, etc. PyQt does it for us with loadUi
#source of tutorials: https://www.youtube.com/watch?v=RxGlB9U64fg&list=PLs3IFJPw3G9LTcNjRVR6BSJwUaoj44rCV

#NOTE
#firebase replacing data and refreshing information
#extract information ---> instead input it
#have button to go to login page if already signed up on sign in page?
#All information needs to be saved in that account


#push data: https://github.com/codefirstio/Python-Firebase-Realtime-Database-CRUD-Series/blob/master/createdata.py 

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage



from datetime import datetime
import time
from time import sleep

import smtplib
from email.message import EmailMessage

from PyQt5.QtCore import QObject,QThread,pyqtSignal

#importing raspberrypi 
#import RPi.GPIO as GPIO
#import time import sleep

import pyrebase

#need to import pyrebase
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

   
  


class SignUp(QDialog):
    def __init__(self):
        super(SignUp,self).__init__()
        #loads .ui file into code
        loadUi("signup.ui",self)
        #the loginbutton on QDialog (self) will execute accessLogin function when it is clicked
        self.subutton.clicked.connect(self.accessSU)
        self.ihaveacct_button.clicked.connect(self.HaveAnAcct)

        self.errormessage.setVisible(False)
        self.errormessage2.setVisible(False)

        #button for already have an account, different Login screen than verification screen

    def accessSU(self):
        ea_user= self.easu.text()
        password_user = self.passwordsu.text()
        firstname = self.firstname.text()
        lastname = self.lastname.text()
        DOB = self.DOB.text()

        #https://github.com/codefirstio/PyQT5-with-Firebase-Auth-Login-and-Signup-form/blob/master/main.py
        try:
            #create account and push the data to database
            auth.create_user_with_email_and_password(ea_user,password_user)
            #key = {"Email":ea_user}
            #db.child("users").child(key)
            data = {"First name": firstname,"Last name": lastname, "DOB": DOB}
            db.child("users").push(data)
         



            mainmenu = MainMenu()
            widget.addWidget(mainmenu)
            widget.setCurrentIndex(widget.currentIndex()+1)

        except:
            if len(password_user) <= 6:
                self.errormessage2.setVisible(True)
                self.errormessage.setVisible(False)
            else:
                self.errormessage.setVisible(True)
                self.errormessage2.setVisible(False)
            #need to add condition for both, extract data from firebase?
            #it'll show both separaetely if the ocnditions don't fit

    def HaveAnAcct(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Verify(QDialog):
    def __init__(self):
        super(Verify,self).__init__()
        loadUi("verify.ui",self)
        #self.verifybutton.clicked.connect(self.runMotor)
        #self.verifybutton.clicked.connect(self.runSensor)
        self.backtoMain2.clicked.connect(self.gotomain)

    #def runMotor, all the stuff for the motor
    #if info is right, just one click and dispense, if not, try again
    def runMotor(self):
        ea_li= self.ea_lo.text()
        password_li = self.pw_lo.text()
        auth.sign_in_with_email_and_password(ea_li,password_li)
        print("Successful verification")

           


        #put motor code

    def gotomain(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class Pharm(QDialog):
    def __init__(self):
        super(Pharm,self).__init__()
        loadUi("pharm.ui",self)
        self.cvs.clicked.connect(self.show_cvs)
        self.wal.clicked.connect(self.show_wal)
        self.rite.clicked.connect(self.show_rite)
        self.app.clicked.connect(self.gotoMedInfo)
    
    def show_cvs(QDialog):
        cvspage = CVSpage ()
        widget.addWidget(cvspage)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def show_wal(QDialog):
        walgreen = Walgreen ()
        widget.addWidget(walgreen)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def show_rite(QDialog):
        riteaid = RiteAid ()
        widget.addWidget(riteaid)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoMedInfo(self):
        medinfo = MedInfo()
        widget.addWidget(medinfo)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class CVSpage(QDialog):
    def __init__(self):
        super(CVSpage,self).__init__()
        loadUi ("cvs.ui",self)
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
        pharm = Pharm ()
        widget.addWidget(pharm)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Walgreen(QDialog):
    def __init__(self):
        super(Walgreen,self).__init__()
        loadUi ("walgreens.ui",self)
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
        pharm = Pharm ()
        widget.addWidget(pharm)
        widget.setCurrentIndex(widget.currentIndex()+1)

class RiteAid(QDialog):
    def __init__(self):
        super(RiteAid,self).__init__()
        loadUi ("riteaid.ui",self)
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
        pharm = Pharm ()
        widget.addWidget(pharm)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Drug(QDialog):
    def __init__(self):
        super(Drug,self).__init__()
        loadUi ("drug.ui",self)
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
        widget.setCurrentIndex(widget.currentIndex()+1)


#will inherit from QDialog which is the screen
#This class will take everything from QDialog
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        #loads .ui file into code
        loadUi("login.ui",self)
        #the loginbutton on QDialog (self) will execute accessLogin function when it is clicked
        self.loginbutton.clicked.connect(self.accessLI)
        #self.loginbutton.clicked.connect(self.goMain)
        self.backtoSU.clicked.connect(self.backtoSignUp)
        self.errormessage.setVisible(False)
    #This function will take the email and password
    #nothing happens, just basic logging in screen

    def accessLI(self):
        ea_li= self.ea_lo.text()
        password_li = self.pw_lo.text()
        try:
            self.worker = WorkerThread()
            self.worker.start()
            self.worker.finished.connect(self.imDone)
            self.loginbutton.setEnabled(False)

            auth.sign_in_with_email_and_password(ea_li,password_li)
            mainmenu = MainMenu()
            widget.addWidget(mainmenu)
            widget.setCurrentIndex(widget.currentIndex()+1) #####

        except:
            self.errormessage.setVisible(True)

    def imDone(self):
        print("I'm done!!!!!")
        self.loginbutton.setEnabled(True)
       
    def backtoSignUp(self):
        signup = SignUp()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)

   
    
class MainMenu(QDialog):
    def __init__(self):
        super(MainMenu,self).__init__()
        loadUi("mainmenu.ui",self)
        self.profilebutton.clicked.connect(self.gotoprofile)
        self.medinfobutton.clicked.connect(self.gotoMedInfo)
        self.loutmain.clicked.connect(self.gotoLoginScreen)


    def gotoprofile(self):
        yourpro = YourProfile()
        widget.addWidget(yourpro)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoMedInfo(self):
        medinfo = MedInfo()
        widget.addWidget(medinfo)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoLoginScreen(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

        
class YourProfile(QDialog):
    def __init__(self):
        super(YourProfile,self).__init__()
        loadUi("yourprofile.ui",self)
        self.bmain1.clicked.connect(self.gotomain2)
        self.bmain1_2.clicked.connect(self.infoupdate)
        #update prfile button push to firbease with updatePro
    
    def infoupdate(self):
        
        firstname = self.firstname.text()
        lastname = self.lastname.text()
        DOB = self.DOB.text()

        #https://github.com/codefirstio/PyQT5-with-Firebase-Auth-Login-and-Signup-form/blob/master/main.py
        try:
            #create account and push the data to database
            #auth.create_user_with_email_and_password(ea_user,password_user)
            #key = {"Email":ea_user}
            #db.child("users").child(key)
            data = {"First name": firstname,"Last name": lastname, "DOB": DOB}
            db.child("users").child("-MxjjptBWfzNItImoJY3").update(data)
        except:
            print("not right")
         
  
    def gotoprofile(self):
        yourpro = YourProfile()
        widget.addWidget(yourpro)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotomain2(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class MedInfo(QDialog):
    def __init__(self):
        super(MedInfo,self).__init__()
        loadUi("MedInfo.ui",self)
        self.submit.clicked.connect(self.sendInfo)
        self.backtoMain3.clicked.connect(self.gotomain3)
        self.verifyItsYou.clicked.connect(self.gotoVerify)
        self.DrugInfo.clicked.connect(self.goDrugInfo)
        self.Pharm.clicked.connect(self.goPharm)

        #new button for updating info
        self.pushButton.clicked.connect(self.updateInfo)
        
    def sendInfo(self):
#2/21/22 updating from t1 and m1 to hour and minute and PM
        
        m1 = self.m1.text()
        h1 = int(self.h1.text())
        min1 = self.min1.text()
        AmPm = self.ap1.text();

        if AmPm == "PM":
            h1 = h1 + 12;


        
        data = {"medication 1":m1,"Hour 1":h1,"Minute 1":min1}
        db.child("Medication Information").push(data);
        #push this data
        #Display little thing saying information successfully updated
        #if user has information just replace it

    def updateInfo(self):
        m1 = self.m1.text()
        h1 = int(self.h1.text())
        min1 = self.min1.text()

        AmPm = self.ap1.text();

        if AmPm == "PM":
            h1 = h1 + 12;



        data = {"medication 1":m1,"Hour 1":h1,"Minute 1":min1}
        db.child("Medication Information").child("-Mxjk5Za6vVJE3H7AD5I").update(data);





    def gotoVerify(QDialog):
        verifyYou = Verify()
        widget.addWidget(verifyYou)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotomain3(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goDrugInfo(QDialog):
        drugscom = Drug ()
        widget.addWidget(drugscom)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goPharm(QDialog):
        pharm = Pharm ()
        widget.addWidget(pharm)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

class WorkerThread(QtCore.QThread):
    def run(self):

       
        while True:

            now = datetime.now()


             #pulling time from firebase then converting to an integer


            userHour = db.child("Medication Information").child("-Mxjk5Za6vVJE3H7AD5I").child("Hour 1").get();
            userMin = db.child("Medication Information").child("-Mxjk5Za6vVJE3H7AD5I").child("Minute 1").get();

           
            uHour = int(str(userHour.val()));
            uMin = int(str(userMin.val()));



            current_hour= int(now.strftime("%H"))
            current_min = int(now.strftime("%M"))
            

            usec = 00

            userstr = (str(uHour)+":"+str(uMin)+":"+str(usec))

        
            userdiff = datetime.strptime(userstr, "%H:%M:%S")

        
            if (uMin == current_min) == True:
                                
                msg=EmailMessage()
                #msg.set_content(body)
                msg['subject']="Time to Take Medication"
                msg['to'] = "banshoukeir@gwu.edu"
                msg['Hello']


                user = "encapsulate22@gmail.com"

                msg['from']=user
                
                password="ldlsyipkmdjnmxro"
#gxfsicsrhpfgrvfw

                server=smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(user, password)
                server.send_message(msg)

                server.quit()
                break

            else:
                time.sleep(1)


    



 
##category of "User Account Info" for all users
##category of "UserInfo" for a specific user

#main
#this is for the actual widget
app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
SIU= SignUp()

#stacking on top of this widget called widget
widget = QStackedWidget()
widget.addWidget(SIU)
#widget.setFixedHeight(600)
#widget.setFixedWidth(550)
widget.show()

try:
    sys.exit(app.exec_())

except:
    print("Done")
