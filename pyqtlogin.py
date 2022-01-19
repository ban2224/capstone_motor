#all screens represent a class in a python
#the variables are the labels, widgets, etc. PyQt does it for us with loadUi
#source of tutorials: https://www.youtube.com/watch?v=RxGlB9U64fg&list=PLs3IFJPw3G9LTcNjRVR6BSJwUaoj44rCV

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget

#importing raspberrypi 
import RPi.GPIO as GPIO
import time import sleep

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


#will inherit from QDialog which is the screen
#This class will take everything from QDialog
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        #loads .ui file into code
        loadUi("login.ui",self)
        #the loginbutton on QDialog (self) will execute accessLogin function when it is clicked
        self.loginbutton.clicked.connect(self.accessLI)

    #This function will take the email and password
    def accessLI(self):
        ea_li= self.ea_lo.text()
        password_li = self.pw_lo.text()
        auth.sign_in_with_email_and_password(ea_li,password_li)
        print("Successful login")

        # set up GPIO pins
        GPIO.setup(7, GPIO.OUT) # Connected to PWMA
        GPIO.setup(11, GPIO.OUT) # Connected to AIN2


# Drive the motor clockwise
        print("Clockwise")
        GPIO.output(11, GPIO.LOW) # Set AIN2

# Set the motor speed
        GPIO.output(7, GPIO.HIGH) # Set PWMA


# Wait 5 seconds
        print("wait 5 seconds")
        time.sleep(5)

# Drive the motor counterclockwise
        print("counterclockwise")
    
        GPIO.output(11, GPIO.HIGH) # Set AIN2

# Set the motor speed
        GPIO.output(7, GPIO.HIGH) # Set PWMA



# Wait 5 seconds
        print("wait 5 seconds")
        time.sleep(5)

# Reset all the GPIO pins by setting them to LOW

        GPIO.output(11, GPIO.LOW) # Set AIN2
        GPIO.output(7, GPIO.LOW) # Set PWMA

 
##category of "User Account Info" for all users
##category of "UserInfo" for a specific user

#main
#this is for the actual widget
app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
LI = Login()

#stacking on top of this widget called widget
widget = QStackedWidget()
widget.addWidget(LI)
widget.setFixedHeight(300)
widget.setFixedWidth(400)
widget.show()

try:
    sys.exit(app.exec_())

except:
    print("Done")
