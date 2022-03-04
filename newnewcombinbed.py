import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
import pyrebase

################################
# RPi and Motor Pre-allocations
################################
#
#define GPIO pins
direction= 22 # Direction (DIR) GPIO Pin
step1 = 23 # Step GPIO Pin for motor #1
step2 = 17 # Step pin for motor #2
EN_pin1 = 24 # enable pin (LOW to enable)
EN_pin2 = 27 # emable pin for motor 2

# Declare a instance of class pass GPIO pins numbers and the motor type
motor1 = RpiMotorLib.A4988Nema(direction, step1, (21,21,21), "DRV8825")
motor2 = RpiMotorLib.A4988Nema(direction, step2, (21,21,21), "DRV8825")

GPIO.setup(EN_pin1,GPIO.OUT) # set enable pin as output
GPIO.setup(EN_pin2,GPIO.OUT) # set enable pin as output

###########################
#dispensing
###########################
#def motor1 ():
GPIO.output(EN_pin1,GPIO.LOW) # pull enable to low to enable motor
motor1.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                        "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                     33, # number of steps
                     .0009, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]
print("Motor 1 has been run")
GPIO.output(EN_pin1,GPIO.HIGH) # pull enable to low to enable motor
GPIO.output(EN_pin2,GPIO.LOW) # pull enable to low to enable motor
    

###Lift
#def lifmotor():
motor2.motor_go(False,"Full",3077,.0005,False,.05)

GPIO.output(EN_pin1,GPIO.HIGH) # pull enable to low to enable motor
GPIO.output(EN_pin2,GPIO.HIGH) # pull enable to low to enable motor


print("all complete")

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

#def light():
pin = 5
counter=50 
GPIO.setup(pin,GPIO.IN)

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
                         GPIO.cleanup()
            
                     break
        else:
        
            pass

    
  
except  KeyboardInterrupt:
    GPIO.cleanup()
## verification
    



