#all screens represent a class in a python
#the variables are the labels, widgets, etc. PyQt does it for us with loadUi
#source for tutorials: https://www.youtube.com/watch?v=RxGlB9U64fg&list=PLs3IFJPw3G9LTcNjRVR6BSJwUaoj44rCV 

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget

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
class SignUp(QDialog):
    def __init__(self):
        super(SignUp,self).__init__()
        #loads .ui file into code
        loadUi("signup.ui",self)
        #the loginbutton on QDialog (self) will execute accessLogin function when it is clicked
        self.subutton.clicked.connect(self.accessSU)

    #This function will take the email and password
    def accessSU(self):
        ea_user= self.easu.text()
        password_user = self.passwordsu.text()
        auth.create_user_with_email_and_password(ea_user,password_user)
        print("successful creation")

 
##category of "User Account Info" for all users
##category of "UserInfo" for a specific user

#main
#this is for the actual widget
app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
SU = SignUp()

#stacking on top of this widget called widget
widget = QStackedWidget()
widget.addWidget(SU)
widget.setFixedHeight(300)
widget.setFixedWidth(400)
widget.show()

#stacking as many screens on top of each other. one screen leads to another 

try:
    sys.exit(app.exec_())

except:
    print("Done")

