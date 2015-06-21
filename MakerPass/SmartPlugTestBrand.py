#!/usr/bin/python

import logging

from MachineStates import MachineStates
from SmartPlug import SmartPlug
from datetime import datetime
from MakerPassLogger import SmartPlugTestBrand_logger as logger

class SmartPlugTestBrand(SmartPlug):
        
	def __init__(self, plug_id, description, ip_address, plug_name, machine_power_threshold):
		super(SmartPlugTestBrand, self).__init__(plug_id, description, ip_address, plug_name, machine_power_threshold)

		## we delay calls to isSwitchedOn() to reduce network overhead -- these
		## vars help us perform timeouts 
		self.switched_on_timeout_start = datetime.now()
	
		## time delay before calling isSwitchedOn() functionality again (seconds)
		self.switched_on_delay_time = 10

		## store continuous state of plug switch as we will not always
		## recalculate the value on each call of isSwitchedOn()
		self.switch_state = False


        ##  ----- METHODS -------------------------------------
        def enableMachinePlug(self):
                logger.debug( " SmartPlugTestBrand.enableMachinePlug() called ")
        def disableMachinePlug(self):
                logger.debug( " SmartPlugTestBrand.disableMachinePlug() called ")
        def isMachinePlugEnabled(self):
                logger.debug( " SmartPlugTestBrand.isMachinePlugPlugEnabled() called ")

	def checkSwitchState(self):

                try:

                        fd = open("switch_machine_on","r+")
                        if (fd != None):
                                fd.close()
                                return True

                except IOError:
                        pass

                return False
		
        def isSwitchedOn(self):


		## calculate how long since last call 
        	switch_on_timeout_end = datetime.now()
        	timediff_millis = (switch_on_timeout_end - self.switched_on_timeout_start).total_seconds()
		#logger.debug( str(timediff_millis))

		## wait at least switch_on_delay_time seconds before making actual check again
        	if ( timediff_millis > self.switched_on_delay_time ):
                	logger.debug( "Making isSwitchedOn() check after delay:  %.2gs" % timediff_millis)
			self.switch_state = self.checkSwitchState()
                	self.switched_on_timeout_start = datetime.now()
		
		return self.switch_state

	def manageState(self, scan_detected, is_new_user):


		if (self.state == MachineStates.STATE_ALL_OFF):

			## machine and plug are both off in this state
			## so we are just waiting for a scan
	
			if (is_new_user == True): 
				logger.debug( "plug_id:  " + self.plug_id + " - " + self.ip_address )
				logger.debug( "Transition to STATE_NEED_SWITCH_ON\n")
				self.enableMachinePlug()
				self.state = MachineStates.STATE_NEED_SWITCH_ON
			
	
		elif (self.state == MachineStates.STATE_NEED_SWITCH_ON):
			
			## in this state the user has swiped in successfully, and the plug
			## is enabled, but the machine has not yet been switched on, so we
			## are still giving the user the chance to swipe out if desired
 
			if (self.isSwitchedOn()):
				self.state = MachineStates.STATE_ALL_ON
				logger.debug( "plug_id:  " + self.plug_id + " - " + self.ip_address )
				logger.debug( "Transition to STATE_ALL_ON\n")

			## detect new user
			elif (scan_detected == True): 
				
				## detect an "unswipe" 
				if (is_new_user == False): 
					self.state = MachineStates.STATE_ALL_OFF;
					logger.debug( "plug_id:  " + self.plug_id + " - " + self.ip_address )
					logger.debug( "Transition to STATE_ALL_OFF\n")


		elif (self.state == MachineStates.STATE_ALL_ON):
	
			## note there is no "unswipe" option here - we do not
			## automatically switch off a machine  - user must turn
			## it off and then they will be automatically logged out
			## otherwise, if a new person has logged in, we stay in 
			## this state
			if (not(self.isSwitchedOn())): 
				self.state = MachineStates.STATE_ALL_OFF
				self.disableMachinePlug()
				logger.debug( "plug_id:  " + self.plug_id + " - " + self.ip_address )
				logger.debug( "Transition to STATE_ALL_OFF\n")

		else: 
			logger.debug( "StatePlugWemoInsight.manageState():  oops..invalid state encountered...")
			logger.debug( " must have been those darn cosmic rays..")
			raise SystemExit
	

	

