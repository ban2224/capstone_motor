#all screens represent a class in a python
#the variables are the labels, widgets, etc. PyQt does it for us with loadUi
#source of tutorials: https://www.youtube.com/watch?v=RxGlB9U64fg&list=PLs3IFJPw3G9LTcNjRVR6BSJwUaoj44rCV

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget

importing raspberrypi 
import RPi.GPIO as GPIO
import time 
import sleep

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


class SignUp(QDialog):
    def __init__(self):
        super(SignUp,self).__init__()
        #loads .ui file into code
        loadUi("signup.ui",self)
        #the loginbutton on QDialog (self) will execute accessLogin function when it is clicked
        self.subutton.clicked.connect(self.accessSU)
        self.subutton.clicked.connect(self.gotomain)

    def accessSU(self):
        ea_user= self.easu.text()
        password_user = self.passwordsu.text()
        auth.create_user_with_email_and_password(ea_user,password_user)
        print("successful creation") 

    def gotomain(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
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
        self.loginbutton.clicked.connect(self.gotomain)
       
    #This function will take the email and password
    def accessLI(self):
        ea_li= self.ea_lo.text()
        password_li = self.pw_lo.text()
        auth.sign_in_with_email_and_password(ea_li,password_li)
        print("Successful login")


    def gotomain(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex()+2) #####
    
    def runMotor(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        aMotorPins = [8, 10, 11, 13]

#IF time == true
    #run motor
# Set all pins as output
        for pin in aMotorPins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

aSequence = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]
        
iNumSteps = len(aSequence)

##if sys.argv[3] == "cw":
iDirection = 1
##else:
##  iDirection = -1

fWaitTime = int(1) / float(1000)

iDeg = int(int(45) * 11.377777777777)

iSeqPos = 0
# If the fourth argument is present, it means that the motor should start at a
# specific position from the aSequence list
if len(sys.argv) > 4:
    iSeqPos = int(sys.argv[4])

# 1024 steps is 90 degrees
# 4096 steps is 360 degrees

        for step in range(0,iDeg):

            for iPin in range(0, 4):
                iRealPin = aMotorPins[iPin]
                if aSequence[iSeqPos][iPin] != 0:
                    GPIO.output(iRealPin, True)
                else:
                    GPIO.output(iRealPin, False)
 
    iSeqPos += iDirection
 
    if (iSeqPos >= iNumSteps):
        iSeqPos = 0
    if (iSeqPos < 0):
        iSeqPos = iNumSteps + iDirection
 
    # Time to wait between steps
    time.sleep(fWaitTime)

for pin in aMotorPins:
    GPIO.output(pin, False)

# Print the position from the aSequence list which should have been the
# next position, if the previous loop was not ended
# Need to catch this output when running from another script

##print (iSeqPos)

    
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
        widget.setCurrentIndex(widget.currentIndex()+2)

    def gotoMedInfo(self):
        medinfo = MedInfo()
        widget.addWidget(medinfo)
        widget.setCurrentIndex(widget.currentIndex()+2)

    def gotoLoginScreen(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+2)

        
class YourProfile(QDialog):
    def __init__(self):
        super(YourProfile,self).__init__()
        loadUi("yourprofile.ui",self)
        self.bmain1.clicked.connect(self.gotomain2)
        #update prfile button push to firbease with updatePro
  
    def gotoprofile(self):
        yourpro = YourProfile()
        widget.addWidget(yourpro)
        widget.setCurrentIndex(widget.currentIndex()+2)

    def gotomain2(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex()+2)


class MedInfo(QDialog):
    def __init__(self):
        super(MedInfo,self).__init__()
        loadUi("MedInfo.ui",self)
        self.refreshMedbutton.clicked.connect(self.updateInfo)
        self.backtoMain3.clicked.connect(self.gotomain3)

    def updateInfo(self):
        med1 = self.m1.text()
        t1 = self.mt1.text()
        med2 = self.m2.text()
        t2 = self.mt2.text()
        med3 = self.m3.text()
        t3 = self.mt3.text()
        med4 = self.m4.text()
        t4 = self.mt4.text()
        data = {"medication 1":med1,"time 1":t1,"medication 2":med2,"time 2":t2};
        db.child("Medication Information").push(data);
        #push this data
        #Display little thing saying information successfully updated
        #if user has information just replace it
    
    def gotomain3(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex()+2)





    



 
##category of "User Account Info" for all users
##category of "UserInfo" for a specific user

#main
#this is for the actual widget
app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
SIU= SignUp()

#stacking on top of this widget called widget
widget = QStackedWidget()
widget.addWidget(SIU)
#widget.setFixedHeight(300)
#widget.setFixedWidth(300)
widget.show()

try:
    sys.exit(app.exec_())

except:
    print("Done")
