#!/usr/bin/python

import MakerPassDatabase

from MachinePlug import MachinePlug
from MachineStates import MachineStates
from datetime import datetime
from MakerPassLogger import MachinePlug_PowerMonitored_logger as logger


class MachinePlug_PowerMonitored(MachinePlug):

	def __init__(self, machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold):
		super(MachinePlug_PowerMonitored, self).__init__(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold)

		## we delay calls to isSwitchedOn() to reduce network overhead -- these
		## vars help us perform timeouts -- we re-mark this time when leaving ALL_OFF state
		self.switched_on_timeout_start = datetime.now()
	
		## time delay before calling isSwitchedOn() functionality again (seconds)
		self.switched_on_delay_time = 10

		## store continuous state of plug switch as we will not always
		## recalculate the value on each call of isSwitchedOn()
		self.switch_state = False

        ##  ----- METHODS -------------------------------------


        def enableMachinePlug(self):
                logger.debug( " MachinePlug_PowerMonitored.enableMachinePlug() called ")
		self.doEnableMachinePlug()
        def disableMachinePlug(self):
                logger.debug( " MachinePlug_PowerMonitored.disableMachinePlug() called ")
		self.doDisableMachinePlug()

	def isPowerAboveThreshold(self):

		return self.doIsPowerAboveThreshold()
		
        def isSwitchedOn(self):


		## calculate how long since last call 
        	switch_on_timeout_end = datetime.now()
        	timediff_millis = (switch_on_timeout_end - self.switched_on_timeout_start).total_seconds()
		#logger.debug( str(timediff_millis))

		## wait at least switch_on_delay_time seconds before making actual check again
		## this not only prevents killing the network, but gives time for the machine to 
		## ramp up power before the next power check
        	if ( timediff_millis > self.switched_on_delay_time ):
                	logger.debug( "Making isSwitchedOn() check after delay:  %.2gs" % timediff_millis)
			self.switch_state = self.isPowerAboveThreshold()
                	self.switched_on_timeout_start = datetime.now()
		
		return self.switch_state

	def doManageState(self, scan_detected, is_new_user):


		if (self.state == MachineStates.STATE_ALL_OFF):

			## machine and plug are both off in this state
			## so we are just waiting for a scan
	
			if (is_new_user == True): 
				logger.debug( "plug_id:  " + self.plug_id  )
				logger.debug( "Transition to STATE_NEED_SWITCH_ON\n")
				self.enableMachinePlug()
				## mark begin time for doing isSwitchedOn() check -- this
				## is important to mark here as we need an initial delay
				## to be x seconds to give machine time to power on
				## otherwise
				self.switched_on_timeout_start = datetime.now()
				self.state = MachineStates.STATE_NEED_SWITCH_ON
				MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))
			
	
		elif (self.state == MachineStates.STATE_NEED_SWITCH_ON):
			
			## in this state the user has swiped in successfully, and the plug
			## is enabled, but the machine has not yet been switched on, so we
			## are still giving the user the chance to swipe out if desired
 
			if (self.isSwitchedOn()):
			
				logger.debug( "plug_id:  " + self.plug_id  )
				logger.debug( "Transition to STATE_ALL_ON\n")
				
				self.state = MachineStates.STATE_ALL_ON
				MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))
				
				## mark machine effective use time - this is the time the machine has actually been switched on
				## we do this so the user is not charged for time between when they scanned and the machine was turned on				
				MakerPassDatabase.markMachineEffectiveUseTime(self.current_user, self.machine_id)
				
				
			## detect new user
			elif (scan_detected == True): 
				
				## detect an "unswipe" - no need to detect new user here
				if (is_new_user == False): 
					logger.debug( "plug_id:  " + self.plug_id)
					logger.debug( "Transition to STATE_ALL_OFF\n")
					self.state = MachineStates.STATE_ALL_OFF;
					self.disableMachinePlug()
					self.current_user = ""
					MakerPassDatabase.clearMachineUser(self.machine_id)
					MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))

		elif (self.state == MachineStates.STATE_ALL_ON):
	
			## note there is no "unswipe" option here - we do not
			## automatically switch off a machine  - user must turn
			## it off and then they will be automatically logged out
			## otherwise, if a new person has logged in, we stay in 
			## this state
			if (not(self.isSwitchedOn())): 
				logger.debug( "plug_id:  " + self.plug_id  )
				logger.debug( "Transition to STATE_ALL_OFF\n")
				self.state = MachineStates.STATE_ALL_OFF
				self.disableMachinePlug()
				MakerPassDatabase.logoutUser(self.current_user, self.machine_id)
				self.current_user = ""
				MakerPassDatabase.clearMachineUser(self.machine_id)
				MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))

		else: 
			logger.debug( "MachinePlug_PowerMonitored.doManageState():  oops..invalid state encountered...")
			logger.debug( " must have been those darn cosmic rays..")
			raise SystemExit
	

	

