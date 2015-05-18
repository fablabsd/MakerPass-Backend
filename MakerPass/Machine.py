#!/usr/bin/python

import SmartPlug
import MakerPassDatabase

class MachineStates:
        ## enumerated machine states
        STATE_ALL_OFF = 0
        STATE_NEED_ENABLE = 1
        STATE_NEED_SWITCH_ON = 2
        STATE_ALL_ON = 3

	
class Machine(object):


	def __init__(self, machine_id, plug_id):
		self.machine_id = machine_id
		self.state = MachineStates.STATE_ALL_OFF
		self.current_user = ""
		
		## might need another database table for this one i.e. map machine and plug to threshold value 
		self.switched_on_threshold = 10 ## ?? -- might need another database table for this i.e. 

		## get smartplug info for this machine
		rowdata = MakerPassDatabase.getSmartPlugData(plug_id)
		if (len(rowdata) == 0): 
			print "Error:  Failed to retrieve smartplug_rec for the given plug_id: " + plug_id
			raise SystemExit

		## should only be one...
		self.plug = SmartPlug.SmartPlug(rowdata[0]['plug_id'], \
		rowdata[0]['description'], rowdata[0]['ip_address'], \
		rowdata[0]['statemap_type'])

	
	##  ----- METHODS ------------------------------------- 
	def enableMachinePlug():
		pass
	def disableMachinePlug():
		pass
	def isMachinePlugEnables():
		pass
	def isSwitchedOn():
		pass
	def manageState():
		pass

