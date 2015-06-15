#!/usr/bin/python

import subprocess
import time 

process_id =  subprocess.Popen("ps -eo pid,comm,args | \grep  -P --max-count=1  \"makerpass.+main.py\" | \grep -v grep | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.read()


## kill makerpass processes
while (process_id):

	print "Killing PID: " + str(process_id)
	print subprocess.Popen("sudo kill -9 " + str(process_id), shell=True, stdout=subprocess.PIPE).stdout.read()
	process_id =  subprocess.Popen("ps -eo pid,comm,args | \grep  -P --max-count=1  \"makerpass.+main.py\" | \grep -v grep | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.read()



