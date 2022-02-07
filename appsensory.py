import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget


import RPi.GPIO as GPIO
import time 
from collections import Counter

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



class UserProfile(QDialog):
    def __init__(self):
        super(UserProfile,self).__init__()
        
        loadUi("profile.ui",self)
        self.refreshbu.clicked.connect(self.sensorInitiate)
        
                
         
   # def pushData(self):
   #     med_name = self.medname.text()
   #     med_num = self.mednum.text()
   #     data = {"Medication name":med_name, "Number of pills":med_num}
   #     db.child("user").push(data)

    def sensorInitiate(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        

        pin =7
        counter=50 
        GPIO.setup(7,GPIO.IN)
        

        try:
            while True:
                if GPIO.input(7) >=1:
                    time.sleep(.05)
           
                    tend=time.time() +1*1
                    while time.time() < tend:
                         i=GPIO.input(7)
                         if i==True:
                             counter=counter-1
                             print(counter)
                             if counter==0:
                                 print('slot is empty, needs to refill pills')
                                 GPIO.cleanup()
            
                             break
                else:
        
                    pass
  
        except  KeyboardInterrupt:
            GPIO.cleanup()
    
        
        
       



app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
UP = UserProfile()

#stacking on top of this widget called widget
widget = QStackedWidget()
widget.addWidget(UP)
widget.setFixedHeight(300)
widget.setFixedWidth(400)
widget.show()



try:
    sys.exit(app.exec_())

except:
    print("Done")
