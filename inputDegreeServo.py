import RPi.GPIO as GPIO
import time

#Set GIPIO numbering mode
GPIO.setmode(GPIO.BOARD)

#Se pin 11 as output, and define as servo1 as PWM pin
GPIO.setup(17, GPIO.OUT)
servo1 = GPIO.PWN(17,50) # pin 11 for servo1, pulse 50hz

#Start PWN running, with value of 0 (pulls off)
servo1.start(0)

#Loop to allow user to set servo angle. Try/finally allows exit
#With execution of servo.stop and GPIO cleanup
try: 
  while True:
    #Ask user for angle and turn servo to it
    angle = float(input('Enter angle between 0 & 180: '))
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

finally: 
  #Clean things up at the end
  servo1.stop()
  GPIO.cleanup()
  print("Goodbye")



