import RPi.GPIO as GPIO
import time
from collections import Counter
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pin =7
counter=50 
GPIO.setup(pin,GPIO.IN)
total=50

try:
    while True:
        if GPIO.input(pin) >=1:
            #print("Light off")
            time.sleep(.05)
           
          
            tend=time.time() +1*1
            while time.time() < tend:
                 i=GPIO.input(pin)
                 if i==True:
                     counter=counter-1
                     print(counter)
                     break
                     if counter==0:
                         exit()
            
            
            #GPIO.cleanup()
            
           # count=count+1
            #print(count)
            #totalP=total-count
 
        else:
        
            pass
            
        
            
            #GPIO.cleanup()

except  KeyboardInterrupt:
    GPIO.cleanup()
