#!/usr/bin/python

class MachineStates:
        ## enumerated machine states
        STATE_ALL_OFF = 0
        STATE_NEED_SWITCH_ON = 1 
        STATE_ALL_ON = 2 

	string_version = ['Off', 'Switch On Machine', 'Active/Running']

	@staticmethod	
	def toString(value):
		return MachineStates.string_version[value]
		
