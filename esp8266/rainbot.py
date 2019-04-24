# Rain Detector
# MagPi Issue 74
# PJ Evans @mrpjevans
# Version for ESP8266 / MicroPython

import os
import network   # pylint: disable=all
import time
import machine
import urequests
import ujson

# Load and configure Wifi
with open('rainbot.json') as configJson:
    config = ujson.load(configJson)
sta_if = network.WLAN(network.STA_IF)


# Connect to wifi
def connectToWifi():

    if sta_if.isconnected() is False:
        print('Not connected')
        if sta_if.active() is False:
            print('Activating interface')
            sta_if.active(True)
        print('Connecting to ' + config['ssid'])
        sta_if.connect(config['ssid'], config['psk'])
        while True:
            print('Checking connection')
            time.sleep(1)
            if sta_if.isconnected():
                print('Connected to Wifi')
                break
    else:
        print('Connected to Wifi')


# Send alert to Pushover
def pushover(message):

    print(message)

    # Check Wifi Connection
    connectToWifi()

    url = "https://api.pushover.net:443/1/messages.json"
    headers = {"Content-type": "application/json"}
    data = '{"token": "' + config['pushover_app_key'] + '","user": "' + config['pushover_user_key'] + '","title": "Rainbot", "message": "' + message + '"}'
    resp = urequests.post(url, data=data, headers=headers)

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
    dryNow = currentValue > int(config['sensor_threshold'])

    if dryLastCheck and not dryNow:

        pushover("It's Raining!")

    elif not dryLastCheck and dryNow:

        pushover("Yay, no more rain!")

    # Remember what the reading was for next check
    dryLastCheck = dryNow

    # Wait a bit
    time.sleep(5)
