#!/usr/bin/python

import RPi.GPIO as GPIO
import subprocess
import time 


# use P1 header pin numbering convention
GPIO.setmode(GPIO.BCM)

# Set up the GPIO channels
GPIO.setup(27, GPIO.OUT)
 
GPIO.output(27, GPIO.HIGH)

 
