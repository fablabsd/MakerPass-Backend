#!/usr/bin/python

import sys
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
	def enableMachinePlug(self):
		print "FATAL:  Machine.enableMachinePlug() called directly - should be called from derived class"
		sys.exit(1)	
	def disableMachinePlug(self):
		print "FATAL:  Machine.disableMachinePlug() called directly - should be called from derived class"
		sys.exit(1)	
	def isMachinePlugEnabled(self):
		print "FATAL:  Machine.isMachinePlugEnabled() called directly - should be called from derived class"
		sys.exit(1)	
	def isSwitchedOn(self):
		print "FATAL:  Machine.isSwitchedOn() called directly - should be called from derived class"
		sys.exit(1)	
	def manageState(self):
		if (self.plug.statemap_type == "ON_OFF_W_POWER_MONITOR"):
			self.manageState_on_off_power_monitor()
		elif (self.plug.statemap_type == "ON_OFF"):
			self.manageState_on_off()	
		else:
			print "Error:  Unrecognized statemap type for this Machine Smartplug device:  " + self.plug.statemap_type
			sys.exit()

	def manageState_on_off_power_monitor(self):
		print "FATAL:  Machine.manageState_on_off_power_monitor() called directly - should be called from derived class"
		sys.exit(1) 

	def manageState_on_off(self):
		print "FATAL:  Machine.manageState_on_off() called directly - should be called from derived class"
		sys.exit(1) 
		
