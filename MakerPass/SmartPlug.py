#!/usr/bin/python

from MachineStates import MachineStates



class SmartPlug(object):
        
	def __init__(self, plug_id, description, ip_address, plug_name, machine_power_threshold):
                self.plug_id = plug_id
                self.description = description
                self.ip_address = ip_address
		self.state = MachineStates.STATE_ALL_OFF
                
		## unique name of the plug, used to 
		## determine what plug to connect to (i.e. it's loaded into the plug beforehand) 
		self.plug_name = plug_name

		## used to determine whether machine is switch one - in milliwatts
		self.machine_power_threshold = machine_power_threshold

