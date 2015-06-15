#!/usr/bin/python

import subprocess
import time 


## kill watchdog process(es)
process_id =  subprocess.Popen("ps -eo pid,comm,args | \grep  -P --max-count=1  \"makerpass.+LEDwatchdog.py\" | \grep -v grep | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.read()

while (process_id):

	print "Killing PID: " + process_id
	print subprocess.Popen("sudo kill -9 " + process_id, shell=True, stdout=subprocess.PIPE).stdout.read()
	process_id =  subprocess.Popen("ps -eo pid,comm,args | \grep  -P --max-count=1  \"makerpass.+LEDwatchdog.py\" | \grep -v grep | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.read()


