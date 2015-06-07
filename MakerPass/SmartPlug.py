#!/usr/bin/python

from MachineStates import MachineStates



class SmartPlug(object):
        
	def __init__(self, plug_id, description, ip_address, plug_name):
                self.plug_id = plug_id
                self.description = description
                self.ip_address = ip_address
                self.plug_name = plug_name
		self.state = MachineStates.STATE_ALL_OFF

