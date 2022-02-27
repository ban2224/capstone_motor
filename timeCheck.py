import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget

from datetime import datetime
import time
from time import sleep

import smtplib
from email.message import EmailMessage









class LastIdea(QDialog):
    def __init__(self): 
        super(LastIdea,self).__init__()

        loadUi("timeCheck.ui",self)
        
        #object button name is submit 
        self.notify.clicked.connect(self.checkTime)
        self.keepclick.clickedconnect(self.printIt)

    def printIt(self):
        print("Click")
        

    def checkTime(self):


        while True:

            now = datetime.now()

            current_hour = int(now.strftime("%H"))
            if current_hour < 12:
                current_hour = current_hour + 12
                
            current_min = int(now.strftime("%M"))
            current_sec = int(now.strftime("%S"))


            #pull from firebase  
            uhour = int(self.user_hour.text());
            umin = int(self.user_min.text());
            usec = 00

            userstr = (str(uhour)+":"+str(umin)+":"+str(usec))
            userdiff = datetime.strptime(userstr, "%H:%M:%S")

            
            if int(userdiff.strftime("%M")) == current_min and int(userdiff.strftime("%H")) == current_hour:

                                
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
                #keep running
                print("")
                time.sleep(1)

                


app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
LAST = LastIdea()

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
