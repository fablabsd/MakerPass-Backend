#!/usr/bin/python

import RPi.GPIO as GPIO
import subprocess
import time 


# use P1 header pin numbering convention
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

# Set up the GPIO channels
GPIO.setup(17, GPIO.OUT)
 

## loop infinitely checking if makerpass process exists
## and if so keep light on, otherwise turn off
while (True):
	process_exists =  subprocess.Popen("ps -elf | \grep  -P \"makerpass.+main.py\" | \grep -v grep", shell=True, stdout=subprocess.PIPE).stdout.read()

	if (process_exists):
		GPIO.output(17, GPIO.HIGH)
	else:
		GPIO.output(17, GPIO.LOW)

	## sleep 10 seconds to take it easy on CPU
	time.sleep(10)

 
 
