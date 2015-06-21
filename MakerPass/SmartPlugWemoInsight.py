#!/usr/bin/python

import ouimeaux

from MachineStates import MachineStates
from SmartPlug import SmartPlug
from datetime import datetime
from ouimeaux.environment import Environment
from ouimeaux.environment import UnknownDevice
from MakerPassLogger import SmartPlugWemoInsight_logger as logger

class SmartPlugWemoInsight(SmartPlug):

	## static instance of the wemo environment
	env = 0
        
	def __init__(self, plug_id, description, ip_address, plug_name, machine_power_threshold):
		super(SmartPlugWemoInsight, self).__init__(plug_id, description, ip_address, plug_name, machine_power_threshold)

		## create the static/global WEMO environment variable if it doesn't exist
		if (SmartPlugWemoInsight.env == 0):
			SmartPlugWemoInsight.env = Environment(with_cache=False, bind=None)
			SmartPlugWemoInsight.env.start()
        		SmartPlugWemoInsight.env.discover(3)
			
		self.wemo_switch = self.getSwitch(plug_name)
		logger.debug( "switch = " + str(self.wemo_switch))

		## we delay calls to isSwitchedOn() to reduce network overhead -- these
		## vars help us perform timeouts -- we re-mark this time when leaving ALL_OFF state
		self.switched_on_timeout_start = datetime.now()
	
		## time delay before calling isSwitchedOn() functionality again (seconds)
		self.switched_on_delay_time = 10

		## store continuous state of plug switch as we will not always
		## recalculate the value on each call of isSwitchedOn()
		self.switch_state = False


        ##  ----- METHODS -------------------------------------

	def getSwitch(self, plug_name):
		try:
			return SmartPlugWemoInsight.env.get_switch(plug_name)
		except (UnknownDevice):
			logger.debug( "Unable to get switch:  " + self.plug_name)
			raise UnknownDevice
			

        def enableMachinePlug(self):
                logger.debug( " SmartPlugWemoInsight.enableMachinePlug() called ")
		self.wemo_switch.basicevent.SetBinaryState(BinaryState=1)
        def disableMachinePlug(self):
                logger.debug( " SmartPlugWemoInsight.disableMachinePlug() called ")
		self.wemo_switch.basicevent.SetBinaryState(BinaryState=0)
        #def isMachinePlugEnabled(self):
                #logger.debug( " SmartPlugWemoInsight.isMachinePlugPlugEnabled() called ")

	def isPowerAboveThreshold(self):

		power = self.wemo_switch.current_power
		logger.debug( "power for " + self.plug_name + ": " + str(power))
			
		if (power > self.machine_power_threshold):
			return True

                return False
		
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

	def manageState(self, scan_detected, is_new_user):


		if (self.state == MachineStates.STATE_ALL_OFF):

			## machine and plug are both off in this state
			## so we are just waiting for a scan
	
			if (is_new_user == True): 
				logger.debug( "plug_id:  " + self.plug_id + " - " + self.ip_address )
				logger.debug( "Transition to STATE_NEED_SWITCH_ON\n")
				self.enableMachinePlug()
				## mark begin time for doing isSwitchedOn() check -- this
				## is important to mark here as we need an initial delay
				## to be x seconds to give machine time to power on
				self.switched_on_timeout_start = datetime.now()
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
				
				## detect an "unswipe" - no need to detect new user here
				if (is_new_user == False): 
					self.state = MachineStates.STATE_ALL_OFF;
					logger.debug( "plug_id:  " + self.plug_id + " - " + self.ip_address )
					logger.debug( "Transition to STATE_ALL_OFF\n")
					self.disableMachinePlug()

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
	

	

