#!/usr/bin/python
import sys
import time
import RPi.GPIO as GPIO
from datetime import datetime
 
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

iDeg = int(int(360) * 11.377777777777)

iSeqPos = 0
# If the fourth argument is present, it means that the motor should start at a
# specific position from the aSequence list
if len(sys.argv) > 4:
    iSeqPos = int(sys.argv[4])
    print('movoing')

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
pin =7
counter=50 
GPIO.setup(pin,GPIO.IN)

try:
    while True:
        if GPIO.input(pin) >=1:
            time.sleep(.1)
           
            tend=time.time() +1*1
            while time.time() < tend:
                 i=GPIO.input(pin)
                 if i==True:
                     if iRealPin == aMotorPins[iPin]:
                        
                         print('Motor ran and light works')
                        
                         yes=str(input('Did you get your pill? Input yes or no. \n'))
                         valid="yes" or"Yes"
                         if yes==valid:
                              now=datetime.now()
                              counter=counter-1
                              print("Pill count is:", counter)
                              current_time=now.strftime("%H:%M:%S:")
                              print("Pill is dispenses at", current_time)
                              exit
                         elif yes!=valid:
                                print("Error in system run again")
                         if counter==0:
                             print('slot is empty, needs to refill pills')
                             GPIO.cleanup()
                      
          
                         
                     break
            else:
          
                pass
        
    
except  KeyboardInterrupt:
    GPIO.cleanup()
    
    

    

    

