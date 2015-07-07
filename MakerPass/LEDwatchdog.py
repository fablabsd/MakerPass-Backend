#!/usr/bin/python

import RPi.GPIO as GPIO
import subprocess
import time 


# use P1 header pin numbering convention
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

# Set up the GPIO channels
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
 

## loop infinitely checking if makerpass process exists
## and if so keep light on, otherwise turn off
while (True):
	process_exists =  subprocess.Popen("ps -elf | \grep  -P \"makerpass.+main.py\" | \grep -v grep", shell=True, stdout=subprocess.PIPE).stdout.read()

	## if process exists, set LEDs high, and touch the process_online file for read by 
	## cgi/MakerPassWebClient.py...otherwise, blink the LEDs and remove file
	if (process_exists):
		GPIO.output(17, GPIO.HIGH)
		GPIO.output(27, GPIO.HIGH)
		subprocess.Popen("touch /home/pi/makerpass/MakerPass/process_online", shell=True, stdout=subprocess.PIPE).stdout.read()
		## sleep 10 seconds to take it easy on CPU
		time.sleep(10)
	else:
		GPIO.output(17, GPIO.LOW)
		GPIO.output(27, GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(17, GPIO.HIGH)
		GPIO.output(27, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(17, GPIO.LOW)
		GPIO.output(27, GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(17, GPIO.HIGH)
		GPIO.output(27, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(17, GPIO.LOW)
		GPIO.output(27, GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(17, GPIO.HIGH)
		GPIO.output(27, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(17, GPIO.LOW)
		GPIO.output(27, GPIO.LOW)
		time.sleep(5)
		subprocess.Popen("\\rm -f /home/pi/makerpass/MakerPass/process_online", shell=True, stdout=subprocess.PIPE).stdout.read()

 
