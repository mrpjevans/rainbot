# Rain Detector
# MagPi Issue 74
# PJ Evans @mrpjevans
# Version for ESP8266 / MicroPython

import os
import network   # pylint: disable=all
from time import sleep
import machine
import urequests

#from network import WLAN
wlan = network.WLAN(network.STA_IF)

#
# Functions
#

def loadEnv():
    env = {}
    files = os.listdir() 
    if ".env" in files:
        with open(".env", "r") as envfile:
            for line in envfile:
                line = line.rstrip("\n")
                pair = line.split('=')
                if len(pair) > 1:
                    env[pair[0]] = pair[1]
    return env

# Helper for maintaining a wifi connection
def wifiConnect():

    if not wlan.isconnected():
        print('Connecting to ' + env['WIFI_SSID'])
        wlan.connect(env['WIFI_SSID'], env['WIFI_PASS'])
        while not wlan.isconnected():
                machine.idle() # save power while waiting
        print('WLAN connection succeeded!')

def pushover(message):

    print(message)

    # Check Wifi Connection
    wifiConnect()

    url = "https://api.pushover.net:443/1/messages.json"
    headers = {"Content-type": "application/json" }
    data = '{"token": "' + env['PUSHOVER_API'] + '","user": "' + env['PUSHOVER_USER'] + '","title": "Rain Detector", "message": "' + message + '"}'
    resp = urequests.post(url, data=data, headers=headers)

# Load up
env = loadEnv()

# Send startup message (and Check Wifi Connection)
pushover('Rainbot lives!')

# Set up connection to analog pin
adc = machine.ADC(0)

# Is it raining? Let's assume not.
dryLastCheck = True

# Loop forever
while True:

    # Read rain sensor
    currentValue = adc.read()
    print('Sensor: ' + str(currentValue))

    # Is it dry? (1024 = completely dry)
    dryNow = currentValue > int(env['SENSOR_THRESHOLD'])

    if dryLastCheck and not dryNow:

        pushover("It's Raining!")
        
    elif not dryLastCheck and dryNow:
        
        pushover("Yay, no more rain!")
        
    # Remember what the reading was for next check
    dryLastCheck = dryNow

    # Wait a bit
    sleep(5)
