#!/usr/bin/python


config_fd = open("pipe_scan", "r")
device_name = config_fd.read()
config_fd.close()

print device_name

