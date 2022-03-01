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
# Snip...

# Step 1: Create a worker class

###

####

now = datetime.now()

current_hour = int(now.strftime("%H"))
current_min = int(now.strftime("%M"))
current_sec = int(now.strftime("%S"))

####just define a time right now and see if it will work that way
uHour = 13;
uMin = 7;



               
class Window(QDialog):
    def __init__(self):
        super(Window,self).__init__()
           #loads .ui file into code
        loadUi("timeCheck.ui",self)
        #self.keepclick.clicked.connect(self.printIt) #connected to 'printIt' function
        #self.notify.clicked.connect(self.myFunction) #when clicked will run the task

        #dictionary
        self.thread = {}
        self.keepclick.clicked.connect(self.printIt) #connected to 'printIt' function
        self.notify.clicked.connect(self.starting) #when clicked will run the task


    def printIt(self):
        print("Click")

    def starting(self):
        self.thread[1] = ThreadClass(parent = None)
        self.thread[1].start() #need to tie this in to the functions that go with the login button
        self.thread[1].any_signal.connect(self.myFunction)
        self.notify.setEnabled(False) #disabled when clicked on this button

    def myFunction(self):
        
        #index = self.sender().index #thread class object 

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
                  

            
class ThreadClass(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent = None):
        super(ThreadClass, self).__init__(parent)
        self.is_running = True
    def run(self):
        print("RUNNING!")
    def stop(self):
        print("Stopping")
        self.terminate()



app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
LAST = Window()

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
