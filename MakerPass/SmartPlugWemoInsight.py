#!/usr/bin/python

from MachineStates import MachineStates
from SmartPlug import SmartPlug

class SmartPlugWemoInsight(SmartPlug):
        
	def __init__(self, plug_id, description, ip_address):
		super(SmartPlugWemoInsight, self).__init__(plug_id, description, ip_address)
		self.switched_on_threshold = 12345  ## need to address what this value should be


        ##  ----- METHODS -------------------------------------
        def enableMachinePlug(self):
                print " SmartPlugWemoInsight.enableMachinePlug() called "
        def disableMachinePlug(self):
                print " SmartPlugWemoInsight.disableMachinePlug() called "
        def isMachinePlugEnabled(self):
                print " SmartPlugWemoInsight.isMachinePlugPlugEnabled() called "
        def isSwitchedOn(self):
                print " SmartPlugWemoInsight.isSwitchedOn() called "

        def manageState(self, scan_detected, is_new_user):
                print "SmartPlugTestBrand.manageState() called"

		if (self.state == MachineStates.STATE_ALL_OFF):
	
			if (is_new_user == True): 
				self.state = MachineStates.STATE_NEED_SWITCH_ON
			
			if (self.isSwitchedOn()): self.state = MachineStates.STATE_NEED_ENABLE
	
	
		elif (self.state == MachineStates.STATE_NEED_SWITCH_ON):
	
			if (self.isSwitchedOn()):
				enableMachinePlug()
				self.state = MachineStates.STATE_ALL_ON

			## detect an "unswipe"
			if (scan_detected == True): 
				if (is_new_user == False): self.state = ALL_OFF;

		elif (self.state == MachineStates.STATE_NEED_ENABLE):	
	
			if ( is_new_user == True ): 
				enableMachinePlug()
				self.state = MachineStates.STATE_ALL_ON
			
			if (Not(self.isSwitchedOn())): self.state = MachineStates.STATE_ALL_OFF
	
		elif (self.state == MachineStates.STATE_ALL_ON):
	
			## note there is no "unswipe" option here - we do not
			## automatically switch off a machine  - user must turn
			## it off and then they will be automatically logged out
			if (Not(self.isSwitchedOn())): 
				self.state = MachineStates.STATE_ALL_OFF
				disableMachinePlug()
	
		else: 
			print "StatePlugWemoInsight.manageState():  oops..invalid state encountered..."
			print " must have been those darn cosmic rays.."
			raise SystemExit
	
	

