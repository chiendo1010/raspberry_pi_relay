#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time
import datetime  
import Adafruit_DHT
  
GPIO.setmode(GPIO.BCM)  
  
# init list with pin numbers  
  
pinList = [17, 18]  
  
# loop through pins and set mode and state to 'low'  
  
for i in pinList:   
  GPIO.setup(i, GPIO.OUT)   
  GPIO.output(i, GPIO.HIGH)  
  
# time to sleep between operations in the main loop  
  
SleepTimeL = 300  
  
# main loop  

def main():
	i = 0
	while True:
		if i < 12:
			GPIO.output(18, GPIO.LOW)  
			print "Fan 1 is running. Fan 2 off"
		else:
		  	GPIO.output(18, GPIO.HIGH)
			print "Fan 1 off. Fan 2 is running"
		
		
		#--------------------------------------------
		humidity, temperature = Adafruit_DHT.read_retry(22, 4)
		print(datetime.datetime.now())
		if humidity is not None and temperature is not None:
			print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		else:
			print('Failed to get reading. Try again!')
		
		print "i = ",i
		i += 1
		time.sleep(SleepTimeL);

		if i > 24:
			i = 0

def destroy():
	GPIO.output(pinList, GPIO.LOW)
	GPIO.cleanup()

try:  
	main()  
except KeyboardInterrupt:  
	# End program cleanly with keyboard 
  	print " Quit"  
  	# Reset GPIO settings  
	destroy()




