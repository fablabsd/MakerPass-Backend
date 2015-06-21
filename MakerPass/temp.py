#!/usr/bin/python

import subprocess
from MachineStates import MachineStates
from MakerPassLogger import logger


def test_logger():
	logger.debug("logger output")
	
	
import logging
logging.basicConfig(filename='/home/pi/makerpass/MakerPass/logs/example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')




#config_fd = open("pipe_scan", "r")
#device_name = config_fd.read().rstrip()
device_name = "12|34\n".rstrip()
#config_fd.close()

print device_name

value1, value2 = device_name.split("|")

print value1
print value2

print MachineStates.toString(MachineStates.STATE_ALL_ON)

process_exists =  subprocess.Popen("ps -elf | \grep  makerpass | \grep -v grep", shell=True, stdout=subprocess.PIPE).stdout.read()

if (process_exists):
	print "yes\n"
else:
	print "no\n"

test_logger()