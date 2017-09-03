#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)

status = True

if status == True:
    GPIO.output(22,True)
    time.sleep(1)
else:
    GPIO.output(22,False)
    time.sleep(1)
GPIO.cleanup()
