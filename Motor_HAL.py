import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
import pyrebase

# import sys
# from PyQt5.uic import loadUi
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget
import pyrebase
firebaseConfig=firebaseConfig = {
  'apiKey': "AIzaSyDFcKZxM45qSe9DmtSPoUwwVYilclTouKs",
  'authDomain': "capstone-project-6325f.firebaseapp.com",
  'databaseURL': "https://capstone-project-6325f-default-rtdb.firebaseio.com",
  'projectId': "capstone-project-6325f",
  'storageBucket': "capstone-project-6325f.appspot.com",
  'messagingSenderId': "463650994151",
  'appId': "1:463650994151:web:62f7742b008e5485726f42",
  'measurementId': "G-E88E98P34S"
};
firebase=pyrebase.initialize_app(firebaseConfig)



db=firebase.database()
#
#define GPIO pins
direction= 22 # Direction (DIR) GPIO Pin

# Step pins
step1 = 23
step2 = 17
step3 = 4
step4 = 6

# Enable pins (LOW to enable)
EN_pin1 = 24
EN_pin2 = 27
EN_pin3 = 12
EN_pin4 = 13

# Declare a instance of class pass GPIO pins numbers and the motor type
motor1 = RpiMotorLib.A4988Nema(direction, step1, (21,21,21), "DRV8825")
motor2 = RpiMotorLib.A4988Nema(direction, step2, (21,21,21), "DRV8825")
motor3 = RpiMotorLib.A4988Nema(direction, step3, (21,21,21), "DRV8825")
motor4 = RpiMotorLib.A4988Nema(direction, step4, (21,21,21), "DRV8825")


# Setup enable pins as output
GPIO.setup(EN_pin1,GPIO.OUT)
GPIO.setup(EN_pin2,GPIO.OUT)
GPIO.setup(EN_pin3,GPIO.OUT)
GPIO.setup(EN_pin4,GPIO.OUT)


################################
# RPi and Motor Pre-allocations
################################
# class Main(QDialog):
#     def __init__():
#         super(Main,self).__init__()
#         #loads .ui file into code
#         loadUi("Dispensepage.ui",self)
#         self.verifybutton.clicked.connect(self.runSensor)
#         #self.pushButton.clicked.connect(self.RunMotors)
#         self.pushButton.clicked.connect(self.rotate(1,True))
#         

#     def runMotor(self):


#############################
# Motor 1 is for level select, 2,3, and 4 are for levels 1,2,and 3
#############################

#############################
# move_to_level(level)
# - Move to the desired level (integer)
# rotate(level, load)
# # - rotate the desired level (integer) in load (true), unload (false) direction
# #
# #############################
# 

Cur_level = 0
Steps_level = 3077
Step_delay = 0.001
Initial_delay = 0.05
Stepping = "Full"

Steps_rot = 71
Step_delay_rot = 0.005

def en_motor(motor):
    print("Enabling motor " + str(motor))
    if motor == 1:
        GPIO.output(EN_pin1,GPIO.LOW)
    elif motor == 2:
        GPIO.output(EN_pin2,GPIO.LOW)
    elif motor == 3:
        GPIO.output(EN_pin3,GPIO.LOW)
    elif motor == 4:
        GPIO.output(EN_pin4,GPIO.LOW)

def disable_motors():
    print("Disabling all Motors")
    GPIO.output(EN_pin1,GPIO.HIGH)
    GPIO.output(EN_pin2,GPIO.HIGH)
    GPIO.output(EN_pin3,GPIO.HIGH)
    GPIO.output(EN_pin4,GPIO.HIGH)


def move_to_level(level):
    Cur_level=1
    
    if Cur_level == level:
        return
    elif Cur_level > level:
        en_motor(1)
        move_up(Cur_level - level)
        print("Moving to level: " + str(level))
    elif Cur_level < level:
        en_motor(1)
        move_down(level - Cur_level)
        print("Moving to level: " + str(level))
    
    disable_motors()

def move_up(levels):
    motor1.motor_go(False,Stepping,Steps_level,Step_delay,False,Initial_delay)


def move_down(levels):
    motor1.motor_go(True,Stepping,Steps_level,Step_delay,False,Initial_delay)


def rotate(level, load):
    print("Rotating motor " + str(level + 1))
    if level == 1:
        en_motor(2)
        motor2.motor_go(load,Stepping,Steps_rot,Step_delay_rot,False,Initial_delay)

    elif level == 2:
        en_motor(3)
        motor3.motor_go(load,Stepping,Steps_rot,Step_delay_rot,False,Initial_delay)

    elif level == 3:
        en_motor(4)
        motor4.motor_go(load,Stepping,Steps_rot,Step_delay_rot,False,Initial_delay)
    disable_motors()

###########################
# Motor and Function Testing
###########################
#def dispense():
data2 = db.child("Count").child("Level").get()
#data2=db.{"level":level}
data3 = int(str(data2.val()))
print(data3)

if data3==1:
    move_to_level(1)
    rotate(1,True)
    move_to_level(1)
    
data4 = db.child("Count").child("Level2").get()
#data2=db.{"level":level}
data5 = int(str(data2.val()))
print(data5)

if data5==1:
    move_to_level(1)
    rotate(1,True)
    move_to_level(1)

data6 = db.child("Count").child("Level3``").get()
#data2=db.{"level":level}
data6 = int(str(data2.val()))
print(data5)

if data6==1:
    move_to_level(1)
    rotate(1,True)
    move_to_level(1)
#move_to_level(2)

def Load():
    data2 = db.child("Count").child("Level").get()
    #data2=db.{"level":level}
    data3 = int(str(data2.val()))
    print("level:")
    print(data3)

    if data3==1:
        move_to_level(1)
        rotate(1,False)
      #data=db.child("slot").get()
# #     
       

#pull the current slot count from firebase
slotn=db.child("slot").child("slot").get()
#convert it to an integer 
slotne=int(str(slotn.val()))

#the if statement checks its value, and will decrement and update if it is between 1 and 20
# if the current slot number is 0, it will not update and notify the user that the slots are empty
if slotne<=20 and slotne>=1:
#     slotinitial=db.child("slot").child("slot").get();
#     slotnew=int(str(slotinitial.val()))
    
#     slotnew=int(str(slotinitial.val()))
     slotnewnew=slotne-1
#     print(slotnewnew)
    
#   #data=db.child("slot").get()
     data={"slot":slotnewnew}
     db.child("slot").update(data)


else:
    print("Slot empty, please go to loading page and refill")
 
#         data={"slot":slotne}
#         db.child("slot").update(data)
#         print(data) 
#         #slot=slot-1
#         #Load()
#         time.sleep(1)
#         #print(slot)
#         data1 = int(data)
#         if slotne<0:
#             break
#     
                  
    
        
    
        


# slotinitial=db.child("slot").child("slot").get();
#     
# slotnew=int(str(slotinitial.val()))
# slotnewnew=slotnew-1
# print(slotnewnew)
# #     #data=db.child("slot").get()
# #   #data=db.child("slot").get()
# #     
# data={"slot":slotnewnew}
# db.child("slot").update(data)
# print(data)    
# 
# 
# 
# #GPIO.setmode(GPIO.BOARD)
pin = 5
GPIO.setup(pin,GPIO.IN)


def lightsensor():
    counter=50     
    try:
    #if passowrd is correct &&corect
    #run motor
        while True:
            if GPIO.input(pin) >=1:
                time.sleep(.05)
                 
           
                tend=time.time() +1*1
                while time.time() < tend:
                        i=GPIO.input(pin)
                        if i==True:
                            counter=counter-1
                            db.child("Count")
                            data={"count":counter}
                            db.update(data)
            
                            print(counter)
                            if counter==0:
                                print('slot is empty, needs to refill pills')
                                #GPIO.cleanup()
                     #check=input("yes")
                     #v=yes
                     #if check==v:
                         #continue
                     #else:
                         #Break 
                     
                     #passwordgaian
                     #run motor again 
                            break
                            if counter==0:
                                print('slot is empty, needs to refill pills')
                                #GPIO.cleanup()
            
                            break
            else:
        
                pass



    except  KeyboardInterrupt:
            GPIO.cleanup()
# 
# 

#def light():



# app = QApplication(sys.argv) #always need this to launch the app, pass command line arguments to it
# MW= Main()
# 
# #stacking on top of this widget called widget
# widget = QStackedWidget()
# widget.addWidget(MW)
# widget.setFixedHeight(550)
# widget.setFixedWidth(500)
# widget.show()
# 
# try:
#     sys.exit(app.exec_())
# 
# except:
#     print("Done")
#     GPIO.cleanup()

