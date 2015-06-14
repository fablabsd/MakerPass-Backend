#!/usr/bin/python

import subprocess
import time 

process_id =  subprocess.Popen("ps -elf | \grep  -P --max-count=1  \"makerpass.+main.py\" | \grep -v grep | cut -d\" \" -f9", shell=True, stdout=subprocess.PIPE).stdout.read()


## kill makerpass processes
while (process_id):

	print "Killing PID: " + process_id
	print subprocess.Popen("sudo kill -9 " + process_id, shell=True, stdout=subprocess.PIPE).stdout.read()
	process_id =  subprocess.Popen("ps -elf | \grep  -P --max-count=1  \"makerpass.+main.py\" | \grep -v grep | cut -d\" \" -f9", shell=True, stdout=subprocess.PIPE).stdout.read()



