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


# https://www.youtube.com/watch?v=k5tIk7w50L4   first video watched
# https://www.youtube.com/watch?v=G7ffF0U36b0 second video watched


####just define a time right now and see if it will work that way
uHour = 13;
uMin = 56;



               
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
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.finished.connect(self.imDone)
        self.notify.setEnabled(False)

    def imDone(self):
        print("I'm done!!!!!")
        self.notify.setEnabled(True)

        
          
                  

            
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
