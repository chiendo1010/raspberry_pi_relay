#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time  
import Adafruit_DHT
  
GPIO.setmode(GPIO.BCM)  
  
# init list with pin numbers  
  
pinList = [17, 18]  
  
# loop through pins and set mode and state to 'low'  
  
for i in pinList:   
  GPIO.setup(i, GPIO.OUT)   
  GPIO.output(i, GPIO.HIGH)  
  
# time to sleep between operations in the main loop  
  
SleepTimeL = 2  
  
# main loop  
  
try:  
  GPIO.output(17, GPIO.LOW)  
  print "ONE"  
  time.sleep(SleepTimeL);   
  GPIO.output(18, GPIO.LOW)  
  print "TWO"  
  time.sleep(SleepTimeL);    
  GPIO.cleanup()  
  print "Good bye!"  

  humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	
  if humidity is not None and temperature is not None:
   print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
  else:
   print('Failed to get reading. Try again!')

  
# End program cleanly with keyboard  
except KeyboardInterrupt:  
  print " Quit"  
  
  # Reset GPIO settings  
  GPIO.cleanup()




