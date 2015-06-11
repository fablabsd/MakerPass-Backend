#!/usr/bin/python

from MachineStates import MachineStates

#config_fd = open("pipe_scan", "r")
#device_name = config_fd.read().rstrip()
device_name = "12|34\n".rstrip()
#config_fd.close()

print device_name

value1, value2 = device_name.split("|")

print value1
print value2

print MachineStates.toString(MachineStates.STATE_ALL_ON)


