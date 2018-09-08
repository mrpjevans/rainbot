#!/usr/bin/env python3

##############################################################################
# A script to read inputs from a rain sensor and send an alert if it rains   #
# using Pushover.                                                            #
#                                                                            #
# By PJ Evans (@mrpjevans)                                                   #
# Original pushover function by Wesley Archer (@raspberrycoulis)             #
# https://mrpjevans.com/                                                     #
##############################################################################

from gpiozero import DigitalInputDevice
from time import sleep
import http.client, urllib.parse

# Some setup first:
APP_TOKEN = 'YOUR_PUSHOVER_APP_TOKEN'    # The app token - required for Pushover
USER_TOKEN = 'YOUR_PUSHOVER_USER_TOKEN'   # Ths user token - required for Pushover

# Set up our digital input and assume it's not currently raining
rainSensor = DigitalInputDevice(17)
dryLastCheck = True

# Send the pushover alert
def pushover(message):
    print(message)
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": APP_TOKEN,                         # Insert app token here
        "user": USER_TOKEN,                         # Insert user token here
        "title": "Rain Detector",
        "message": message,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# Loop forever
while True:

    # Get the current reading
    dryNow = rainSensor.value
    print("Sensor says: " + str(dryNow))

    if dryLastCheck and not dryNow:

        pushover("It's Raining!")
        
    elif not dryLastCheck and dryNow:
        
        pushover("Yay, no more rain!")
        
    # Remember what the reading was for next check
    dryLastCheck = dryNow

    # Wait a bit
    sleep(5)
