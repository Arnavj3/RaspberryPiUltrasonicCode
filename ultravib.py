#!/usr/bin/python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import urllib2
import json

url = 'https://temp-data-cf6e2.firebaseio.com/tempdata.json'


GPIO.setmode(GPIO.BCM)

trigger = 18
echo = 24
vibmotor = 23

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(vibmotor, GPIO.OUT)

def distance():
        #set trigger to high
        GPIO.output(trigger, True)

        #set trigger after 0.01ms to low
        time.sleep(0.00001)
        GPIO.output(trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        #save StartTime
        while GPIO.input(echo) == 0:
                StartTime = time.time()

        #save time of arrival 
        while GPIO.input(echo) == 1:
                StopTime = time.time()


        #time difference between start and arrival
        TimeElapsed = StartTime - StopTime

        distance = (TimeElapsed * 34300)/2

        return abs(distance) 

def sendData(distance):
        postdata = {
                'Distance': distance
  }

        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        data = json.dumps(postdata)

        response = urllib2.urlopen(req,data)

def checkDist(distance):
	if distance <= 5:
		return 1

	else:
		return 0

if __name__ == '__main__':
	try:
                while True:
                        dist = distance()
                        print("Measured distance = %.1f cm" %dist)
                        sendData(dist)
			if checkDist(dist) == 1 :
				GPIO.output(vibmotor, GPIO.HIGH)

                        #time.sleep(1)

        except KeyboardInterrupt:
                print "-- Measurement Stopped --"
                GPIO.cleanup()

