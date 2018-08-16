#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
import Adafruit_DHT


# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN  = 4

# time to sleep between operations in the main loop

SLEEP_TIME = 600    #10 minutes
TIME_RUNNING_EACH_FAN = 3600/SLEEP_TIME #Each hour, the fan will be changed.
TIME_RESET_COUNTER = 7200/SLEEP_TIME
HOT_TEMPERATURE = 32

GPIO.setmode(GPIO.BCM)

# init list with pin numbers
FAN_WALL = 17  #Fan on wall
FAN_BOX = 18  #Fan in box
pinList = [FAN_WALL, FAN_BOX]

# loop through pins and set mode and state to 'low'

for i in pinList:
  GPIO.setup(i, GPIO.OUT)
  GPIO.output(i, GPIO.HIGH)


# main loop

def main():
    i = 0
    while True:
        if i < TIME_RUNNING_EACH_FAN:
            GPIO.output(FAN_BOX, GPIO.LOW)
            print "i= " ,i, ", Fan 1 is running. Fan 2 off"
        else:
            GPIO.output(FAN_BOX, GPIO.HIGH)
            print "i= " ,i, ", Fan 1 off. Fan 2 is running"

        #--------------------------------------------
        humidity, temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)
        # time.sleep(2);
        # humidity, temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)

        # Skip to the next reading if a valid measurement couldn't be taken.
        # This might happen if the CPU is under a lot of load and the sensor
        # can't be reliably read (timing is critical to read the sensor).
        if humidity is None or temp is None:
            time.sleep(2)
            continue

        CurrentTime = str(datetime.datetime.now())
        print(CurrentTime + ' -- Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

        #if temperature > 32.5 or humidity > 90:
        if temperature > HOT_TEMPERATURE:
            GPIO.output(FAN_WALL, GPIO.LOW)
            print('Temp or Humidity is too high. Starting FAN_WALL')
        else:
            GPIO.output(FAN_WALL, GPIO.HIGH)

        i += 1    #Test
        time.sleep(SLEEP_TIME);
        print('-----------')
        if i > TIME_RESET_COUNTER:
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
