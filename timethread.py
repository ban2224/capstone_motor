import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget

from datetime import datetime
import time
from time import sleep

import smtplib
from email.message import EmailMessage



from PyQt5.QtCore import QObject,QThread,pyqtSignal


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




# https://www.youtube.com/watch?v=k5tIk7w50L4   first video watched
# https://www.youtube.com/watch?v=G7ffF0U36b0 second video watched


####just define a time right now and see if it will work that way
uHour = 13;
uMin = 48;

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        #loads .ui file into code
        loadUi("login.ui",self)
        #the loginbutton on QDialog (self) will execute accessLogin function when it is clicked
        self.loginbutton.clicked.connect(self.accessLI)
                
        #self.loginbutton.clicked.connect(self.goMain)
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
        #update prfile button push to firbease with updatePro
  
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
        self.submit.clicked.connect(self.updateInfo)
        self.backtoMain3.clicked.connect(self.gotomain3)
        self.verifyItsYou.clicked.connect(self.gotoVerify)

    def updateInfo(self):
#2/21/22 updating from t1 and m1 to hour and minute and PM
        
        med1 = self.med1.text()
        h1 = self.h1.text()
        min1 = self.min1.text()
        
        data = {"medication 1":med1,"Hour 1":h1,"Minute 1":min1}
        db.child("Medication Information").push(data);
        #push this data
        #Display little thing saying information successfully updated
        #if user has information just replace it

    def gotoVerify(QDialog):
        verifyYou = Verify()
        widget.addWidget(verifyYou)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotomain3(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setCurrentIndex(widget.currentIndex()+1)
          
                  

            
class WorkerThread(QtCore.QThread):
    def run(self):

       
        while True:

            now = datetime.now()



            current_min = int(now.strftime("%M"))
            current_sec = int(now.strftime("%S"))


            #pull from firebase  
        #uhour = int(self.user_hour.text());
        #umin = int(self.user_min.text());
            usec = 00

            userstr = (str(uHour)+":"+str(uMin)+":"+str(usec))

        
            userdiff = datetime.strptime(userstr, "%H:%M:%S")

        
            if (uMin == current_min) == True:
                                
                msg=EmailMessage()
                #msg.set_content(body)
                msg['subject']="Time to Take Medication"
                msg['to'] = "banshoukeir@gwmail.gwu.edu"
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
                            
           


app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
LAST = Login()

#stacking on top of this widget called widget
widget = QStackedWidget()
widget.addWidget(LAST)
#widget.setFixedHeight(550)
#widget.setFixedWidth(400)
widget.show()

try:
    sys.exit(app.exec_())

except:
    print("Done")
