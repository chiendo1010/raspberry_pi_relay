#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
import Adafruit_DHT

import json
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN  = 4

# time to sleep between operations in the main loop
SLEEP_TIME = 1200    #20 minutes
TIME_RUNNING_EACH_FAN = 3600/SLEEP_TIME #Each hour, the fan will be changed.
TIME_RESET_COUNTER = 7200/SLEEP_TIME
HOT_TEMPERATURE = 32

GPIO.setmode(GPIO.BCM)

# init list with pin numbers
FAN_WALL = 17  #Fan on wall
FAN_BOX = 18  #Fan in box
pinList = [FAN_WALL, FAN_BOX]

GDOCS_OAUTH_JSON       = 'PythonUpdateDrive-d0c1bcd626be.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'TemperatureInMiningHouse'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 30


# loop through pins and set mode and state to 'low'
for i in pinList:
  GPIO.setup(i, GPIO.OUT)
  GPIO.output(i, GPIO.HIGH)


def login_open_sheet(oauth_key_file, spreadsheet):
    while True:
        """Connect to Google Docs spreadsheet and return the first worksheet."""
        try:
            # scope =  ['https://spreadsheets.google.com/feeds']
            scope=[
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
            gc = gspread.authorize(credentials)
            worksheet = gc.open(spreadsheet).sheet1
            return worksheet
        except Exception as ex:
            print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
            print('Google sheet login failed with error:', ex)
            sleep(10)
        pass



# main loop

def main():
    i = 0
    worksheet = None
    print('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, SLEEP_TIME))
    print('Press Ctrl-C to quit.')
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
        if humidity is None or temperature is None:
            time.sleep(2)
            continue

        CurrentTime = str(datetime.datetime.now())
        CurrentTime = CurrentTime[:-7]
        print(CurrentTime + ' -- Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

        #if temperature > 32.5 or humidity > 90:
        if temperature > HOT_TEMPERATURE:
            GPIO.output(FAN_WALL, GPIO.LOW)
            print('Temp or Humidity is too high. Starting FAN_WALL')
        else:
            GPIO.output(FAN_WALL, GPIO.HIGH)

        # Login if necessary.
        if worksheet is None:
            worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        # Append the data in the spreadsheet, including a timestamp
        try:
            temperature = float("{0:.2f}".format(temperature))
            humidity = float("{0:.2f}".format(humidity))
            worksheet.append_row((CurrentTime, temperature, humidity))
        except:
            # Error appending data, most likely because credentials are stale.
            # Null out the worksheet so a login is performed at the top of the loop.
            print('Append error, logging in again')
            worksheet = None
            # time.sleep(FREQUENCY_SECONDS)
            # continue

        # Wait 30 seconds before continuing
        # print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))

        time.sleep(SLEEP_TIME);
        i += 1
        print('-----------')
        if i >= TIME_RESET_COUNTER:
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
